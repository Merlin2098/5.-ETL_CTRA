# core/etl/date_processor.py
"""
Servicio de procesamiento de fechas y conversiones
"""
import pandas as pd
from datetime import date
import re
from typing import Tuple, Dict, Any

class DateProcessor:
    """Servicio para procesamiento de fechas y conversiones"""
    
    # Nombres de meses en español
    MESES_ES = {
        '01': 'enero', '02': 'febrero', '03': 'marzo', '04': 'abril',
        '05': 'mayo', '06': 'junio', '07': 'julio', '08': 'agosto', 
        '09': 'septiembre', '10': 'octubre', '11': 'noviembre', '12': 'diciembre'
    }
    
    @staticmethod
    def agregar_mes_analizado(df: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame]:
        """
        Agrega columna MES_ANALIZADO
        
        Args:
            df: DataFrame a procesar
            
        Returns:
            Tupla (éxito, mensaje, DataFrame con columna agregada)
        """
        try:
            df['MES_ANALIZADO'] = df['INICIO CONTRATO'].dt.to_period('M').astype(str)
            return True, "Columna MES_ANALIZADO agregada", df
            
        except Exception as e:
            return False, f"Error al agregar MES_ANALIZADO: {str(e)}", df
    
    @staticmethod
    def agregar_fecha_generar(df: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame]:
        """
        Agrega columna FECHA_GENERAR con la fecha actual
        
        Args:
            df: DataFrame a procesar
            
        Returns:
            Tupla (éxito, mensaje, DataFrame con columna agregada)
        """
        try:
            fecha_actual = date.today().strftime('%d/%m/%Y')
            df['FECHA_GENERAR'] = fecha_actual
            return True, "FECHA_GENERAR agregada", df
            
        except Exception as e:
            return False, f"Error al agregar FECHA_GENERAR: {str(e)}", df
    
    @staticmethod
    def convertir_fechas_a_texto(df: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame]:
        """
        Convierte fechas a texto en español
        
        Args:
            df: DataFrame a procesar
            
        Returns:
            Tupla (éxito, mensaje, DataFrame con fechas convertidas)
        """
        try:
            def convertir_fecha(fecha_str):
                """Convierte 'dd/mm/yyyy' a 'dd de mes de yyyy'"""
                try:
                    dia, mes_num, anio = fecha_str.split('/')
                    mes_nombre = DateProcessor.MESES_ES.get(mes_num, mes_num)
                    dia_limpio = str(int(dia))
                    return f"{dia_limpio} de {mes_nombre} de {anio}"
                except:
                    return fecha_str
            
            def transformar_intervalos(intervalos_str):
                """Transforma todos los intervalos en un texto"""
                if pd.isna(intervalos_str):
                    return ""
                
                intervalos_str = str(intervalos_str)
                patron_fecha = r'\d{2}/\d{2}/\d{4}'
                fechas_encontradas = re.findall(patron_fecha, intervalos_str)
                
                cadena_transformada = intervalos_str
                for fecha_num in set(fechas_encontradas):
                    fecha_letra = convertir_fecha(fecha_num)
                    cadena_transformada = cadena_transformada.replace(fecha_num, fecha_letra)
                
                # Reemplazar separador
                return cadena_transformada.replace(' | ', '; ')
            
            # Convertir FECHAS_CERTIFICADO
            if 'FECHAS_CERTIFICADO' in df.columns:
                df['FECHAS_CERTIFICADO'] = df['FECHAS_CERTIFICADO'].apply(transformar_intervalos)
            
            # Convertir FECHA_GENERAR
            if 'FECHA_GENERAR' in df.columns:
                df['FECHA_GENERAR'] = df['FECHA_GENERAR'].apply(convertir_fecha)
            
            return True, "Fechas convertidas a texto en español", df
            
        except Exception as e:
            return False, f"Error al convertir fechas a texto: {str(e)}", df
    
    @staticmethod
    def calcular_dias_laborados(df: pd.DataFrame) -> Tuple[bool, str, pd.DataFrame]:
        """
        Calcula DÍAS_LABORADOS a partir de intervalos
        
        Args:
            df: DataFrame a procesar
            
        Returns:
            Tupla (éxito, mensaje, DataFrame con días calculados)
        """
        try:
            def contar_dias(periodos_texto):
                if pd.isna(periodos_texto):
                    return 0
                
                periodos = str(periodos_texto).split("|")
                total_dias = 0
                
                for periodo in periodos:
                    periodo = periodo.strip()
                    if "al" not in periodo:
                        continue
                    
                    try:
                        inicio_txt, fin_txt = periodo.split("al")
                        inicio = pd.to_datetime(inicio_txt.strip(), format="%d/%m/%Y")
                        fin = pd.to_datetime(fin_txt.strip(), format="%d/%m/%Y")
                        total_dias += (fin - inicio).days + 1
                    except:
                        continue
                
                return total_dias
            
            df['DÍAS_LABORADOS'] = df['FECHAS_CERTIFICADO'].apply(contar_dias)
            return True, "DÍAS_LABORADOS calculados", df
            
        except Exception as e:
            return False, f"Error al calcular días laborados: {str(e)}", df