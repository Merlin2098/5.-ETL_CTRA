# core/etl/etl_service.py
"""
Servicio principal ETL - Orquesta todo el proceso
"""
import pandas as pd
import time
from typing import Tuple, Dict, Optional, Callable
from datetime import datetime

from .data_loader import DataLoader
from .data_cleaner import DataCleaner
from .date_processor import DateProcessor
from .contract_splitter import ContractSplitter
from .period_consolidator import PeriodConsolidator
from .file_generator import FileGenerator

class ETLService:
    """
    Servicio principal ETL que orquesta todo el proceso
    """
    
    def __init__(self):
        """Inicializa el servicio ETL"""
        self.df = None
        self.estadisticas = {}
        self.progress_callback = None
    
    def set_progress_callback(self, callback: Callable[[int, str], None]):
        """
        Configura el callback para reportar progreso
        
        Args:
            callback: Función que recibe (porcentaje, mensaje)
        """
        self.progress_callback = callback
    
    def _report_progress(self, porcentaje: int, mensaje: str):
        """
        Reporta el progreso si hay un callback configurado
        
        Args:
            porcentaje: Porcentaje de avance (0-100)
            mensaje: Mensaje descriptivo del paso actual
        """
        if self.progress_callback:
            self.progress_callback(porcentaje, mensaje)
    
    def _formatear_tiempo(self, segundos: float) -> str:
        """Formatea tiempo en formato legible"""
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segs = int(segundos % 60)
        
        partes = []
        if horas > 0:
            partes.append(f"{horas}h")
        if minutos > 0:
            partes.append(f"{minutos}m")
        if segs > 0 or not partes:
            partes.append(f"{segs}s")
        
        return " ".join(partes)
    
    def procesar_completo(self, ruta_archivo_raw: str) -> Tuple[bool, str, Dict]:
        """
        Ejecuta el pipeline completo de procesamiento ETL
        
        Args:
            ruta_archivo_raw: Ruta al archivo Excel de entrada
            
        Returns:
            Tupla (éxito, mensaje, estadísticas)
        """
        inicio_tiempo = time.time()
        
        self._report_progress(0, "🚀 Iniciando procesamiento ETL...")
        
        try:
            # PASO 1: Carga y validación inicial
            self._report_progress(2, "📂 Cargando archivo Excel...")
            exito, mensaje, self.df = DataLoader.cargar_archivo(ruta_archivo_raw)
            if not exito:
                return False, mensaje, self.estadisticas
            self.estadisticas['registros_originales'] = len(self.df)
            
            self._report_progress(5, "🔍 Filtrando columnas necesarias...")
            exito, mensaje, self.df = DataLoader.filtrar_columnas_necesarias(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            self.estadisticas['columnas_eliminadas'] = len(self.df.columns) - len(DataLoader.COLUMNAS_REQUERIDAS)
            
            self._report_progress(9, "🔍 Validando estructura de datos...")
            exito, mensaje = DataLoader.validar_columnas(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            
            # PASO 2: Limpieza de datos
            self._report_progress(13, "🧹 Eliminando filas con datos nulos...")
            exito, mensaje, self.df = DataCleaner.eliminar_filas_nulas(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            self.estadisticas['filas_nulas_eliminadas'] = self.estadisticas['registros_originales'] - len(self.df)
            
            self._report_progress(17, "🚫 Limpiando registros anulados...")
            exito, mensaje, self.df = DataCleaner.limpiar_anulados(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            self.estadisticas['registros_anulados'] = self.estadisticas['registros_originales'] - len(self.df) - self.estadisticas['filas_nulas_eliminadas']
            
            self._report_progress(21, "🔧 Formateando columnas...")
            exito, mensaje, self.df = DataCleaner.formatear_columnas(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            
            self._report_progress(25, "📅 Detectando fechas inválidas...")
            exito, mensaje, self.df = DataCleaner.detectar_fechas_invalidas(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            self.estadisticas['fechas_invalidas'] = self.estadisticas['registros_originales'] - len(self.df) - self.estadisticas['filas_nulas_eliminadas'] - self.estadisticas['registros_anulados']
            
            self._report_progress(29, "♻️ Eliminando registros duplicados...")
            exito, mensaje, self.df = DataCleaner.eliminar_duplicados(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            self.estadisticas['duplicados_eliminados'] = self.estadisticas['registros_originales'] - len(self.df) - self.estadisticas['filas_nulas_eliminadas'] - self.estadisticas['registros_anulados'] - self.estadisticas['fechas_invalidas']
            
            # PASO 3: Procesamiento de contratos
            self._report_progress(33, "📅 Dividiendo contratos por mes...")
            exito, mensaje, self.df = ContractSplitter.dividir_contratos_por_mes(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            self.estadisticas['contratos_divididos'] = len(self.df) - (self.estadisticas['registros_originales'] - self.estadisticas['filas_nulas_eliminadas'] - self.estadisticas['registros_anulados'] - self.estadisticas['fechas_invalidas'] - self.estadisticas['duplicados_eliminados'])
            
            self._report_progress(45, "📆 Agregando MES_ANALIZADO...")
            exito, mensaje, self.df = DateProcessor.agregar_mes_analizado(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            
            # PASO 4: Consolidación y generación de certificados
            self._report_progress(55, "📋 Consolidando períodos contiguos...")
            exito, mensaje, self.df = PeriodConsolidator.consolidar_y_generar_fechas(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            self.estadisticas['certificados_generados'] = len(self.df)
            
            self._report_progress(70, "⏱️ Calculando días laborados...")
            exito, mensaje, self.df = DateProcessor.calcular_dias_laborados(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            
            self._report_progress(80, "🗓️ Agregando FECHA_GENERAR...")
            exito, mensaje, self.df = DateProcessor.agregar_fecha_generar(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            
            self._report_progress(87, "🔤 Convirtiendo fechas a texto en español...")
            exito, mensaje, self.df = DateProcessor.convertir_fechas_a_texto(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            
            # PASO 5: Guardado final
            self._report_progress(95, "💾 Guardando archivo procesado...")
            exito, mensaje, ruta_salida = FileGenerator.guardar_archivo(self.df)
            if not exito:
                return False, mensaje, self.estadisticas
            
            # Estadísticas finales
            tiempo_total = time.time() - inicio_tiempo
            self.estadisticas['archivo_salida'] = ruta_salida
            self.estadisticas['registros_finales'] = len(self.df)
            self.estadisticas['tiempo_total'] = tiempo_total
            self.estadisticas['tiempo_formateado'] = self._formatear_tiempo(tiempo_total)
            
            self._report_progress(100, "✅ Procesamiento completado exitosamente")
            
            return True, "Procesamiento completado con éxito", self.estadisticas
            
        except Exception as e:
            mensaje_error = f"Error inesperado en el procesamiento: {str(e)}"
            self._report_progress(0, f"❌ {mensaje_error}")
            return False, mensaje_error, self.estadisticas