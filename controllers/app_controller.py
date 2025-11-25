# controllers/app_controller.py
"""
AppController - Coordinador Central de la Aplicación
Gestión de estado global, configuración y coordinación entre módulos
Versión 2.0 - Integrado con core/utils
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

from config.paths import AppPaths
from gui.themes.theme_manager import ThemeManager
from core.utils.logger import get_controller_logger
from core.utils.file_utils import FileUtils


class AppController:
    """
    Controlador principal de la aplicación
    
    Responsabilidades:
    1. ✅ Gestión de configuración global
    2. ✅ Coordinación entre módulos  
    3. ✅ Estado global de la aplicación
    4. ✅ Gestión de temas y preferencias
    5. ✅ Manejo de errores a nivel aplicación
    6. ✅ Sistema de logging centralizado
    7. ✅ Utilidades de archivos centralizadas
    """
    
    def __init__(self):
        # Estado de la aplicación
        self.app_state = {
            'initialized': False,
            'current_tab': 'etl',
            'theme': 'dark',
            'data_loaded': False,
            'processing': False,
            'etl_completed': False
        }
        
        # Configuración
        self.settings = {}
        
        # Referencias a otros controladores
        self.etl_controller = None
        self.certificates_controller = None
        
        # Servicios
        self.theme_manager = None
        self.file_utils = FileUtils()
        
        # Sistema de logging
        self.logger = None
        
        # Inicializar
        self._initialize()
    
    def _initialize(self):
        """Inicialización del controlador de aplicación"""
        try:
            # 1. Configurar sistema de logging
            self._setup_logging()
            
            # 2. Cargar configuración
            self._load_settings()
            
            # 3. Inicializar ThemeManager
            self.theme_manager = ThemeManager()
            
            # 4. Aplicar configuración de tema
            theme = self.settings.get('app', {}).get('theme', 'dark')
            self.theme_manager.set_theme(theme)
            self.app_state['theme'] = theme
            
            # 5. Asegurar directorios de datos
            self._ensure_data_directories()
            
            # 6. Estado listo
            self.app_state['initialized'] = True
            
            self.log_info("✅ AppController inicializado correctamente")
            
        except Exception as e:
            error_msg = f"Error inicializando AppController: {e}"
            if self.logger:
                self.log_error(error_msg)
            else:
                print(f"❌ {error_msg}")
            # Configuración por defecto como fallback
            self._setup_default_config()
    
    def _setup_logging(self):
        """Configura el sistema de logging - ✅ ACTUALIZADO al sistema modular"""
        try:
            # ✅ USAR EL NUEVO SISTEMA MODULAR
            self.logger = get_controller_logger("AppController")
            self.log_info("✅ Sistema de logging modular inicializado")
            
        except Exception as e:
            print(f"❌ Error configurando logging: {e}")
            # Fallback a logging básico
            import logging
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger('AppController')
    
    def _ensure_data_directories(self):
        """Asegura que todos los directorios de datos existan"""
        try:
            directories = [
                AppPaths.get_raw_dir(),
                AppPaths.get_clean_dir(), 
                AppPaths.get_output_dir(),
                AppPaths.get_templates_dir(),
                Path("logs"),  # Directorio base de logs
                Path("logs/app"),  # Directorio específico de app
                Path("logs/etl"),  # Directorio específico de etl
                Path("logs/certificates")  # Directorio específico de certificates
            ]
            
            for directory in directories:
                if self.file_utils.ensure_dir(str(directory)):
                    print(f"✅ Directorio asegurado: {directory}")
                else:
                    print(f"⚠️ No se pudo crear directorio: {directory}")
                    
        except Exception as e:
            self.log_error("Error creando directorios de datos", e)
    
    def _load_settings(self):
        """Carga la configuración desde settings.json"""
        try:
            config_file = AppPaths.get_config_file()
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
                self.log_info(f"✅ Configuración cargada desde: {config_file}")
            else:
                self._setup_default_config()
                self.log_warning("⚠️ Configuración no encontrada, usando valores por defecto")
                
        except Exception as e:
            self.log_error("Error cargando configuración", e)
            self._setup_default_config()
    
    def _setup_default_config(self):
        """Configuración por defecto"""
        self.settings = {
            "app": {
                "name": "Sistema de Certificados",
                "version": "1.0.0", 
                "theme": "dark"
            },
            "etl": {
                "batch_size": 1000,
                "encoding": "utf-8"
            },
            "certificates": {
                "batch_size": 50,
                "retry_attempts": 3
            }
        }
    
    def save_settings(self):
        """Guarda la configuración actual en settings.json"""
        try:
            config_file = AppPaths.get_config_file()
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
                
            self.log_info(f"✅ Configuración guardada en: {config_file}")
            
        except Exception as e:
            self.log_error("Error guardando configuración", e)
    
    # === SISTEMA DE LOGGING ===
    
    def log_info(self, message: str, extra_data: Optional[dict] = None):
        """Log de información"""
        if hasattr(self.logger, 'info'):
            self.logger.info(message, extra_data)
        else:
            print(f"📝 {message}")
    
    def log_error(self, message: str, exception: Optional[Exception] = None):
        """Log de error"""
        if hasattr(self.logger, 'error'):
            self.logger.error(message, exception)
        else:
            error_msg = f"❌ {message}"
            if exception:
                error_msg += f" | Exception: {str(exception)}"
            print(error_msg)
    
    def log_warning(self, message: str, extra_data: Optional[dict] = None):
        """Log de advertencia"""
        if hasattr(self.logger, 'warning'):
            self.logger.warning(message, extra_data)
        else:
            warning_msg = f"⚠️ {message}"
            print(warning_msg)
    
    def log_debug(self, message: str, extra_data: Optional[dict] = None):
        """Log de debug"""
        if hasattr(self.logger, 'debug'):
            self.logger.debug(message, extra_data)
        else:
            debug_msg = f"🐛 {message}"
            print(debug_msg)
    
    # === GESTIÓN DE ESTADO ===
    
    def set_app_state(self, key: str, value: Any):
        """Actualiza el estado global de la aplicación"""
        old_value = self.app_state.get(key)
        self.app_state[key] = value
        
        # Persistir cambios importantes
        if key == 'theme':
            self.settings['app']['theme'] = value
            self.save_settings()
            self.log_info(f"🎨 Tema cambiado a: {value}")
        
        # Log de cambios de estado importantes
        if key in ['processing', 'etl_completed', 'data_loaded']:
            self.log_info(f"📊 Estado actualizado: {key} = {value} (antes: {old_value})")
    
    def get_app_state(self, key: str) -> Any:
        """Obtiene un valor del estado global"""
        return self.app_state.get(key)
    
    def get_full_app_state(self) -> Dict[str, Any]:
        """Obtiene todo el estado de la aplicación"""
        return self.app_state.copy()
    
    # === GESTIÓN DE MÓDULOS ===
    
    def register_etl_controller(self, etl_controller):
        """Registra el controlador ETL"""
        self.etl_controller = etl_controller
        self.log_info("✅ ETL Controller registrado en AppController")
    
    def register_certificates_controller(self, certificates_controller):
        """Registra el controlador de certificados"""
        self.certificates_controller = certificates_controller
        self.log_info("✅ Certificates Controller registrado en AppController")
    
    def get_controller(self, controller_type: str):
        """Obtiene un controlador registrado"""
        if controller_type == 'etl':
            return self.etl_controller
        elif controller_type == 'certificates':
            return self.certificates_controller
        return None
    
    def is_controller_available(self, controller_type: str) -> bool:
        """Verifica si un controlador está disponible"""
        return self.get_controller(controller_type) is not None
    
    # === GESTIÓN DE TEMAS ===
    
    def toggle_theme(self) -> str:
        """Alterna entre tema claro y oscuro"""
        new_theme = self.theme_manager.toggle_theme()
        self.set_app_state('theme', new_theme)
        return new_theme
    
    def get_current_theme_data(self) -> Dict[str, Any]:
        """Obtiene los datos del tema actual"""
        return self.theme_manager.theme_data
    
    def get_current_theme_name(self) -> str:
        """Obtiene el nombre del tema actual"""
        return self.theme_manager.get_current_theme()
    
    def set_theme(self, theme_name: str) -> bool:
        """Establece un tema específico"""
        try:
            self.theme_manager.set_theme(theme_name)
            self.set_app_state('theme', theme_name)
            return True
        except ValueError as e:
            self.log_error(f"Tema no encontrado: {theme_name}", e)
            return False
    
    # === GESTIÓN DE DATOS ===
    
    def set_data_loaded(self, loaded: bool = True):
        """Marca si hay datos cargados en la aplicación"""
        self.set_app_state('data_loaded', loaded)
    
    def is_data_loaded(self) -> bool:
        """Verifica si hay datos cargados"""
        return self.app_state.get('data_loaded', False)
    
    def set_etl_completed(self, completed: bool = True):
        """Marca si el procesamiento ETL está completado"""
        self.set_app_state('etl_completed', completed)
        if completed:
            self.set_data_loaded(True)
    
    def is_etl_completed(self) -> bool:
        """Verifica si el ETL está completado"""
        return self.app_state.get('etl_completed', False)
    
    def set_processing(self, processing: bool = True):
        """Marca si hay un proceso en ejecución"""
        self.set_app_state('processing', processing)
    
    def is_processing(self) -> bool:
        """Verifica si hay un proceso en ejecución"""
        return self.app_state.get('processing', False)
    
    # === CONFIGURACIÓN ===
    
    def get_setting(self, section: str, key: str, default: Any = None) -> Any:
        """Obtiene un valor de configuración"""
        return self.settings.get(section, {}).get(key, default)
    
    def set_setting(self, section: str, key: str, value: Any):
        """Establece un valor de configuración"""
        if section not in self.settings:
            self.settings[section] = {}
        self.settings[section][key] = value
        self.save_settings()
    
    # === UTILIDADES DE ARCHIVOS ===
    
    def validate_excel_file(self, file_path: str) -> bool:
        """Valida si un archivo es un Excel válido"""
        is_valid = self.file_utils.is_valid_excel_file(file_path)
        if is_valid:
            file_size = self.file_utils.get_file_size_readable(file_path)
            self.log_info(f"✅ Archivo Excel válido: {file_path} ({file_size})")
        else:
            self.log_warning(f"❌ Archivo Excel inválido: {file_path}")
        return is_valid
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Obtiene información de un archivo"""
        try:
            path = Path(file_path)
            if path.exists():
                return {
                    'exists': True,
                    'size_bytes': self.file_utils.get_file_size(file_path),
                    'size_readable': self.file_utils.get_file_size_readable(file_path),
                    'creation_time': self.file_utils.get_file_creation_time(file_path),
                    'modification_time': self.file_utils.get_file_modification_time(file_path),
                    'is_excel': self.file_utils.is_valid_excel_file(file_path)
                }
            else:
                return {'exists': False}
        except Exception as e:
            self.log_error("Error obteniendo información de archivo", e)
            return {'exists': False, 'error': str(e)}
    
    # === UTILIDADES ===
    
    def get_app_info(self) -> Dict[str, str]:
        """Obtiene información de la aplicación"""
        return {
            'name': self.settings.get('app', {}).get('name', 'Sistema de Certificados'),
            'version': self.settings.get('app', {}).get('version', '1.0.0'),
            'theme': self.get_current_theme_name(),
            'initialized': self.app_state['initialized'],
            'controllers': {
                'etl': self.is_controller_available('etl'),
                'certificates': self.is_controller_available('certificates')
            }
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Obtiene información del sistema y aplicación"""
        import platform
        import sys
        
        return {
            'sistema': {
                'plataforma': platform.platform(),
                'python_version': sys.version,
                'directorio_aplicacion': str(AppPaths.get_base_path())
            },
            'aplicacion': self.get_app_info(),
            'estado': self.get_full_app_state(),
            'rutas': {
                'datos': str(AppPaths.get_data_dir()),
                'raw': str(AppPaths.get_raw_dir()),
                'clean': str(AppPaths.get_clean_dir()),
                'output': str(AppPaths.get_output_dir()),
                'logs': str(Path("logs").absolute())
            }
        }
    
    def cleanup(self):
        """Limpieza antes de cerrar la aplicación"""
        try:
            self.save_settings()
            # Limpiar logs antiguos (mantener solo 7 días)
            if hasattr(self.logger, 'cleanup_old_logs'):
                self.logger.cleanup_old_logs(days_to_keep=7)
            self.log_info("✅ AppController: Limpieza completada")
        except Exception as e:
            error_msg = "Error durante limpieza"
            if self.logger:
                self.log_error(error_msg, e)
            else:
                print(f"❌ {error_msg}: {e}")