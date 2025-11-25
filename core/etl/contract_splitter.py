# core/etl/contract_splitter.py
"""
Servicio para división de contratos por mes
"""
import pandas as pd
from dateutil.relativedelta import relativedelta
from typing import Tuple, List

class ContractSplitter:
    """Servicio para dividir contratos que abarcan múltiples meses"""
    
    @staticmethod
    def dividir_contratos_por_mes(df: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame]:
        """
        Divide contratos que abarcan múltiples meses
        
        Args:
            df: DataFrame con contratos
            
        Returns:
            Tupla (éxito, mensaje, DataFrame con contratos divididos)
        """
        try:
            filas_procesadas = []
            contratos_divididos = 0
            
            for _, row in df.iterrows():
                fecha_inicio = row['INICIO CONTRATO'].date()
                fecha_fin = row['FIN CONTRATO'].date()
                
                # Contar contratos que se dividen
                if fecha_inicio.month != fecha_fin.month or fecha_inicio.year != fecha_fin.year:
                    contratos_divididos += 1
                
                fecha_actual = fecha_inicio
                
                while fecha_actual <= fecha_fin:
                    # Calcular fin del mes actual
                    primer_dia_siguiente_mes = fecha_actual.replace(day=1) + relativedelta(months=1)
                    fin_mes_actual = primer_dia_siguiente_mes - relativedelta(days=1)
                    fin_rango = min(fin_mes_actual, fecha_fin)
                    
                    # Crear nueva fila para este segmento
                    nueva_fila = row.copy()
                    nueva_fila['INICIO CONTRATO'] = fecha_actual
                    nueva_fila['FIN CONTRATO'] = fin_rango
                    filas_procesadas.append(nueva_fila)
                    
                    # Avanzar al siguiente mes
                    fecha_actual = fin_rango + relativedelta(days=1)
            
            df_resultado = pd.DataFrame(filas_procesadas)
            
            # CRÍTICO: Convertir de date a datetime64[ns] para pandas
            df_resultado['INICIO CONTRATO'] = pd.to_datetime(df_resultado['INICIO CONTRATO'])
            df_resultado['FIN CONTRATO'] = pd.to_datetime(df_resultado['FIN CONTRATO'])
            
            mensaje = f"{contratos_divididos} contratos divididos ({len(df_resultado):,} registros)"
            return True, mensaje, df_resultado
            
        except Exception as e:
            return False, f"Error al dividir contratos: {str(e)}", df