import os
import importlib
from typing import List, Dict, Any
from .patch_types import Patch

class PatchEngine:
    def __init__(self):
        self.patches: List[Patch] = []
        self.applied_patches: Dict[str, List[Patch]] = {}
        self._logger = None
    
    def set_logger(self, logger):
        self._logger = logger
    
    def _log(self, message: str, level: str = 'info'):
        if self._logger:
            self._logger.log('patch_engine', message, level)
    
    def register_patch(self, patch: Patch):
        self.patches.append(patch)
        self.patches.sort(key=lambda p: p.priority)
        self._log(f"Registered patch for module '{patch.target_module}' (type: {patch.get_patch_info()['type']})")
    
    def register_patches(self, patches: List[Patch]):
        for patch in patches:
            self.register_patch(patch)
    
    def apply_patches_to_module(self, module_name: str, module_instance: Any, env: Any) -> int:
        applicable_patches = [p for p in self.patches if p.target_module == module_name and not p.applied]
        
        if not applicable_patches:
            return 0
        
        applied_count = 0
        for patch in applicable_patches:
            try:
                success = patch.apply(module_instance, env)
                if success:
                    applied_count += 1
                    if module_name not in self.applied_patches:
                        self.applied_patches[module_name] = []
                    self.applied_patches[module_name].append(patch)
                    self._log(f"Applied patch to module '{module_name}'")
            except Exception as e:
                self._log(f"Error applying patch to module '{module_name}': {e}", 'error')
        
        return applied_count
    
    def load_patches_from_directory(self, patches_dir: str):
        if not os.path.exists(patches_dir):
            self._log(f"Patches directory not found: {patches_dir}", 'warning')
            return
        
        for filename in os.listdir(patches_dir):
            if filename.endswith('.py') and not filename.startswith('__') and filename not in ['patch_types.py', 'patch_engine.py']:
                module_name = filename[:-3]
                try:
                    patch_module = importlib.import_module(f'patches.{module_name}')
                    
                    if hasattr(patch_module, 'patches'):
                        patches_list = getattr(patch_module, 'patches')
                        if isinstance(patches_list, list):
                            self.register_patches(patches_list)
                            self._log(f"Loaded {len(patches_list)} patches from '{filename}'")
                    
                    if hasattr(patch_module, 'get_patches'):
                        get_patches_func = getattr(patch_module, 'get_patches')
                        if callable(get_patches_func):
                            patches_list = get_patches_func()
                            if isinstance(patches_list, list):
                                self.register_patches(patches_list)
                                self._log(f"Loaded {len(patches_list)} patches from '{filename}' via get_patches()")
                    
                except Exception as e:
                    self._log(f"Error loading patches from '{filename}': {e}", 'error')
    
    def get_patches_for_module(self, module_name: str) -> List[Patch]:
        return [p for p in self.patches if p.target_module == module_name]
    
    def get_applied_patches_for_module(self, module_name: str) -> List[Patch]:
        return self.applied_patches.get(module_name, [])
    
    def get_all_patches_info(self) -> List[Dict[str, Any]]:
        return [p.get_patch_info() for p in self.patches]
    
    def get_statistics(self) -> Dict[str, Any]:
        total_patches = len(self.patches)
        applied_patches = sum(len(patches) for patches in self.applied_patches.values())
        
        patches_by_type = {}
        for patch in self.patches:
            patch_type = patch.get_patch_info()['type']
            patches_by_type[patch_type] = patches_by_type.get(patch_type, 0) + 1
        
        return {
            'total_patches': total_patches,
            'applied_patches': applied_patches,
            'pending_patches': total_patches - applied_patches,
            'patches_by_type': patches_by_type,
            'modules_with_patches': list(self.applied_patches.keys())
        }
