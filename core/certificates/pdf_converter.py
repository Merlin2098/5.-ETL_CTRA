"""
Módulo de conversión de certificados Word a PDF.
Convierte archivos .docx a .pdf con manejo de reintentos.
"""

import os
import time
import platform
from pathlib import Path
from typing import Tuple, Dict, List, Optional, Callable, Any


class PDFConverter:
    """Conversor de certificados Word a PDF con retry automático"""
    
    def __init__(self):
        """Inicializa el conversor"""
        self.system = platform.system()
        self.word_available = self._check_word_available()
    
    def _check_word_available(self) -> bool:
        """
        Verifica si MS Word está disponible en el sistema.
        
        Returns:
            True si Word está disponible, False en caso contrario
        """
        if self.system != "Windows":
            return False
        
        try:
            import win32com.client
            import pythoncom
            
            # Inicializar COM
            pythoncom.CoInitialize()
            
            try:
                # Intentar crear instancia de Word
                word = win32com.client.Dispatch("Word.Application")
                word.Visible = False
                word.Quit()
                return True
            except Exception:
                return False
            finally:
                pythoncom.CoUninitialize()
                
        except ImportError:
            # win32com no disponible
            return False
        except Exception:
            return False
    
    def convert_single(self,
                      word_path: str,
                      pdf_path: str,
                      retry: int = 3) -> Tuple[bool, str]:
        """
        Convierte un archivo Word a PDF con reintentos usando win32com directamente.
        
        Args:
            word_path: Ruta del archivo Word
            pdf_path: Ruta del archivo PDF de salida
            retry: Número de reintentos en caso de fallo
            
        Returns:
            Tupla (éxito, mensaje)
        """
        # Verificar si Word está disponible
        if not self.word_available:
            return False, "Microsoft Word no está instalado o no está disponible"
        
        # Validar que el archivo Word existe
        if not os.path.exists(word_path):
            return False, f"Archivo Word no existe: {word_path}"
        
        # Validar extensión
        if not word_path.lower().endswith('.docx'):
            return False, f"El archivo debe ser .docx: {word_path}"
        
        # Asegurar que el directorio de salida existe
        output_dir = os.path.dirname(pdf_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                return False, f"Error al crear directorio: {str(e)}"
        
        # Convertir rutas a absolutas
        word_path_abs = os.path.abspath(word_path)
        pdf_path_abs = os.path.abspath(pdf_path)
        
        # Intentar conversión con reintentos
        last_error = None
        
        for attempt in range(1, retry + 1):
            word_app = None
            doc = None
            
            try:
                import win32com.client
                import pythoncom
                
                # Inicializar COM
                pythoncom.CoInitialize()
                
                try:
                    # Crear instancia de Word
                    word_app = win32com.client.Dispatch("Word.Application")
                    word_app.Visible = False
                    word_app.DisplayAlerts = 0  # No mostrar alertas
                    
                    # Abrir documento
                    doc = word_app.Documents.Open(word_path_abs)
                    
                    # Guardar como PDF (formato 17 = PDF)
                    doc.SaveAs(pdf_path_abs, FileFormat=17)
                    
                    # Cerrar documento
                    doc.Close(False)
                    
                    # Verificar que se creó el PDF
                    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
                        return True, pdf_path
                    else:
                        last_error = "PDF creado pero está vacío"
                        
                except Exception as e:
                    last_error = str(e)
                    
                finally:
                    # Limpiar recursos
                    try:
                        if doc:
                            doc.Close(False)
                    except:
                        pass
                    
                    try:
                        if word_app:
                            word_app.Quit()
                    except:
                        pass
                    
                    pythoncom.CoUninitialize()
                    
            except Exception as e:
                last_error = f"Error al inicializar COM: {str(e)}"
            
            # Si no es el último intento, esperar antes de reintentar
            if attempt < retry:
                time.sleep(2)
        
        # Si llegamos aquí, todos los intentos fallaron
        return False, f"Error después de {retry} intentos: {last_error}"
    
    def convert_batch(self,
                     word_folder: str,
                     pdf_folder: str,
                     progress_callback: Optional[Callable[[int, str, int, int], None]] = None,
                     retry: int = 3) -> Dict[str, Any]:
        """
        Convierte múltiples archivos Word a PDF.
        
        Args:
            word_folder: Carpeta con archivos Word
            pdf_folder: Carpeta de salida para PDFs
            progress_callback: Función callback(índice, mensaje, exitosos, total)
            retry: Número de reintentos por archivo
            
        Returns:
            Diccionario con resultados:
            {
                'total': int,
                'exitosos': int,
                'fallidos': int,
                'archivos_generados': List[str],
                'errores': List[Dict],
                'word_available': bool
            }
        """
        # Validar carpeta de entrada
        if not os.path.exists(word_folder):
            raise ValueError(f"Carpeta Word no existe: {word_folder}")
        
        # Crear carpeta de salida si no existe
        os.makedirs(pdf_folder, exist_ok=True)
        
        # Listar archivos .docx
        word_files = [f for f in os.listdir(word_folder) 
                     if f.lower().endswith('.docx') and not f.startswith('~$')]
        
        if not word_files:
            return {
                'total': 0,
                'exitosos': 0,
                'fallidos': 0,
                'archivos_generados': [],
                'errores': [],
                'word_available': self.word_available
            }
        
        # Si Word no está disponible, fallar rápido
        if not self.word_available:
            return {
                'total': len(word_files),
                'exitosos': 0,
                'fallidos': len(word_files),
                'archivos_generados': [],
                'errores': [{
                    'archivo': 'TODOS',
                    'error': 'Microsoft Word no está instalado o no está disponible. Se requiere MS Word para convertir a PDF.'
                }],
                'word_available': False
            }
        
        # Inicializar resultados
        results = {
            'total': len(word_files),
            'exitosos': 0,
            'fallidos': 0,
            'archivos_generados': [],
            'errores': [],
            'word_available': True
        }
        
        # Procesar cada archivo
        for idx, word_file in enumerate(word_files, 1):
            try:
                # Construir rutas
                word_path = os.path.join(word_folder, word_file)
                pdf_file = os.path.splitext(word_file)[0] + '.pdf'
                pdf_path = os.path.join(pdf_folder, pdf_file)
                
                # Convertir
                success, message = self.convert_single(word_path, pdf_path, retry=retry)
                
                if success:
                    results['exitosos'] += 1
                    results['archivos_generados'].append(pdf_path)
                    
                    # Callback de progreso
                    if progress_callback:
                        progress_callback(
                            idx,
                            f"Convertido: {pdf_file}",
                            results['exitosos'],
                            results['total']
                        )
                else:
                    results['fallidos'] += 1
                    results['errores'].append({
                        'archivo': word_file,
                        'error': message
                    })
                    
                    # Callback de progreso con error
                    if progress_callback:
                        progress_callback(
                            idx,
                            f"ERROR: {word_file} - {message}",
                            results['exitosos'],
                            results['total']
                        )
                
            except Exception as e:
                results['fallidos'] += 1
                error_msg = f"Excepción: {str(e)}"
                
                results['errores'].append({
                    'archivo': word_file,
                    'error': error_msg
                })
                
                # Callback de progreso con excepción
                if progress_callback:
                    progress_callback(
                        idx,
                        f"EXCEPCIÓN: {word_file} - {error_msg}",
                        results['exitosos'],
                        results['total']
                    )
        
        return results
    
    @staticmethod
    def cleanup_word_files(folder: str, 
                          keep_list: Optional[List[str]] = None) -> int:
        """
        Elimina archivos .docx de una carpeta.
        
        Args:
            folder: Carpeta con archivos Word
            keep_list: Lista de nombres de archivo a preservar (opcional)
            
        Returns:
            Cantidad de archivos eliminados
        """
        if not os.path.exists(folder):
            return 0
        
        keep_set = set(keep_list) if keep_list else set()
        deleted_count = 0
        
        # Listar archivos .docx
        word_files = [f for f in os.listdir(folder) 
                     if f.lower().endswith('.docx') and not f.startswith('~$')]
        
        for word_file in word_files:
            # Saltar si está en la lista de preservación
            if word_file in keep_set:
                continue
            
            try:
                word_path = os.path.join(folder, word_file)
                os.remove(word_path)
                deleted_count += 1
            except Exception as e:
                # Ignorar errores de eliminación
                pass
        
        return deleted_count
    
    def get_system_info(self) -> Dict[str, str]:
        """
        Retorna información del sistema para debugging.
        
        Returns:
            Diccionario con información del sistema
        """
        return {
            'system': self.system,
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'converter': 'docx2pdf',
            'word_available': str(self.word_available)
        }