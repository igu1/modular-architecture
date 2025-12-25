import logging
import os
from datetime import datetime
from typing import Optional

class CoreLogger:
    def __init__(self):
        self._loggers = {}
        self._setup_root_logger()
        self.log_dir = 'logs'
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def _setup_root_logger(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    def get_logger(self, module_name: str, module_class: Optional[str] = None):
        logger_name = f"modules.{module_name}"
        if module_class:
            logger_name += f".{module_class}"
        
        if logger_name not in self._loggers:
            self._loggers[logger_name] = logging.getLogger(logger_name)
            self._loggers[logger_name].setLevel(logging.DEBUG)
            
            log_file = os.path.join(self.log_dir, f'{module_name}_{datetime.now().strftime("%Y%m%d")}.log')
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            
            formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            
            self._loggers[logger_name].addHandler(file_handler)
            self._loggers[logger_name].propagate = False
        
        return self._loggers[logger_name]
    
    def log(self, module_name: str, message: str, level: str = 'info', module_class: Optional[str] = None):
        logger = self.get_logger(module_name, module_class)
        
        level_map = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        
        log_level = level_map.get(level.lower(), logging.INFO)
        
        if not logger.handlers:
            log_file = os.path.join(self.log_dir, f'{module_name}_{datetime.now().strftime("%Y%m%d")}.log')
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.propagate = False
        
        logger.log(log_level, message)
        print(f'[{module_name.upper()}] {level.upper()}: {message}')
    
    def log_event(self, event_data: dict):
        event_name = event_data.get('event_name', 'unknown')
        source = event_data.get('source', 'unknown')
        data = event_data.get('data', {})
        
        message = f"Event '{event_name}' from {source}"
        if data:
            message += f" | Data: {data}"
        
        self.log(source or 'system', f"EVENT: {message}", 'info')

core_logger = CoreLogger()
