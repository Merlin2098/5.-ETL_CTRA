"""
Controlador del módulo de certificados.
Orquesta la interacción entre UI y core services con threading.
Soporta filtros múltiples con selección en cascada.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
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
    """Controlador para el módulo de certificados con filtros múltiples"""
    
    # === SIGNALS ===
    # Emitidos hacia la UI
    list_dni_updated = pyqtSignal(list)  # Lista de DNIs disponibles
    list_cliente_updated = pyqtSignal(list)  # Lista de clientes disponibles
    list_mes_updated = pyqtSignal(list)  # Lista de meses disponibles
    
    cliente_section_enabled = pyqtSignal(bool)  # Habilitar/deshabilitar sección Cliente
    mes_section_enabled = pyqtSignal(bool)  # Habilitar/deshabilitar sección Mes
    apply_button_enabled = pyqtSignal(bool)  # Habilitar/deshabilitar botón Aplicar
    
    filter_applied = pyqtSignal(int)  # Cantidad de registros filtrados
    progress_updated = pyqtSignal(int, str, float)  # (porcentaje, mensaje, tiempo_restante)
    generation_completed = pyqtSignal(dict)  # Resultados finales
    error_occurred = pyqtSignal(str, str)  # (título, mensaje)
    file_loaded = pyqtSignal(int, str)  # (cantidad_registros, ruta_archivo)
    
    def __init__(self):
        """Inicializa el controlador"""
        super().__init__()
        
        # Estado del controlador
        self.df_original = None
        self.df_filtered = None
        self.template_path = None
        self.output_folder = None
        
        # Almacenar selecciones múltiples
        self.selected_dnis = []
        self.selected_clientes = []
        self.selected_meses = []
        
        # Core services
        self.data_filter = CertificateDataFilter()
        
        # Worker thread
        self.worker = None
        
        # Logger modular
        self.logger = get_controller_logger("CertificatesController")
        self.logger.info("=" * 60)
        self.logger.info("CertificatesController inicializado (Filtros Múltiples)")
        self.logger.info("=" * 60)
    
    # === MÉTODOS PARA CARGA ===
    
    def load_clean_file(self, file_path: str) -> None:
        """
        Carga archivo limpio y emite signal para lista DNI.
        Estado inicial: todo desmarcado, solo DNI habilitado.
        
        Args:
            file_path: Ruta del archivo Excel limpio
        """
        try:
            self.logger.info(f"Cargando archivo limpio: {file_path}")
            
            # Validar que sea un Excel válido
            if not FileUtils.is_valid_excel_file(file_path):
                error_msg = "Archivo no válido. Debe ser .xlsx o .xls"
                self.logger.error(error_msg)
                self.error_occurred.emit("Error de Archivo", error_msg)
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
            
            # Obtener DNIs únicos (sin "TODOS")
            dnis = self.data_filter.get_unique_dnis(self.df_original)
            self.logger.info(f"DNIs únicos encontrados: {len(dnis)}")
            
            # Emitir signals - Estado inicial
            self.list_dni_updated.emit(dnis)  # Poblar lista DNI
            self.list_cliente_updated.emit([])  # Cliente vacío
            self.list_mes_updated.emit([])  # Mes vacío
            
            # Deshabilitar secciones dependientes
            self.cliente_section_enabled.emit(False)
            self.mes_section_enabled.emit(False)
            self.apply_button_enabled.emit(False)
            
            self.file_loaded.emit(len(self.df_original), file_path)
            
            # Reset selecciones
            self._reset_selections()
            
        except Exception as e:
            error_msg = f"Error al cargar archivo: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit("Error de Carga", error_msg)
    
    # === MÉTODOS PARA FILTROS EN CASCADA ===
    
    def on_dni_selection_changed(self, selected_dnis: List[str]) -> None:
        """
        Actualiza lista Cliente según DNIs seleccionados.
        Se ejecuta cada vez que el usuario marca/desmarca DNIs.
        
        Args:
            selected_dnis: Lista de DNIs seleccionados
        """
        if self.df_original is None:
            return
        
        try:
            self.logger.info(f"DNIs seleccionados: {len(selected_dnis)}")
            self.selected_dnis = selected_dnis
            
            # Validar si hay al menos 1 DNI seleccionado
            if len(selected_dnis) == 0:
                # Deshabilitar todo
                self.logger.info("Sin DNIs seleccionados - Deshabilitando cascada")
                self.list_cliente_updated.emit([])
                self.list_mes_updated.emit([])
                self.cliente_section_enabled.emit(False)
                self.mes_section_enabled.emit(False)
                self.apply_button_enabled.emit(False)
                
                # Reset selecciones dependientes
                self.selected_clientes = []
                self.selected_meses = []
                return
            
            # Obtener clientes únicos según DNIs seleccionados
            clientes = self.data_filter.get_unique_clients(
                self.df_original,
                dni_filters=selected_dnis
            )
            
            self.logger.info(f"Clientes disponibles: {len(clientes)}")
            
            # Emitir signal para actualizar lista Cliente
            self.list_cliente_updated.emit(clientes)
            self.cliente_section_enabled.emit(True)  # Habilitar sección Cliente
            
            # Reset Mes (debe elegir clientes primero)
            self.list_mes_updated.emit([])
            self.mes_section_enabled.emit(False)
            self.apply_button_enabled.emit(False)
            
            self.selected_clientes = []
            self.selected_meses = []
            
        except Exception as e:
            error_msg = f"Error al actualizar clientes: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit("Error de Filtro", error_msg)
    
    def on_cliente_selection_changed(self, selected_clientes: List[str]) -> None:
        """
        Actualiza lista Mes según Clientes seleccionados.
        
        Args:
            selected_clientes: Lista de Clientes seleccionados
        """
        if self.df_original is None or len(self.selected_dnis) == 0:
            return
        
        try:
            self.logger.info(f"Clientes seleccionados: {len(selected_clientes)}")
            self.selected_clientes = selected_clientes
            
            # Validar si hay al menos 1 Cliente seleccionado
            if len(selected_clientes) == 0:
                self.logger.info("Sin Clientes seleccionados - Deshabilitando Mes")
                self.list_mes_updated.emit([])
                self.mes_section_enabled.emit(False)
                self.apply_button_enabled.emit(False)
                
                self.selected_meses = []
                return
            
            # Obtener meses únicos según DNIs + Clientes seleccionados
            meses = self.data_filter.get_unique_months(
                self.df_original,
                dni_filters=self.selected_dnis,
                client_filters=selected_clientes
            )
            
            self.logger.info(f"Meses disponibles: {len(meses)}")
            
            # Emitir signal para actualizar lista Mes
            self.list_mes_updated.emit(meses)
            self.mes_section_enabled.emit(True)  # Habilitar sección Mes
            
            # Botón Aplicar sigue deshabilitado hasta que seleccione meses
            self.apply_button_enabled.emit(False)
            self.selected_meses = []
            
        except Exception as e:
            error_msg = f"Error al actualizar meses: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit("Error de Filtro", error_msg)
    
    def on_mes_selection_changed(self, selected_meses: List[str]) -> None:
        """
        Valida selección de Meses y habilita/deshabilita botón Aplicar.
        
        Args:
            selected_meses: Lista de Meses seleccionados
        """
        if self.df_original is None:
            return
        
        try:
            self.logger.info(f"Meses seleccionados: {len(selected_meses)}")
            self.selected_meses = selected_meses
            
            # Validar si hay al menos 1 Mes seleccionado
            if len(selected_meses) == 0:
                self.logger.info("Sin Meses seleccionados - Deshabilitando Aplicar")
                self.apply_button_enabled.emit(False)
                return
            
            # Validación completa: DNI, Cliente, Mes con selecciones
            if (len(self.selected_dnis) > 0 and 
                len(self.selected_clientes) > 0 and 
                len(self.selected_meses) > 0):
                
                self.logger.info("Todos los filtros tienen selecciones - Habilitando Aplicar")
                self.apply_button_enabled.emit(True)
            else:
                self.apply_button_enabled.emit(False)
            
        except Exception as e:
            error_msg = f"Error al validar meses: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit("Error de Validación", error_msg)
    
    def apply_filters(self) -> None:
        """
        Aplica los filtros combinados y emite signal con cantidad de registros.
        Solo se ejecuta cuando el usuario presiona "Aplicar Filtros".
        """
        if self.df_original is None:
            return
        
        try:
            self.logger.info("=" * 60)
            self.logger.info("APLICANDO FILTROS COMBINADOS")
            self.logger.info("=" * 60)
            self.logger.info(f"DNIs: {len(self.selected_dnis)} seleccionados")
            self.logger.info(f"Clientes: {len(self.selected_clientes)} seleccionados")
            self.logger.info(f"Meses: {len(self.selected_meses)} seleccionados")
            
            # Aplicar filtro con listas
            self.df_filtered = self.data_filter.apply_filter(
                self.df_original,
                dnis=self.selected_dnis,
                clientes=self.selected_clientes,
                meses=self.selected_meses
            )
            
            # Obtener resumen
            summary = self.data_filter.get_filter_summary(
                self.df_original,
                self.df_filtered,
                dnis=self.selected_dnis,
                clientes=self.selected_clientes,
                meses=self.selected_meses
            )
            
            self.logger.info(f"Registros filtrados: {len(self.df_filtered)}")
            self.logger.info(f"Porcentaje: {summary['porcentaje']}%")
            
            # Emitir signal
            self.filter_applied.emit(len(self.df_filtered))
            
        except Exception as e:
            error_msg = f"Error al aplicar filtros: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit("Error de Filtro", error_msg)
    
    def clear_filters(self) -> None:
        """
        Limpia todos los filtros y resetea al estado inicial.
        Botón "Limpiar Filtros".
        """
        try:
            self.logger.info("Limpiando todos los filtros")
            
            # Reset estado
            self._reset_selections()
            self.df_filtered = None
            
            # Obtener DNIs nuevamente
            if self.df_original is not None:
                dnis = self.data_filter.get_unique_dnis(self.df_original)
                
                # Emitir signals - Estado inicial
                self.list_dni_updated.emit(dnis)
                self.list_cliente_updated.emit([])
                self.list_mes_updated.emit([])
                
                # Deshabilitar todo excepto DNI
                self.cliente_section_enabled.emit(False)
                self.mes_section_enabled.emit(False)
                self.apply_button_enabled.emit(False)
            
            self.logger.info("Filtros limpiados exitosamente")
            
        except Exception as e:
            error_msg = f"Error al limpiar filtros: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit("Error", error_msg)
    
    def _reset_selections(self) -> None:
        """Resetea todas las selecciones a listas vacías"""
        self.selected_dnis = []
        self.selected_clientes = []
        self.selected_meses = []
    
    # === MÉTODOS PARA PLANTILLA Y SALIDA ===
    
    def set_template(self, path: str) -> None:
        """
        Establece plantilla Word.
        
        Args:
            path: Ruta de la plantilla
        """
        try:
            self.logger.info(f"Validando plantilla: {path}")
            
            # Validar existencia
            if not os.path.exists(path):
                error_msg = "La plantilla no existe"
                self.logger.error(error_msg)
                self.error_occurred.emit("Error de Plantilla", error_msg)
                return False
            
            # Validar extensión
            if not path.lower().endswith('.docx'):
                error_msg = "La plantilla debe ser .docx"
                self.logger.error(error_msg)
                self.error_occurred.emit("Error de Plantilla", error_msg)
                return False
            
            self.template_path = path
            self.logger.info(f"Plantilla establecida: {os.path.basename(path)}")
            return True
            
        except Exception as e:
            error_msg = f"Error al establecer plantilla: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit("Error de Plantilla", error_msg)
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
                return True
            else:
                error_msg = "No se pudo crear/acceder a la carpeta de salida"
                self.logger.error(error_msg)
                self.error_occurred.emit("Error de Carpeta", error_msg)
                return False
                
        except Exception as e:
            error_msg = f"Error al establecer carpeta: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit("Error de Carpeta", error_msg)
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
            self.error_occurred.emit("Error de Generación", error_msg)
    
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
            self.error_occurred.emit("Error de Validación", error_msg)
            return False
        
        # Validar plantilla
        if not self.template_path:
            error_msg = "No se ha seleccionado plantilla"
            self.logger.error(error_msg)
            self.error_occurred.emit("Error de Validación", error_msg)
            return False
        
        # Validar carpeta de salida
        if not self.output_folder:
            error_msg = "No se ha seleccionado carpeta de salida"
            self.logger.error(error_msg)
            self.error_occurred.emit("Error de Validación", error_msg)
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
        self.error_occurred.emit("Error de Worker", error_msg)
        
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
            'selected_dnis': len(self.selected_dnis),
            'selected_clientes': len(self.selected_clientes),
            'selected_meses': len(self.selected_meses),
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
                self.error_occurred.emit("Error de Exportación", error_msg)
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
                self.error_occurred.emit("Error de Exportación", error_msg)
                return False
                
        except Exception as e:
            error_msg = f"Error al exportar: {str(e)}"
            self.logger.error(error_msg, exception=e)
            self.error_occurred.emit("Error de Exportación", error_msg)
            return False