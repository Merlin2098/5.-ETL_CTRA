# core/utils/logger.py
"""
Sistema de logging centralizado para la aplicación
Maneja logs tanto en archivo como en consola
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class AppLogger:
    """
    Logger centralizado de la aplicación - MANTENIDO PARA COMPATIBILIDAD
    
    Características:
    - Logs en archivo (rotación diaria)
    - Logs en consola
    - Formato consistente
    - Niveles de log configurables
    """
    
    def __init__(self, log_dir: str = "logs", app_name: str = "SistemaCertificados"):
        """
        Inicializa el sistema de logging
        
        Args:
            log_dir: Directorio donde guardar los logs
            app_name: Nombre de la aplicación para el log
        """
        self.log_dir = Path(log_dir)
        self.app_name = app_name
        self.logger = None
        self.setup_logging()
    
    def setup_logging(self) -> bool:
        """
        Configura el sistema de logging
        """
        try:
            print(f"🔧 [AppLogger] Iniciando setup_logging para: {self.app_name}")
            
            # Crear directorio de logs si no existe
            self.log_dir.mkdir(parents=True, exist_ok=True)
            print(f"🔧 [AppLogger] Directorio logs: {self.log_dir.absolute()}")
            
            # Configurar el logger principal
            self.logger = logging.getLogger(self.app_name)
            self.logger.setLevel(logging.INFO)
            
            # Evitar que se propague al logger root
            self.logger.propagate = False
            
            # Limpiar handlers existentes
            self.logger.handlers.clear()
            print(f"🔧 [AppLogger] Logger creado: {self.logger}")
            
            # Formato consistente para todos los logs
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            # Handler para archivo (con rotación diaria)
            log_file = self.log_dir / f"{self.app_name}_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            print(f"🔧 [AppLogger] FileHandler creado: {log_file}")
            
            # Handler para consola - CORREGIDO
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            print(f"🔧 [AppLogger] ConsoleHandler creado")
            
            # Agregar handlers al logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
            print(f"🔧 [AppLogger] Handlers agregados. Total: {len(self.logger.handlers)}")
            
            # Test directo
            self.logger.info("🔧 [AppLogger] TEST: Logging inicializado correctamente")
            self.logger.info(f"🔧 [AppLogger] Logs guardados en: {log_file.absolute()}")
            
            print(f"🔧 [AppLogger] Setup completado exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ [AppLogger] ERROR en setup: {e}")
            import traceback
            traceback.print_exc()
            # Fallback a logging básico
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(self.app_name)
            return False
    
    # === MÉTODOS EXISTENTES (MANTENIDOS) ===
    
    def info(self, message: str, extra_data: Optional[dict] = None):
        """
        Log de nivel INFO
        
        Args:
            message: Mensaje a loguear
            extra_data: Datos adicionales para el log
        """
        if self.logger:
            if extra_data:
                self.logger.info(f"{message} | Extra: {extra_data}")
            else:
                self.logger.info(message)
    
    def error(self, message: str, exception: Optional[Exception] = None):
        """
        Log de nivel ERROR
        
        Args:
            message: Mensaje a loguear
            exception: Excepción relacionada (opcional)
        """
        if self.logger:
            if exception:
                self.logger.error(f"{message} | Exception: {str(exception)}", exc_info=True)
            else:
                self.logger.error(message)
    
    def warning(self, message: str, extra_data: Optional[dict] = None):
        """
        Log de nivel WARNING
        
        Args:
            message: Mensaje a loguear
            extra_data: Datos adicionales para el log
        """
        if self.logger:
            if extra_data:
                self.logger.warning(f"{message} | Extra: {extra_data}")
            else:
                self.logger.warning(message)
    
    def debug(self, message: str, extra_data: Optional[dict] = None):
        """
        Log de nivel DEBUG
        
        Args:
            message: Mensaje a loguear
            extra_data: Datos adicionales para el log
        """
        if self.logger:
            if extra_data:
                self.logger.debug(f"{message} | Extra: {extra_data}")
            else:
                self.logger.debug(message)
    
    def critical(self, message: str, exception: Optional[Exception] = None):
        """
        Log de nivel CRITICAL
        
        Args:
            message: Mensaje a loguear
            exception: Excepción relacionada (opcional)
        """
        if self.logger:
            if exception:
                self.logger.critical(f"{message} | Exception: {str(exception)}", exc_info=True)
            else:
                self.logger.critical(message)
    
    def get_log_file_path(self) -> Optional[Path]:
        """
        Obtiene la ruta del archivo de log actual
        
        Returns:
            Path: Ruta del archivo de log o None si no está configurado
        """
        for handler in self.logger.handlers:
            if isinstance(handler, logging.FileHandler):
                return Path(handler.baseFilename)
        return None
    
    def cleanup_old_logs(self, days_to_keep: int = 30):
        """
        Elimina logs más antiguos que days_to_keep
        
        Args:
            days_to_keep: Número de días a mantener los logs
        """
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            for log_file in self.log_dir.glob("*.log"):
                if log_file.stat().st_mtime < cutoff_date.timestamp():
                    log_file.unlink()
                    self.info(f"🗑️ Log antiguo eliminado: {log_file.name}")
                    
        except Exception as e:
            self.error("Error limpiando logs antiguos", e)


# === NUEVO SISTEMA MODULAR (EXTENSIÓN) ===

class ControllerLogger:
    """Logger modular específico para cada controlador - NUEVO"""
    
    def __init__(self, controller_name: str, log_level=logging.INFO):
        self.controller_name = controller_name
        self.log_level = log_level
        self.logger = None
        self._setup_logger()
    
    def _setup_logger(self):
        """Configura el logger específico del controlador"""
        # Crear instancia de logger
        logger_name = f"app.{self.controller_name}"
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(self.log_level)
        
        # Evitar handlers duplicados
        if self.logger.handlers:
            return
            
        # Crear directorio de logs específico
        log_dir = self._get_log_directory()
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
        log_filename = f"{self.controller_name}_{timestamp}.log"
        log_file = log_dir / log_filename
        
        # Configurar formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para archivo
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def _get_log_directory(self) -> Path:
        """Determina el directorio de logs basado en el nombre del controlador"""
        base_log_dir = Path("logs")
        
        if "etl" in self.controller_name.lower():
            return base_log_dir / "etl"
        elif "certificat" in self.controller_name.lower():  # certificates o certificate
            return base_log_dir / "certificates"
        else:
            return base_log_dir / "app"
    
    # Métodos de logging (misma interfaz que AppLogger para compatibilidad)
    def info(self, message: str, extra_data: Optional[dict] = None):
        if extra_data:
            self.logger.info(f"{message} | Extra: {extra_data}")
        else:
            self.logger.info(message)
    
    def debug(self, message: str, extra_data: Optional[dict] = None):
        if extra_data:
            self.logger.debug(f"{message} | Extra: {extra_data}")
        else:
            self.logger.debug(message)
    
    def warning(self, message: str, extra_data: Optional[dict] = None):
        if extra_data:
            self.logger.warning(f"{message} | Extra: {extra_data}")
        else:
            self.logger.warning(message)
    
    def error(self, message: str, exception: Optional[Exception] = None):
        if exception:
            self.logger.error(f"{message} | Exception: {str(exception)}", exc_info=True)
        else:
            self.logger.error(message)
    
    def critical(self, message: str, exception: Optional[Exception] = None):
        if exception:
            self.logger.critical(f"{message} | Exception: {str(exception)}", exc_info=True)
        else:
            self.logger.critical(message)


# Funciones de utilidad para mantener compatibilidad
def setup_app_logger() -> AppLogger:
    """Función de compatibilidad - retorna AppLogger existente"""
    return AppLogger()

def get_controller_logger(controller_name: str) -> ControllerLogger:
    """Nueva función para obtener logger modular"""
    return ControllerLogger(controller_name)