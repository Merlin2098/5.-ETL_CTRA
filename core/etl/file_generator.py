# core/etl/file_generator.py
"""
Servicio para generación de archivos de salida
"""
import pandas as pd
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple
from config.paths import AppPaths

class FileGenerator:
    """Servicio para generación de archivos de salida"""
    
    @staticmethod
    def guardar_archivo(df: pd.DataFrame) -> Tuple[bool, str, str]:
        """
        Guarda el DataFrame procesado
        
        Args:
            df: DataFrame a guardar
            
        Returns:
            Tupla (éxito, mensaje, ruta de salida)
        """
        try:
            timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
            nombre_archivo = f"clean_{timestamp}.xlsx"
            ruta_salida = AppPaths.get_clean_dir() / nombre_archivo
            
            # Asegurar que el directorio existe
            AppPaths.get_clean_dir().mkdir(parents=True, exist_ok=True)
            
            df.to_excel(ruta_salida, index=False, engine='openpyxl')
            
            mensaje = f"Archivo guardado: {nombre_archivo}"
            return True, mensaje, str(ruta_salida)
            
        except Exception as e:
            return False, f"Error al guardar archivo: {str(e)}", ""