# core/etl/period_consolidator.py
"""
Servicio para consolidación de períodos contiguos
"""
import pandas as pd
from typing import Tuple

class PeriodConsolidator:
    """Servicio para consolidar períodos contiguos y generar certificados"""
    
    @staticmethod
    def consolidar_y_generar_fechas(df: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame]:
        """
        Consolida períodos contiguos y genera FECHAS_CERTIFICADO
        
        Args:
            df: DataFrame con períodos divididos
            
        Returns:
            Tupla (éxito, mensaje, DataFrame consolidado)
        """
        try:
            df_temp = df.copy()
            
            # Agregar columna auxiliar para detectar continuidad
            df_temp['DIA_SIGUIENTE_FIN'] = df_temp['FIN CONTRATO'] + pd.Timedelta(days=1)
            
            # Ordenar por grupo y fecha
            df_temp = df_temp.sort_values([
                'DNI', 'CLIENTE', 'MES_ANALIZADO', 'CARGO', 'INICIO CONTRATO'
            ])
            
            # Detectar rupturas en la continuidad
            df_temp['IS_BREAK'] = ~(
                (df_temp['DNI'] == df_temp['DNI'].shift(1)) &
                (df_temp['CLIENTE'] == df_temp['CLIENTE'].shift(1)) &
                (df_temp['MES_ANALIZADO'] == df_temp['MES_ANALIZADO'].shift(1)) &
                (df_temp['CARGO'] == df_temp['CARGO'].shift(1)) &
                (df_temp['INICIO CONTRATO'] == df_temp['DIA_SIGUIENTE_FIN'].shift(1))
            ).fillna(True)
            
            # Asignar ID de grupo para períodos contiguos
            df_temp['GRUPO_ID'] = df_temp['IS_BREAK'].cumsum()
            
            # Consolidar por grupo
            df_consolidado = df_temp.groupby([
                'DNI', 'APELLIDOS Y NOMBRES', 'CLIENTE', 'CARGO', 
                'MES_ANALIZADO', 'GRUPO_ID'
            ]).agg(
                INICIO_CONSOLIDADO=('INICIO CONTRATO', 'min'),
                FIN_CONSOLIDADO=('FIN CONTRATO', 'max')
            ).reset_index()
            
            # Formatear intervalos
            df_consolidado['INTERVALO'] = (
                df_consolidado['INICIO_CONSOLIDADO'].dt.strftime('%d/%m/%Y') + 
                ' al ' + 
                df_consolidado['FIN_CONSOLIDADO'].dt.strftime('%d/%m/%Y')
            )
            
            # Agrupar intervalos por certificado
            df_certificado = df_consolidado.groupby([
                'DNI', 'APELLIDOS Y NOMBRES', 'CLIENTE', 'CARGO', 'MES_ANALIZADO'
            ]).agg(
                FECHAS_CERTIFICADO=('INTERVALO', lambda x: ' | '.join(x))
            ).reset_index()
            
            mensaje = f"{len(df_certificado):,} certificados consolidados"
            return True, mensaje, df_certificado
            
        except Exception as e:
            return False, f"Error al consolidar períodos: {str(e)}", df