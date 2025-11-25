"""
Módulo de filtrado de datos para generación de certificados.
Permite filtrado opcional y progresivo del DataFrame limpio.
"""

import pandas as pd
from typing import List, Optional, Tuple


class CertificateDataFilter:
    """
    Filtrador de datos limpio para generación de certificados.
    Filtrado opcional en cascada: DNI → Cliente → Mes
    """
    
    # Columnas requeridas para generación de certificados
    REQUIRED_COLUMNS = [
        'APELLIDOS Y NOMBRES',
        'FECHAS_CERTIFICADO',
        'DÍAS_LABORADOS',
        'CARGO',
        'CLIENTE',
        'FECHA_GENERAR'
    ]
    
    # Columnas adicionales para filtrado
    FILTER_COLUMNS = ['DNI', 'CLIENTE', 'MES_ANALIZADO']
    
    @staticmethod
    def load_clean_data(file_path: str) -> pd.DataFrame:
        """
        Carga archivo Excel limpio con DNI como string.
        
        Args:
            file_path: Ruta al archivo Excel limpio
            
        Returns:
            DataFrame cargado
            
        Raises:
            ValueError: Si hay problemas con el archivo o columnas faltantes
        """
        # Validar extensión
        if not file_path.lower().endswith(('.xlsx', '.xls')):
            raise ValueError("El archivo debe ser .xlsx o .xls")
        
        try:
            # Cargar con DNI como string para preservar ceros iniciales
            df = pd.read_excel(file_path, dtype={'DNI': str})
        except FileNotFoundError:
            raise ValueError(f"Archivo no encontrado: {file_path}")
        except Exception as e:
            raise ValueError(f"Error al cargar archivo: {str(e)}")
        
        # Validar que no esté vacío
        if df.empty:
            raise ValueError("El archivo está vacío")
        
        # Validar columnas requeridas
        missing_cols = [col for col in CertificateDataFilter.REQUIRED_COLUMNS 
                       if col not in df.columns]
        
        if missing_cols:
            raise ValueError(f"Faltan columnas requeridas: {', '.join(missing_cols)}")
        
        return df
    
    @staticmethod
    def get_unique_dnis(df: pd.DataFrame) -> List[str]:
        """
        Retorna lista ordenada de DNIs únicos.
        
        Args:
            df: DataFrame con datos
            
        Returns:
            Lista con "TODOS" seguido de DNIs únicos ordenados
        """
        if 'DNI' not in df.columns:
            return ["TODOS"]
        
        # Obtener DNIs únicos, eliminar nulos
        dnis = df['DNI'].dropna().unique().tolist()
        
        # Ordenar
        dnis_sorted = sorted(dnis)
        
        # Agregar "TODOS" al inicio
        return ["TODOS"] + dnis_sorted
    
    @staticmethod
    def get_unique_clients(df: pd.DataFrame, 
                          dni_filter: Optional[str] = None) -> List[str]:
        """
        Retorna clientes únicos (opcionalmente filtrados por DNI).
        
        Args:
            df: DataFrame con datos
            dni_filter: DNI para filtrar (opcional, "TODOS" = sin filtro)
            
        Returns:
            Lista con "TODOS" seguido de clientes únicos ordenados
        """
        if 'CLIENTE' not in df.columns:
            return ["TODOS"]
        
        # Aplicar filtro de DNI si corresponde
        df_filtered = df.copy()
        if dni_filter and dni_filter != "TODOS":
            if 'DNI' in df.columns:
                df_filtered = df_filtered[df_filtered['DNI'] == dni_filter]
        
        # Obtener clientes únicos
        clientes = df_filtered['CLIENTE'].dropna().unique().tolist()
        
        # Ordenar
        clientes_sorted = sorted(clientes)
        
        # Agregar "TODOS" al inicio
        return ["TODOS"] + clientes_sorted
    
    @staticmethod
    def get_unique_months(df: pd.DataFrame,
                         dni_filter: Optional[str] = None,
                         client_filter: Optional[str] = None) -> List[str]:
        """
        Retorna meses únicos (opcionalmente filtrados).
        
        Args:
            df: DataFrame con datos
            dni_filter: DNI para filtrar (opcional, "TODOS" = sin filtro)
            client_filter: Cliente para filtrar (opcional, "TODOS" = sin filtro)
            
        Returns:
            Lista con "TODOS" seguido de meses únicos ordenados cronológicamente
        """
        if 'MES_ANALIZADO' not in df.columns:
            return ["TODOS"]
        
        # Aplicar filtros progresivos
        df_filtered = df.copy()
        
        # Filtro por DNI
        if dni_filter and dni_filter != "TODOS":
            if 'DNI' in df.columns:
                df_filtered = df_filtered[df_filtered['DNI'] == dni_filter]
        
        # Filtro por Cliente
        if client_filter and client_filter != "TODOS":
            if 'CLIENTE' in df.columns:
                df_filtered = df_filtered[df_filtered['CLIENTE'] == client_filter]
        
        # Obtener meses únicos
        meses = df_filtered['MES_ANALIZADO'].dropna().unique().tolist()
        
        # Ordenar cronológicamente (asumiendo formato YYYY-MM)
        meses_sorted = sorted(meses)
        
        # Agregar "TODOS" al inicio
        return ["TODOS"] + meses_sorted
    
    @staticmethod
    def apply_filter(df: pd.DataFrame,
                    dni: Optional[str] = None,
                    cliente: Optional[str] = None,
                    mes: Optional[str] = None) -> pd.DataFrame:
        """
        Aplica filtros combinados (ignora "TODOS" y None).
        
        Args:
            df: DataFrame original
            dni: DNI a filtrar (None o "TODOS" = sin filtro)
            cliente: Cliente a filtrar (None o "TODOS" = sin filtro)
            mes: Mes a filtrar (None o "TODOS" = sin filtro)
            
        Returns:
            DataFrame filtrado
        """
        # Copiar DataFrame para no modificar el original
        df_result = df.copy()
        
        # Aplicar filtro DNI
        if dni and dni != "TODOS" and 'DNI' in df_result.columns:
            df_result = df_result[df_result['DNI'] == dni]
        
        # Aplicar filtro Cliente
        if cliente and cliente != "TODOS" and 'CLIENTE' in df_result.columns:
            df_result = df_result[df_result['CLIENTE'] == cliente]
        
        # Aplicar filtro Mes
        if mes and mes != "TODOS" and 'MES_ANALIZADO' in df_result.columns:
            df_result = df_result[df_result['MES_ANALIZADO'] == mes]
        
        return df_result
    
    @staticmethod
    def validate_columns(df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Valida que existan las columnas requeridas para placeholders.
        
        Args:
            df: DataFrame a validar
            
        Returns:
            Tupla (éxito, lista_columnas_faltantes)
        """
        missing = []
        
        for col in CertificateDataFilter.REQUIRED_COLUMNS:
            if col not in df.columns:
                missing.append(col)
        
        success = len(missing) == 0
        return success, missing
    
    @staticmethod
    def export_filtered(df: pd.DataFrame, output_path: str) -> bool:
        """
        Exporta DataFrame filtrado a Excel.
        
        Args:
            df: DataFrame a exportar
            output_path: Ruta de salida
            
        Returns:
            True si se exportó correctamente, False en caso contrario
        """
        try:
            df.to_excel(output_path, index=False)
            return True
        except Exception as e:
            print(f"Error al exportar: {str(e)}")
            return False
    
    @staticmethod
    def get_filter_summary(df_original: pd.DataFrame, 
                          df_filtered: pd.DataFrame,
                          dni: Optional[str] = None,
                          cliente: Optional[str] = None,
                          mes: Optional[str] = None) -> dict:
        """
        Genera resumen del filtrado aplicado.
        
        Args:
            df_original: DataFrame original
            df_filtered: DataFrame después del filtro
            dni: Filtro DNI aplicado
            cliente: Filtro Cliente aplicado
            mes: Filtro Mes aplicado
            
        Returns:
            Diccionario con resumen del filtrado
        """
        return {
            'total_original': len(df_original),
            'total_filtrado': len(df_filtered),
            'porcentaje': round(len(df_filtered) / len(df_original) * 100, 2) if len(df_original) > 0 else 0,
            'filtros_aplicados': {
                'dni': dni if dni and dni != "TODOS" else None,
                'cliente': cliente if cliente and cliente != "TODOS" else None,
                'mes': mes if mes and mes != "TODOS" else None
            }
        }