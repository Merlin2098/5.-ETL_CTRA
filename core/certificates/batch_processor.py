"""
Módulo orquestador del proceso completo de generación de certificados.
Coordina generación Word, conversión PDF y generación de reportes.
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Callable
import pandas as pd


class CertificateBatchProcessor:
    """Orquestador del proceso completo de generación de certificados"""
    
    def __init__(self,
                 template_path: str,
                 output_base_folder: str):
        """
        Inicializa el procesador batch.
        
        Args:
            template_path: Ruta a la plantilla Word
            output_base_folder: Carpeta base de salida
        """
        self.template_path = template_path
        self.output_base_folder = output_base_folder
        
        # Carpetas de salida (se crearán automáticamente)
        self.word_folder = None
        self.pdf_folder = None
        self.output_folder = None
        
        # Timestamp para esta ejecución
        self.timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
        
        # Variables para tracking de tiempo
        self.start_time = None
        self.items_procesados = 0
        self.total_items = 0
        
        # Crear estructura de carpetas
        self._create_output_structure()
    
    def _create_output_structure(self) -> None:
        """Crea estructura de carpetas con timestamp"""
        # Crear carpeta principal con timestamp
        self.output_folder = os.path.join(
            self.output_base_folder,
            f"certificates_{self.timestamp}"
        )
        
        # Subcarpetas
        self.word_folder = os.path.join(self.output_folder, "word")
        self.pdf_folder = os.path.join(self.output_folder, "pdf")
        
        # Crear todas las carpetas
        os.makedirs(self.word_folder, exist_ok=True)
        os.makedirs(self.pdf_folder, exist_ok=True)
    
    def _format_time(self, total_seconds: float) -> str:
        """
        Convierte segundos a formato horas:minutos:segundos.
        
        Args:
            total_seconds: Tiempo total en segundos
            
        Returns:
            String formateado como HH:MM:SS o MM:SS
        """
        total_seconds = int(total_seconds)  # Redondear a segundos enteros
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def _calculate_tiempo_restante(self, items_procesados: int, total_items: int) -> float:
        """
        Calcula el tiempo restante estimado.
        
        Args:
            items_procesados: Número de ítems procesados
            total_items: Total de ítems a procesar
            
        Returns:
            Segundos restantes estimados
        """
        if items_procesados == 0 or self.start_time is None:
            return 0
        
        tiempo_transcurrido = time.time() - self.start_time
        tiempo_por_item = tiempo_transcurrido / items_procesados
        items_restantes = total_items - items_procesados
        
        return tiempo_por_item * items_restantes
    
    def process(self,
                df_filtered: pd.DataFrame,
                options: dict,
                progress_callback: Optional[Callable[[int, str, float], None]] = None
                ) -> Dict[str, Any]:
        """
        Ejecuta el proceso completo de generación.
        
        Args:
            df_filtered: DataFrame con datos filtrados
            options: Opciones de procesamiento:
                {
                    'generate_word': bool,
                    'convert_pdf': bool,
                    'cleanup_word': bool,
                    'batch_size': int
                }
            progress_callback: Función callback(porcentaje, mensaje, tiempo_restante)
            
        Returns:
            Diccionario con resultados completos
        """
        start_time = time.time()
        
        # Inicializar tracking de tiempo
        self.start_time = start_time
        self.total_items = len(df_filtered)
        self.items_procesados = 0
        
        # Validar opciones
        options = self._validate_options(options)
        
        # Resultado global
        results = {
            'success': False,
            'timestamp': self.timestamp,
            'output_folder': self.output_folder,
            'word_folder': self.word_folder,
            'pdf_folder': self.pdf_folder,
            'input_records': len(df_filtered),
            'word_results': None,
            'pdf_results': None,
            'total_time': 0,
            'total_time_formatted': '00:00',
            'errors': []
        }
        
        try:
            # FASE 1: VALIDACIONES PREVIAS
            if progress_callback:
                progress_callback(0, "Validando datos y configuración...", 0)
            
            validation_ok, validation_msg = self._validate_inputs(df_filtered)
            if not validation_ok:
                results['errors'].append(validation_msg)
                return results
            
            # FASE 2: GENERACIÓN WORD
            if options['generate_word']:
                if progress_callback:
                    progress_callback(5, "Iniciando generación de certificados Word...", 0)
                
                word_results = self._generate_word_certificates(
                    df_filtered,
                    progress_callback
                )
                
                results['word_results'] = word_results
                
                if word_results['exitosos'] == 0:
                    results['errors'].append("No se generó ningún certificado Word")
                    return results
            
            # FASE 3: CONVERSIÓN PDF
            if options['convert_pdf']:
                if progress_callback:
                    progress_callback(55, "Iniciando conversión a PDF...", 0)
                
                pdf_results = self._convert_to_pdf(
                    progress_callback
                )
                
                results['pdf_results'] = pdf_results
            
            # FASE 4: LIMPIEZA (OPCIONAL)
            if options['cleanup_word'] and options['convert_pdf']:
                if progress_callback:
                    progress_callback(95, "Limpiando archivos Word temporales...", 0)
                
                self._cleanup_word_files()
            
            # FASE 5: REPORTE FINAL
            if progress_callback:
                progress_callback(98, "Generando reporte final...", 0)
            
            self._generate_report_json(results, options)
            
            # Marcar como exitoso
            results['success'] = True
            
            # Tiempo total - CONVERSIÓN A FORMATO HORAS:MINUTOS:SEGUNDOS
            total_seconds = time.time() - start_time
            results['total_time'] = round(total_seconds, 2)
            results['total_time_formatted'] = self._format_time(total_seconds)
            
            if progress_callback:
                progress_callback(100, "¡Proceso completado exitosamente!", 0)
            
        except Exception as e:
            # En caso de error, también formatear el tiempo transcurrido
            total_seconds = time.time() - start_time
            results['total_time'] = round(total_seconds, 2)
            results['total_time_formatted'] = self._format_time(total_seconds)
            results['errors'].append(f"Error en proceso: {str(e)}")
            if progress_callback:
                progress_callback(100, f"Error: {str(e)}", 0)
        
        return results
    
    def _validate_options(self, options: dict) -> dict:
        """Valida y completa opciones con valores por defecto"""
        default_options = {
            'generate_word': True,
            'convert_pdf': True,
            'cleanup_word': False,
            'batch_size': 100
        }
        
        # Combinar con opciones provistas
        final_options = default_options.copy()
        final_options.update(options)
        
        return final_options
    
    def _validate_inputs(self, df: pd.DataFrame) -> tuple:
        """
        Valida inputs antes de procesar.
        
        Returns:
            Tupla (éxito, mensaje)
        """
        # Importar validadores
        from core.certificates.validator import CertificateValidator
        
        # Validar plantilla
        success, msg = CertificateValidator.validate_template_exists(self.template_path)
        if not success:
            return False, f"Plantilla inválida: {msg}"
        
        # Validar DataFrame
        success, msg = CertificateValidator.validate_dataframe(df)
        if not success:
            return False, f"DataFrame inválido: {msg}"
        
        # Validar carpeta de salida
        success, msg = CertificateValidator.validate_output_folder(self.output_folder)
        if not success:
            return False, f"Carpeta de salida inválida: {msg}"
        
        return True, ""
    
    def _generate_word_certificates(self,
                                    df: pd.DataFrame,
                                    main_callback: Optional[Callable] = None
                                    ) -> Dict[str, Any]:
        """Genera certificados Word"""
        from core.certificates.word_generator import WordCertificateGenerator
        
        # Crear generador
        generator = WordCertificateGenerator(self.template_path)
        
        # Callback para progreso de Word (5% a 50%)
        def word_progress(idx, msg, exitosos, total):
            if main_callback:
                self.items_procesados = idx
                tiempo_restante = self._calculate_tiempo_restante(idx, total)
                # Calcular porcentaje entre 5% y 50%
                percent = 5 + int((idx / total) * 45)
                main_callback(percent, f"Generando Word: {exitosos}/{total}", tiempo_restante)
        
        # Generar batch
        results = generator.generate_batch(
            df,
            self.word_folder,
            progress_callback=word_progress
        )
        
        return results
    
    def _convert_to_pdf(self,
                       main_callback: Optional[Callable] = None
                       ) -> Dict[str, Any]:
        """Convierte certificados Word a PDF"""
        from core.certificates.pdf_converter import PDFConverter
        
        # Crear conversor
        converter = PDFConverter()
        
        # Callback para progreso de PDF (55% a 90%)
        def pdf_progress(idx, msg, exitosos, total):
            if main_callback:
                # Resetear tracking para fase PDF
                if idx == 1:
                    self.items_procesados = 0
                    self.start_time = time.time()
                
                self.items_procesados = idx
                tiempo_restante = self._calculate_tiempo_restante(idx, total)
                # Calcular porcentaje entre 55% y 90%
                percent = 55 + int((idx / total) * 35)
                main_callback(percent, f"Convirtiendo PDF: {exitosos}/{total}", tiempo_restante)
        
        # Convertir batch
        results = converter.convert_batch(
            self.word_folder,
            self.pdf_folder,
            progress_callback=pdf_progress,
            retry=3
        )
        
        return results
    
    def _cleanup_word_files(self) -> int:
        """Limpia archivos Word después de conversión"""
        from core.certificates.pdf_converter import PDFConverter
        
        deleted_count = PDFConverter.cleanup_word_files(self.word_folder)
        return deleted_count
    
    def _generate_report_json(self, results: dict, options: dict) -> None:
        """Genera reporte en formato JSON"""
        report = {
            'timestamp': self.timestamp,
            'template_used': os.path.basename(self.template_path),
            'input_records': results['input_records'],
            'options': options,
            'word_generation': None,
            'pdf_conversion': None,
            'total_time_seconds': results['total_time'],
            'total_time_formatted': results.get('total_time_formatted', '00:00'),
            'success': results['success'],
            'errors': results['errors']
        }
        
        # Agregar resultados de Word si existen
        if results['word_results']:
            report['word_generation'] = {
                'total': results['word_results']['total'],
                'successful': results['word_results']['exitosos'],
                'failed': results['word_results']['fallidos'],
                'errors': results['word_results']['errores']
            }
        
        # Agregar resultados de PDF si existen
        if results['pdf_results']:
            report['pdf_conversion'] = {
                'total': results['pdf_results']['total'],
                'successful': results['pdf_results']['exitosos'],
                'failed': results['pdf_results']['fallidos'],
                'errors': results['pdf_results']['errores']
            }
        
        # Guardar JSON
        report_path = os.path.join(self.output_folder, "generation_report.json")
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
        except Exception as e:
            results['errors'].append(f"Error al generar reporte JSON: {str(e)}")
    
    def get_output_summary(self) -> Dict[str, str]:
        """
        Retorna resumen de rutas de salida.
        
        Returns:
            Diccionario con rutas principales
        """
        return {
            'output_folder': self.output_folder,
            'word_folder': self.word_folder,
            'pdf_folder': self.pdf_folder,
            'timestamp': self.timestamp
        }