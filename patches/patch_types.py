from abc import ABC, abstractmethod
from typing import Any, Callable, Dict

class Patch(ABC):
    def __init__(self, target_module: str, priority: int = 100):
        self.target_module = target_module
        self.priority = priority
        self.applied = False
    
    @abstractmethod
    def apply(self, module_instance: Any, env: Any) -> bool:
        pass

class FunctionPatch(Patch):
    def __init__(self, target_module: str, function_name: str, function: Callable, priority: int = 100):
        super().__init__(target_module, priority)
        self.function_name = function_name
        self.function = function
    
    def apply(self, module_instance: Any, env: Any) -> bool:
        if hasattr(module_instance, self.function_name):
            setattr(module_instance, f'_original_{self.function_name}', getattr(module_instance, self.function_name))
        setattr(module_instance, self.function_name, self.function.__get__(module_instance, type(module_instance)))
        self.applied = True
        return True
    
    def get_patch_info(self) -> Dict[str, Any]:
        return {'type': 'function'}

class ServicePatch(Patch):
    def __init__(self, target_module: str, service_name: str, service_class: type, priority: int = 100):
        super().__init__(target_module, priority)
        self.service_name = service_name
        self.service_class = service_class
    
    def apply(self, module_instance: Any, env: Any) -> bool:
        env.register_service(f"{self.target_module}_{self.service_name}", self.service_class())
        self.applied = True
        return True
    
    def get_patch_info(self) -> Dict[str, Any]:
        return {'type': 'service'}

class ModelPatch(Patch):
    def __init__(self, target_module: str, model_class: type, priority: int = 100):
        super().__init__(target_module, priority)
        self.model_class = model_class
    
    def apply(self, module_instance: Any, env: Any) -> bool:
        db_service = env.get_service('db_service')
        if db_service:
            db_session = db_service.get_session()
            self.model_class.metadata.create_all(db_session().bind)
            if not hasattr(module_instance, '_patched_models'):
                module_instance._patched_models = []
            module_instance._patched_models.append(self.model_class)
            self.applied = True
            return True
        return False
    
    def get_patch_info(self) -> Dict[str, Any]:
        return {'type': 'model'}

class FieldPatch(Patch):
    def __init__(self, target_module: str, model_name: str, field_name: str, field_column: Any, priority: int = 100):
        super().__init__(target_module, priority)
        self.model_name = model_name
        self.field_name = field_name
        self.field_column = field_column
    
    def apply(self, module_instance: Any, env: Any) -> bool:
        target_model = None
        for model in module_instance.get_models():
            if model.__name__ == self.model_name:
                target_model = model
                break
        
        if not target_model:
            return False
        
        setattr(target_model, self.field_name, self.field_column)
        
        db_service = env.get_service('db_service')
        if db_service:
            session = db_service.get_session()()
            try:
                from sqlalchemy import inspect, text
                table_name = target_model.__tablename__
                column_name = self.field_name
                
                inspector = inspect(session.bind)
                if column_name not in [col['name'] for col in inspector.get_columns(table_name)]:
                    target_model.__table__.append_column(self.field_column)
                    self.field_column.create(session.bind)
            except:
                try:
                    column_type = str(self.field_column.type)
                    if 'String' in column_type:
                        sql = text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} VARCHAR(100)")
                    elif 'Integer' in column_type:
                        sql = text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} INTEGER")
                    else:
                        sql = text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} VARCHAR(255)")
                    session.execute(sql)
                    session.commit()
                except:
                    pass
            finally:
                session.close()
        
        self.applied = True
        return True
    
    def get_patch_info(self) -> Dict[str, Any]:
        return {'type': 'field'}

class RoutePatch(Patch):
    def __init__(self, target_module: str, route_path: str, method: str, handler: Callable, priority: int = 100):
        super().__init__(target_module, priority)
        self.route_path = route_path
        self.method = method
        self.handler = handler
    
    def apply(self, module_instance: Any, env: Any) -> bool:
        env.registry.add_routes([(self.route_path, self.method, self.handler)], self.target_module)
        self.applied = True
        return True
    
    def get_patch_info(self) -> Dict[str, Any]:
        return {'type': 'route'}
