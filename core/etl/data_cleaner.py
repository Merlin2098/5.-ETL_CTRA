# core/etl/data_cleaner.py
"""
Servicio de limpieza y filtrado de datos
"""
import pandas as pd
from typing import Tuple, Optional, Dict, Any

class DataCleaner:
    """Servicio para limpieza y filtrado de datos"""
    
    # Valores que indican registros anulados
    VALORES_ANULADOS = [
        "ANULACION ADENDA DE RESOLUCION",
        "ANULACION RESOLUCION", 
        "ANULADO",
        "ANULADO RESOLUCION"
    ]
    
    @staticmethod
    def eliminar_filas_nulas(df: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame]:
        """
        Elimina filas con DNI o APELLIDOS Y NOMBRES nulos
        
        Args:
            df: DataFrame a limpiar
            
        Returns:
            Tupla (éxito, mensaje, DataFrame limpio)
        """
        try:
            registros_antes = len(df)
            
            # Eliminar nulos
            df_limpio = df.dropna(subset=['DNI', 'APELLIDOS Y NOMBRES'])
            # Eliminar vacíos
            df_limpio = df_limpio[df_limpio["DNI"].astype(str).str.strip() != ""]
            df_limpio = df_limpio[df_limpio["APELLIDOS Y NOMBRES"].astype(str).str.strip() != ""]
            
            filas_eliminadas = registros_antes - len(df_limpio)
            
            mensaje = f"{filas_eliminadas} filas nulas eliminadas"
            return True, mensaje, df_limpio
            
        except Exception as e:
            return False, f"Error al eliminar filas nulas: {str(e)}", df
    
    @staticmethod
    def limpiar_anulados(df: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame]:
        """
        Elimina registros marcados como ANULADOS
        
        Args:
            df: DataFrame a limpiar
            
        Returns:
            Tupla (éxito, mensaje, DataFrame limpio)
        """
        try:
            registros_antes = len(df)
            
            # Normalizar nombres
            df['APELLIDOS Y NOMBRES'] = df['APELLIDOS Y NOMBRES'].astype(str).str.strip().str.upper()
            
            # Eliminar anulados
            df_limpio = df[~df['APELLIDOS Y NOMBRES'].isin(DataCleaner.VALORES_ANULADOS)].copy()
            
            anulados_eliminados = registros_antes - len(df_limpio)
            
            mensaje = f"{anulados_eliminados} registros anulados eliminados"
            return True, mensaje, df_limpio
            
        except Exception as e:
            return False, f"Error al limpiar anulados: {str(e)}", df
    
    @staticmethod
    def formatear_columnas(df: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame]:
        """
        Formatea columnas de texto y fechas
        
        Args:
            df: DataFrame a formatear
            
        Returns:
            Tupla (éxito, mensaje, DataFrame formateado)
        """
        try:
            # Formatear texto
            for col in ['DNI', 'APELLIDOS Y NOMBRES', 'CLIENTE', 'CARGO']:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()
            
            # Formatear fechas
            for col in ['INICIO CONTRATO', 'FIN CONTRATO']:
                if col in df.columns:
                    # Reemplazar valores vacíos/inválidos
                    df[col] = df[col].astype(str).str.strip().replace({
                        "": None, "-": None, "—": None, "nan": None, "NaT": None
                    })
                    df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
            
            return True, "Columnas formateadas correctamente", df
            
        except Exception as e:
            return False, f"Error al formatear columnas: {str(e)}", df
    
    @staticmethod
    def detectar_fechas_invalidas(df: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame]:
        """
        Detecta y elimina registros con fechas inválidas
        
        Args:
            df: DataFrame a validar
            
        Returns:
            Tupla (éxito, mensaje, DataFrame validado)
        """
        try:
            registros_antes = len(df)
            
            # Eliminar fechas nulas
            df_limpio = df.dropna(subset=['INICIO CONTRATO', 'FIN CONTRATO'])
            
            # Eliminar fechas lógicamente incorrectas
            df_limpio = df_limpio[df_limpio['FIN CONTRATO'] >= df_limpio['INICIO CONTRATO']]
            
            fechas_invalidas = registros_antes - len(df_limpio)
            
            mensaje = f"{fechas_invalidas} registros con fechas inválidas eliminados"
            return True, mensaje, df_limpio
            
        except Exception as e:
            return False, f"Error al detectar fechas inválidas: {str(e)}", df
    
    @staticmethod
    def eliminar_duplicados(df: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame]:
        """
        Elimina registros duplicados
        
        Args:
            df: DataFrame a limpiar
            
        Returns:
            Tupla (éxito, mensaje, DataFrame sin duplicados)
        """
        try:
            registros_antes = len(df)
            df_limpio = df.drop_duplicates()
            duplicados_eliminados = registros_antes - len(df_limpio)
            
            mensaje = f"{duplicados_eliminados} duplicados eliminados"
            return True, mensaje, df_limpio
            
        except Exception as e:
            return False, f"Error al eliminar duplicados: {str(e)}", df