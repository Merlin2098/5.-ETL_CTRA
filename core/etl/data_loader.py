# core/etl/data_loader.py
"""
Servicio de carga y validación de datos
"""
import pandas as pd
import os
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

class DataLoader:
    """Servicio para carga y validación inicial de datos"""
    
    # Columnas requeridas en el dataset
    COLUMNAS_REQUERIDAS = [
        'DNI',
        'APELLIDOS Y NOMBRES', 
        'INICIO CONTRATO',
        'FIN CONTRATO',
        'CLIENTE',
        'CARGO'
    ]
    
    @staticmethod
    def cargar_archivo(ruta: str) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        Carga el archivo Excel RAW
        
        Args:
            ruta: Ruta al archivo Excel
            
        Returns:
            Tupla (éxito, mensaje, DataFrame)
        """
        try:
            if not os.path.exists(ruta):
                return False, f"El archivo no existe: {ruta}", None
            
            # Leer con dtype str para preservar formatos
            df = pd.read_excel(ruta, dtype=str)
            
            mensaje = f"Archivo cargado ({len(df):,} registros)"
            return True, mensaje, df
            
        except Exception as e:
            return False, f"Error al cargar archivo: {str(e)}", None
    
    @staticmethod
    def filtrar_columnas_necesarias(df: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame]:
        """
        Filtra solo las columnas necesarias
        
        Args:
            df: DataFrame original
            
        Returns:
            Tupla (éxito, mensaje, DataFrame filtrado)
        """
        try:
            columnas_actuales = df.columns.tolist()
            columnas_faltantes = [col for col in DataLoader.COLUMNAS_REQUERIDAS 
                                if col not in columnas_actuales]
            
            if columnas_faltantes:
                return False, f"Faltan columnas requeridas: {', '.join(columnas_faltantes)}", df
            
            df_filtrado = df[DataLoader.COLUMNAS_REQUERIDAS].copy()
            columnas_eliminadas = len(columnas_actuales) - len(DataLoader.COLUMNAS_REQUERIDAS)
            
            mensaje = f"{columnas_eliminadas} columnas innecesarias eliminadas"
            return True, mensaje, df_filtrado
            
        except Exception as e:
            return False, f"Error al filtrar columnas: {str(e)}", df
    
    @staticmethod
    def validar_columnas(df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Valida que existan todas las columnas requeridas
        
        Args:
            df: DataFrame a validar
            
        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            columnas_faltantes = [col for col in DataLoader.COLUMNAS_REQUERIDAS 
                                if col not in df.columns]
            
            if columnas_faltantes:
                return False, f"Faltan columnas: {', '.join(columnas_faltantes)}"
            
            return True, "Estructura de datos validada"
            
        except Exception as e:
            return False, f"Error al validar columnas: {str(e)}"