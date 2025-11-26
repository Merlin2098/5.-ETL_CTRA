"""
Módulo de filtrado de datos para generación de certificados.
Permite filtrado opcional y progresivo del DataFrame limpio con selección múltiple.
"""

import pandas as pd
from typing import List, Optional, Tuple


class CertificateDataFilter:
    """
    Filtrador de datos limpio para generación de certificados.
    Filtrado opcional en cascada: DNI → Cliente → Mes
    Soporta selección múltiple en cada nivel.
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
        Retorna lista ordenada de DNIs únicos (sin "TODOS").
        
        Args:
            df: DataFrame con datos
            
        Returns:
            Lista con DNIs únicos ordenados
        """
        if 'DNI' not in df.columns:
            return []
        
        # Obtener DNIs únicos, eliminar nulos
        dnis = df['DNI'].dropna().unique().tolist()
        
        # Ordenar
        dnis_sorted = sorted(dnis)
        
        return dnis_sorted
    
    @staticmethod
    def get_unique_clients(df: pd.DataFrame, 
                          dni_filters: Optional[List[str]] = None) -> List[str]:
        """
        Retorna clientes únicos filtrados por DNIs seleccionados.
        
        Args:
            df: DataFrame con datos
            dni_filters: Lista de DNIs para filtrar (None = sin filtro)
            
        Returns:
            Lista con clientes únicos ordenados
        """
        if 'CLIENTE' not in df.columns:
            return []
        
        # Aplicar filtro de DNI si corresponde
        df_filtered = df.copy()
        if dni_filters and len(dni_filters) > 0:
            if 'DNI' in df.columns:
                df_filtered = df_filtered[df_filtered['DNI'].isin(dni_filters)]
        
        # Obtener clientes únicos
        clientes = df_filtered['CLIENTE'].dropna().unique().tolist()
        
        # Ordenar
        clientes_sorted = sorted(clientes)
        
        return clientes_sorted
    
    @staticmethod
    def get_unique_months(df: pd.DataFrame,
                         dni_filters: Optional[List[str]] = None,
                         client_filters: Optional[List[str]] = None) -> List[str]:
        """
        Retorna meses únicos filtrados por DNIs y Clientes seleccionados.
        
        Args:
            df: DataFrame con datos
            dni_filters: Lista de DNIs para filtrar (None = sin filtro)
            client_filters: Lista de Clientes para filtrar (None = sin filtro)
            
        Returns:
            Lista con meses únicos ordenados cronológicamente
        """
        if 'MES_ANALIZADO' not in df.columns:
            return []
        
        # Aplicar filtros progresivos
        df_filtered = df.copy()
        
        # Filtro por DNI
        if dni_filters and len(dni_filters) > 0:
            if 'DNI' in df.columns:
                df_filtered = df_filtered[df_filtered['DNI'].isin(dni_filters)]
        
        # Filtro por Cliente
        if client_filters and len(client_filters) > 0:
            if 'CLIENTE' in df.columns:
                df_filtered = df_filtered[df_filtered['CLIENTE'].isin(client_filters)]
        
        # Obtener meses únicos
        meses = df_filtered['MES_ANALIZADO'].dropna().unique().tolist()
        
        # Ordenar cronológicamente (asumiendo formato YYYY-MM)
        meses_sorted = sorted(meses)
        
        return meses_sorted
    
    @staticmethod
    def apply_filter(df: pd.DataFrame,
                    dnis: Optional[List[str]] = None,
                    clientes: Optional[List[str]] = None,
                    meses: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Aplica filtros múltiples combinados (AND entre categorías, OR dentro de cada categoría).
        
        Ejemplo: 
            dnis=["12345678", "87654321"] AND meses=["2025-08", "2025-09"]
            Retorna registros donde:
            (DNI es 12345678 OR 87654321) AND (MES es 2025-08 OR 2025-09)
        
        Args:
            df: DataFrame original
            dnis: Lista de DNIs a filtrar (None o [] = sin filtro)
            clientes: Lista de Clientes a filtrar (None o [] = sin filtro)
            meses: Lista de Meses a filtrar (None o [] = sin filtro)
            
        Returns:
            DataFrame filtrado
        """
        # Copiar DataFrame para no modificar el original
        df_result = df.copy()
        
        # Aplicar filtro DNI (OR: dni1 OR dni2 OR ...)
        if dnis and len(dnis) > 0 and 'DNI' in df_result.columns:
            df_result = df_result[df_result['DNI'].isin(dnis)]
        
        # Aplicar filtro Cliente (OR: cliente1 OR cliente2 OR ...)
        if clientes and len(clientes) > 0 and 'CLIENTE' in df_result.columns:
            df_result = df_result[df_result['CLIENTE'].isin(clientes)]
        
        # Aplicar filtro Mes (OR: mes1 OR mes2 OR ...)
        if meses and len(meses) > 0 and 'MES_ANALIZADO' in df_result.columns:
            df_result = df_result[df_result['MES_ANALIZADO'].isin(meses)]
        
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
                          dnis: Optional[List[str]] = None,
                          clientes: Optional[List[str]] = None,
                          meses: Optional[List[str]] = None) -> dict:
        """
        Genera resumen del filtrado aplicado.
        
        Args:
            df_original: DataFrame original
            df_filtered: DataFrame después del filtro
            dnis: Lista de filtros DNI aplicados
            clientes: Lista de filtros Cliente aplicados
            meses: Lista de filtros Mes aplicados
            
        Returns:
            Diccionario con resumen del filtrado
        """
        return {
            'total_original': len(df_original),
            'total_filtrado': len(df_filtered),
            'porcentaje': round(len(df_filtered) / len(df_original) * 100, 2) if len(df_original) > 0 else 0,
            'filtros_aplicados': {
                'dnis': dnis if dnis and len(dnis) > 0 else None,
                'clientes': clientes if clientes and len(clientes) > 0 else None,
                'meses': meses if meses and len(meses) > 0 else None
            },
            'cantidad_dnis': len(dnis) if dnis else 0,
            'cantidad_clientes': len(clientes) if clientes else 0,
            'cantidad_meses': len(meses) if meses else 0
        }