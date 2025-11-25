"""
Controlador del módulo de certificados.
Orquesta la interacción entre UI y core services con threading.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd
from PyQt5.QtCore import QObject, pyqtSignal, QThread

# Importar core services
from core.certificates.data_filter import CertificateDataFilter
from core.certificates.validator import CertificateValidator
from core.certificates.batch_processor import CertificateBatchProcessor

# Importar utils existentes
from core.utils.logger import get_controller_logger
from core.utils.file_utils import FileUtils

class CertificateWorker(QThread):
    """Worker thread para ejecutar generación sin bloquear UI"""
    
    # Signals
    progress = pyqtSignal(int, str, float)  # (porcentaje, mensaje, tiempo_restante)
    finished = pyqtSignal(dict)  # Resultados finales
    error = pyqtSignal(str)  # Mensaje de error
    
    def __init__(self,
                 df: pd.DataFrame,
                 template_path: str,
                 output_folder: str,
                 options: dict):
        """
        Inicializa el worker.
        
        Args:
            df: DataFrame con datos filtrados
            template_path: Ruta de la plantilla Word
            output_folder: Carpeta base de salida
            options: Opciones de procesamiento
        """
        super().__init__()
        self.df = df
        self.template_path = template_path
        self.output_folder = output_folder
        self.options = options
        self.logger = get_controller_logger("CertificateWorker")
    
    def run(self):
        """Ejecuta el proceso en background"""
        try:
            self.logger.info("Iniciando proceso de generación de certificados")
            self.logger.info(f"Registros a procesar: {len(self.df)}")
            self.logger.info(f"Opciones: {self.options}")
            
            # Crear procesador batch
            processor = CertificateBatchProcessor(
                template_path=self.template_path,
                output_base_folder=self.output_folder
            )
            
            # Callback para progreso
            def progress_callback(percent, message, tiempo_restante=0):
                self.progress.emit(percent, message, tiempo_restante)
                self.logger.info(f"Progreso {percent}%: {message}")
            
            # Ejecutar proceso
            results = processor.process(
                self.df,
                self.options,
                progress_callback=progress_callback
            )
            
            self.logger.info("Proceso completado")
            self.logger.info(f"Exitoso: {results['success']}")
            
            # === USAR TIEMPO FORMATEADO DEL BATCH PROCESSOR ===
            tiempo_formateado = results.get('total_time_formatted', '00:00')
            self.logger.info(f"Tiempo total: {tiempo_formateado}")
            
            # Emitir resultados
            self.finished.emit(results)
            
        except Exception as e:
            error_msg = f"Error en worker: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error.emit(error_msg)

class CertificatesController(QObject):
    """Controlador para el módulo de certificados"""
    
    # === SIGNALS ===
    # Emitidos hacia la UI
    combo_dni_updated = pyqtSignal(list)  # Lista de DNIs
    combo_cliente_updated = pyqtSignal(list)  # Lista de clientes
    combo_mes_updated = pyqtSignal(list)  # Lista de meses
    filter_applied = pyqtSignal(int)  # Cantidad de registros filtrados
    progress_updated = pyqtSignal(int, str, float)  # (porcentaje, mensaje, tiempo_restante)
    generation_completed = pyqtSignal(dict)  # Resultados finales
    error_occurred = pyqtSignal(str)  # Mensaje de error
    file_loaded = pyqtSignal(int, str)  # (cantidad_registros, ruta_archivo)
    
    def __init__(self):
        """Inicializa el controlador"""
        super().__init__()
        
        # Estado del controlador
        self.df_original = None
        self.df_filtered = None
        self.template_path = None
        self.output_folder = None
        self.filter_criteria = {
            'dni': None,
            'cliente': None,
            'mes': None
        }
        
        # Core services
        self.data_filter = CertificateDataFilter()
        
        # Worker thread
        self.worker = None
        
        # Logger modular
        self.logger = get_controller_logger("CertificatesController")
        self.logger.info("=" * 60)
        self.logger.info("CertificatesController inicializado")
        self.logger.info("=" * 60)
    
    # === MÉTODOS PARA CARGA ===
    
    def load_clean_file(self, file_path: str) -> None:
        """
        Carga archivo limpio y emite signal para combo DNI.
        
        Args:
            file_path: Ruta del archivo Excel limpio
        """
        try:
            self.logger.info(f"Cargando archivo limpio: {file_path}")
            
            # Validar que sea un Excel válido
            if not FileUtils.is_valid_excel_file(file_path):
                error_msg = "Archivo no válido. Debe ser .xlsx o .xls"
                self.logger.error(error_msg)
                self.error_occurred.emit(error_msg)
                return
            
            # Cargar datos
            self.df_original = self.data_filter.load_clean_data(file_path)
            self.df_filtered = None  # Reset filtro
            
            # Log de información
            file_size = FileUtils.get_file_size_readable(file_path)
            self.logger.info(f"Archivo cargado exitosamente")
            self.logger.info(f"Registros: {len(self.df_original)}")
            self.logger.info(f"Tamaño: {file_size}")
            self.logger.info(f"Columnas: {', '.join(self.df_original.columns)}")
            
            # Obtener DNIs únicos
            dnis = self.data_filter.get_unique_dnis(self.df_original)
            self.logger.info(f"DNIs únicos encontrados: {len(dnis) - 1}")  # -1 por "TODOS"
            
            # Emitir signal
            self.combo_dni_updated.emit(dnis)
            self.file_loaded.emit(len(self.df_original), file_path)
            
            # Reset filtros
            self._reset_filter_criteria()
            
        except Exception as e:
            error_msg = f"Error al cargar archivo: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit(error_msg)
    
    # === MÉTODOS PARA FILTROS (CASCADA) ===
    
    def on_dni_changed(self, dni: str) -> None:
        """
        Actualiza combo Cliente según DNI seleccionado.
        
        Args:
            dni: DNI seleccionado
        """
        if self.df_original is None:
            return
        
        try:
            self.logger.info(f"DNI cambiado: {dni}")
            self.filter_criteria['dni'] = dni
            
            # Obtener clientes únicos según DNI
            clientes = self.data_filter.get_unique_clients(
                self.df_original,
                dni_filter=dni
            )
            
            self.logger.info(f"Clientes disponibles: {len(clientes) - 1}")
            
            # Emitir signal
            self.combo_cliente_updated.emit(clientes)
            
            # Reset mes cuando cambia DNI
            self.filter_criteria['mes'] = None
            self.combo_mes_updated.emit(["TODOS"])
            
        except Exception as e:
            error_msg = f"Error al actualizar clientes: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit(error_msg)
    
    def on_cliente_changed(self, dni: str, cliente: str) -> None:
        """
        Actualiza combo Mes según DNI y Cliente.
        
        Args:
            dni: DNI seleccionado
            cliente: Cliente seleccionado
        """
        if self.df_original is None:
            return
        
        try:
            self.logger.info(f"Cliente cambiado: {cliente}")
            self.filter_criteria['cliente'] = cliente
            
            # Obtener meses únicos según DNI y Cliente
            meses = self.data_filter.get_unique_months(
                self.df_original,
                dni_filter=dni,
                client_filter=cliente
            )
            
            self.logger.info(f"Meses disponibles: {len(meses) - 1}")
            
            # Emitir signal
            self.combo_mes_updated.emit(meses)
            
        except Exception as e:
            error_msg = f"Error al actualizar meses: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit(error_msg)
    
    def apply_filter(self, dni: str, cliente: str, mes: str) -> None:
        """
        Aplica filtro y emite cantidad de registros.
        
        Args:
            dni: DNI seleccionado
            cliente: Cliente seleccionado
            mes: Mes seleccionado
        """
        if self.df_original is None:
            return
        
        try:
            self.logger.info("Aplicando filtro...")
            self.logger.info(f"  DNI: {dni}")
            self.logger.info(f"  Cliente: {cliente}")
            self.logger.info(f"  Mes: {mes}")
            
            # Actualizar criterios
            self.filter_criteria['dni'] = dni
            self.filter_criteria['cliente'] = cliente
            self.filter_criteria['mes'] = mes
            
            # Aplicar filtro
            self.df_filtered = self.data_filter.apply_filter(
                self.df_original,
                dni=dni,
                cliente=cliente,
                mes=mes
            )
            
            # Generar resumen
            summary = self.data_filter.get_filter_summary(
                self.df_original,
                self.df_filtered,
                dni=dni,
                cliente=cliente,
                mes=mes
            )
            
            self.logger.info(f"Filtro aplicado:")
            self.logger.info(f"  Total original: {summary['total_original']}")
            self.logger.info(f"  Total filtrado: {summary['total_filtrado']}")
            self.logger.info(f"  Porcentaje: {summary['porcentaje']}%")
            
            # Emitir signal
            self.filter_applied.emit(len(self.df_filtered))
            
        except Exception as e:
            error_msg = f"Error al aplicar filtro: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit(error_msg)
    
    def _reset_filter_criteria(self):
        """Resetea los criterios de filtrado"""
        self.filter_criteria = {
            'dni': None,
            'cliente': None,
            'mes': None
        }
        self.df_filtered = None
    
    # === MÉTODOS PARA GENERACIÓN ===
    
    def set_template_path(self, path: str) -> None:
        """
        Establece ruta de plantilla.
        
        Args:
            path: Ruta de la plantilla Word
            
        """
        try:
            self.logger.info(f"Validando plantilla: {path}")
            
            # Validar con CertificateValidator
            success, msg = CertificateValidator.validate_template_exists(path)
            
            if success:
                self.template_path = path
                file_size = FileUtils.get_file_size_readable(path)
                self.logger.info(f"Plantilla válida establecida ({file_size})")

            else:
                self.logger.error(f"Plantilla inválida: {msg}")

                return False
                
        except Exception as e:
            error_msg = f"Error al establecer plantilla: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit(error_msg)
            return False
    
    def set_output_folder(self, path: str) -> None:
        """
        Establece carpeta de salida.
        
        Args:
            path: Ruta de la carpeta de salida
            
        """
        try:
            self.logger.info(f"Validando carpeta de salida: {path}")
            
            # Asegurar que existe
            if FileUtils.ensure_dir(path):
                self.output_folder = path
                self.logger.info(f"Carpeta de salida establecida: {path}")

            else:
                error_msg = "No se pudo crear/acceder a la carpeta de salida"
                self.logger.error(error_msg)

                return False
                
        except Exception as e:
            error_msg = f"Error al establecer carpeta: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit(error_msg)
            return False
    
    def start_generation(self, options: dict) -> None:
        """
        Inicia generación en thread separado.
        
        Args:
            options: Opciones de generación {generate_word, convert_pdf, cleanup_word}
        """
        try:
            # Validaciones previas
            if not self._validate_before_generation():
                return
            
            # Determinar qué DataFrame usar
            df_to_use = self.df_filtered if self.df_filtered is not None else self.df_original
            
            self.logger.info("=" * 60)
            self.logger.info("INICIANDO GENERACIÓN DE CERTIFICADOS")
            self.logger.info("=" * 60)
            self.logger.info(f"Registros a procesar: {len(df_to_use)}")
            self.logger.info(f"Plantilla: {os.path.basename(self.template_path)}")
            self.logger.info(f"Carpeta salida: {self.output_folder}")
            self.logger.info(f"Opciones: {options}")
            
            # Crear worker
            self.worker = CertificateWorker(
                df=df_to_use,
                template_path=self.template_path,
                output_folder=self.output_folder,
                options=options
            )
            
            # Conectar signals
            self.worker.progress.connect(self._on_worker_progress)
            self.worker.finished.connect(self._on_worker_finished)
            self.worker.error.connect(self._on_worker_error)
            
            # Iniciar worker
            self.worker.start()
            
        except Exception as e:
            error_msg = f"Error al iniciar generación: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit(error_msg)
    
    def _validate_before_generation(self) -> bool:
        """
        Valida que todo esté configurado antes de generar.
        
        Returns:
            True si todo está OK, False en caso contrario
        """
        # Validar que haya datos
        if self.df_original is None:
            error_msg = "No hay datos cargados"
            self.logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False
        
        # Validar plantilla
        if not self.template_path:
            error_msg = "No se ha seleccionado plantilla"
            self.logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False
        
        # Validar carpeta de salida
        if not self.output_folder:
            error_msg = "No se ha seleccionado carpeta de salida"
            self.logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False
        
        return True
    
    # === MÉTODOS INTERNOS (CALLBACKS DEL WORKER) ===
    
    def _on_worker_progress(self, percent: int, message: str, tiempo_restante: float = 0) -> None:
        """
        Recibe progreso del worker y reemite a UI.
        
        Args:
            percent: Porcentaje de progreso (0-100)
            message: Mensaje descriptivo
            tiempo_restante: Segundos restantes estimados
        """
        self.progress_updated.emit(percent, message, tiempo_restante)
    
    def _on_worker_finished(self, results: dict) -> None:
        """
        Recibe resultados finales del worker.
        
        Args:
            results: Diccionario con resultados del proceso
        """
        self.logger.info("=" * 60)
        self.logger.info("GENERACIÓN FINALIZADA")
        self.logger.info("=" * 60)
        self.logger.info(f"Exitoso: {results['success']}")
        
        # === USAR TIEMPO FORMATEADO DEL BATCH PROCESSOR ===
        tiempo_formateado = results.get('total_time_formatted', '00:00')
        self.logger.info(f"Tiempo total: {tiempo_formateado}")
        
        if results['word_results']:
            self.logger.info(f"Word - Exitosos: {results['word_results']['exitosos']}")
            self.logger.info(f"Word - Fallidos: {results['word_results']['fallidos']}")
        
        if results['pdf_results']:
            self.logger.info(f"PDF - Exitosos: {results['pdf_results']['exitosos']}")
            self.logger.info(f"PDF - Fallidos: {results['pdf_results']['fallidos']}")
        
        # Emitir signal (los resultados ya incluyen el tiempo formateado)
        self.generation_completed.emit(results)
        
        # Limpiar worker
        self.worker = None
    
    def _on_worker_error(self, error_msg: str) -> None:
        """
        Maneja errores del worker.
        
        Args:
            error_msg: Mensaje de error
        """
        self.logger.error(f"Error en worker: {error_msg}")
        self.error_occurred.emit(error_msg)
        
        # Limpiar worker
        self.worker = None
    
    # === MÉTODOS AUXILIARES ===
    
    def get_current_state(self) -> Dict[str, Any]:
        """
        Retorna estado actual del controlador.
        
        Returns:
            Diccionario con el estado actual
        """
        return {
            'has_data': self.df_original is not None,
            'total_records': len(self.df_original) if self.df_original is not None else 0,
            'filtered_records': len(self.df_filtered) if self.df_filtered is not None else 0,
            'has_filter': self.df_filtered is not None,
            'filter_criteria': self.filter_criteria.copy(),
            'has_template': self.template_path is not None,
            'has_output_folder': self.output_folder is not None,
            'ready_to_generate': self._validate_before_generation()
        }
    
    def export_filtered_data(self, output_path: str) -> bool:
        """
        Exporta datos filtrados a Excel.
        
        Args:
            output_path: Ruta de salida
            
        Returns:
            True si se exportó correctamente
        """
        try:
            if self.df_filtered is None:
                error_msg = "No hay datos filtrados para exportar"
                self.logger.error(error_msg)
                self.error_occurred.emit(error_msg)
                return False
            
            self.logger.info(f"Exportando datos filtrados: {output_path}")
            
            success = self.data_filter.export_filtered(self.df_filtered, output_path)
            
            if success:
                file_size = FileUtils.get_file_size_readable(output_path)
                self.logger.info(f"Datos exportados exitosamente ({file_size})")
                return True
            else:
                error_msg = "Error al exportar datos"
                self.logger.error(error_msg)
                self.error_occurred.emit(error_msg)
                return False
                
        except Exception as e:
            error_msg = f"Error al exportar: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit(error_msg)
            return False