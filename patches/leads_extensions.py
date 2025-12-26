from patches.patch_types import FunctionPatch, FieldPatch
from datetime import datetime
from sqlalchemy import Column, String

def get_lead_statistics(self):
    db_session = self.get_db_session()
    if not db_session:
        return {'error': 'Database not available'}
    
    try:
        session = db_session()
        models = self.get_models()
        
        stats = {
            'timestamp': datetime.utcnow().isoformat(),
            'module': 'leads',
            'models_count': len(models)
        }
        
        for model in models:
            try:
                count = session.query(model).count()
                stats[f'{model.__tablename__}_count'] = count
            except:
                pass
        
        return stats
    except Exception as e:
        return {'error': str(e)}

patches = [
    FunctionPatch(
        target_module='leads',
        function_name='get_lead_statistics',
        function=get_lead_statistics,
        priority=100
    ),
    
    FieldPatch(
        target_module='leads',
        model_name='Lead',
        field_name='father_name',
        field_column=Column(String(100)),
        priority=90
    ),
    FieldPatch(
        target_module='leads',
        model_name='Lead',
        field_name='mother_name',
        field_column=Column(String(100)),
        priority=90
    ),
    FieldPatch(
        target_module='leads',
        model_name='Lead',
        field_name='guardian_name',
        field_column=Column(String(100)),
        priority=90
    ),
]
