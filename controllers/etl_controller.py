# controllers/etl_controller.py
"""
Controlador ETL - Orquestador delgado para procesamiento de datos
Maneja la comunicación entre UI y servicios ETL
CON LOGGING MODULAR IMPLEMENTADO
"""

import warnings
from typing import Callable, Tuple, Dict

# Suprimir warnings de openpyxl
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

# Importar servicios ETL
from core.etl.etl_service import ETLService
from core.utils.logger import get_controller_logger


class ETLController:
    """
    Controlador delgado para operaciones ETL
    
    Responsabilidades:
    - Comunicación entre UI y servicios ETL
    - Gestión de callbacks de progreso
    - Orquestación básica del flujo
    - Logging modular específico
    """
    
    def __init__(self):
        """Inicializa el controlador ETL"""
        self.etl_service = ETLService()
        self.progress_callback = None
        # NUEVO: Logger modular
        self.logger = get_controller_logger("ETLController")
        self.logger.info("✅ ETLController inicializado")
    
    def set_progress_callback(self, callback: Callable[[int, str], None]):
        """
        Configura el callback para reportar progreso
        
        Args:
            callback: Función que recibe (porcentaje, mensaje)
        """
        self.progress_callback = callback
        self.etl_service.set_progress_callback(callback)
        self.logger.info("📞 Callback de progreso configurado")
    
    def procesar_completo(self, ruta_archivo_raw: str) -> Tuple[bool, str, Dict]:
        """
        Ejecuta el pipeline completo de procesamiento ETL
        
        Args:
            ruta_archivo_raw: Ruta al archivo Excel de entrada
            
        Returns:
            Tupla (éxito, mensaje, estadísticas)
        """
        try:
            self.logger.info(f"🚀 Iniciando procesamiento ETL: {ruta_archivo_raw}")
            
            # Delegar todo el procesamiento al servicio ETL
            resultado = self.etl_service.procesar_completo(ruta_archivo_raw)
            
            éxito, mensaje, estadísticas = resultado
            
            if éxito:
                self.logger.info(f"✅ Procesamiento ETL completado: {mensaje}")
                self.logger.info(f"📊 Estadísticas: {estadísticas}")
            else:
                self.logger.error(f"❌ Procesamiento ETL falló: {mensaje}")
            
            return resultado
            
        except Exception as e:
            mensaje_error = f"Error en controlador ETL: {str(e)}"
            self.logger.error(mensaje_error, exception=e)
            
            if self.progress_callback:
                self.progress_callback(0, f"❌ {mensaje_error}")
            return False, mensaje_error, {}