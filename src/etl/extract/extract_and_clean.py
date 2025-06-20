# Copia el contenido de 01_extract_and_clean.py aquí, sin cambios en el código. 

import pandas as pd
import numpy as np
from utils import *
import openpyxl  # Importar la librería para lectura de bajo nivel

logger = setup_logging()

def extract_rfi_data():
    """Extrae y limpia datos RFI"""
    logger.info("Extrayendo datos RFI...")
    
    # Leer CSV con separador punto y coma
    df = pd.read_csv('../01_raw_data/rfi_raw/RFI.csv', sep=';')
    
    # Renombrar columnas para normalizar
    column_mapping = {
        'Campaign': 'campaign',
        'Month': 'month_year', 
        'Site (Site Directory)': 'site',
        'Placement - DCM': 'placement',
        'Creative': 'creative',
        'Creative Dimensions': 'size',
        'Platform Type': 'platform_type',
        'Impressions': 'impressions',
        'Clicks': 'clicks'
    }
    df = df.rename(columns=column_mapping)
    
    # Convertir fechas del formato 2021-01 a 2021-01-01
    def convert_month_to_date(month_str):
        """Convierte 2021-01 a 2021-01-01"""
        if pd.isna(month_str) or month_str == '' or str(month_str).strip() == '':
            return '1970-01-01'  # Valor por defecto para fechas faltantes
        
        # Limpiar y convertir string
        month_str_clean = str(month_str).strip()
        
        # Verificar que el formato sea correcto (YYYY-MM)
        if len(month_str_clean) == 7 and month_str_clean[4] == '-':
            return month_str_clean + '-01'
        else:
            raise ValueError(f"Formato de fecha RFI inesperado: '{month_str_clean}'")
    
    df['date'] = df['month_year'].apply(convert_month_to_date)
    
    # Limpiar métricas numéricas
    df['impressions'] = df['impressions'].apply(clean_numeric)
    df['clicks'] = df['clicks'].apply(clean_numeric)
    
    # Limpiar valores nulos en campos categóricos
    df['site'] = df['site'].fillna('Unknown')
    df['placement'] = df['placement'].fillna('Unknown')
    df['creative'] = df['creative'].fillna('Unknown') 
    df['size'] = df['size'].fillna('Unknown')
    
    # Seleccionar columnas finales
    df_final = df[['date', 'campaign', 'site', 'placement', 
                   'creative', 'size', 'impressions', 'clicks']]
    
    # Filtrar filas con valores válidos
    df_final = df_final[(df_final['impressions'] > 0) | (df_final['clicks'] > 0)]
    
    # Guardar staging
    save_csv(df_final, '../02_staging/rfi_staging.csv')
    logger.info(f"RFI staging creado: {len(df_final)} filas")
    
    return df_final

def extract_ga_data():
    """Extrae y limpia datos GA"""
    logger.info("==================== INICIANDO EXTRACCIÓN GA (CSV) ====================")
    logger.info("Intentando leer archivo: ../01_raw_data/ga_raw/Raw GA Data.csv")
    
    # Leer CSV (no Excel)
    df = pd.read_csv('../01_raw_data/ga_raw/Raw GA Data.csv', sep=';')
    logger.info(f"Archivo CSV leído exitosamente: {df.shape}")
    logger.info(f"Dimensiones del DataFrame: {df.shape}")
    logger.info(f"Columnas encontradas: {list(df.columns)}")
    logger.info(f"Primeras 3 filas:\n{df.head(3)}")
    
    # Renombrar columnas según la estructura real del CSV
    column_mapping = {
        'Source': 'source',
        'Month of Year': 'month_year',
        'Device Category': 'device',
        'Ad Content': 'ad_content',
        'Sessions': 'sessions',
        'Users': 'users',
        'New Users': 'new_users',
        'Pageviews': 'pageviews',
        'Session Duration': 'session_duration',
        'Calculated AToS': 'avg_session_duration'
    }
    
    logger.info("--- INICIANDO PROCESAMIENTO DETALLADO GA ---")
    logger.info(f"Columnas originales: {list(df.columns)}")
    logger.info(f"Columnas renombradas: {column_mapping}")
    
    df = df.rename(columns=column_mapping)
    logger.info(f"Columnas después del renombre: {list(df.columns)}")
    
    # Limpiar y convertir columnas numéricas con logging
    numeric_cols = ['users', 'new_users', 'sessions', 'pageviews']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_numeric)
            logger.info(f"Columna {col} convertida - suma total: {df[col].sum()}")
        else:
            logger.warning(f"Columna {col} no encontrada en DataFrame")
    
    # Convertir fecha desde month_year (formato 202104 -> 2021-04-01)
    df['date'] = pd.to_datetime(df['month_year'].astype(str), format='%Y%m')
    df['date'] = df['date'].dt.strftime('%Y-%m-01')
    logger.info(f"Fechas procesadas desde month_year. Ejemplo: {df['date'].iloc[0]}")
    
    # Procesar duración de sesión desde session_duration
    def duration_to_seconds(duration):
        if pd.isna(duration) or duration == '00:00:00' or str(duration).strip() == '':
            return 0
        try:
            duration_str = str(duration).strip().replace(',', '.')
            if ':' in duration_str:
                parts = duration_str.split(':')
                if len(parts) == 2:  # MM:SS
                    return int(parts[0]) * 60 + int(parts[1])
                elif len(parts) == 3:  # HH:MM:SS
                    return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            else:
                # Asumir que son segundos directamente
                return float(duration_str)
        except Exception as e:
            logger.warning(f"Error procesando duración '{duration}': {e}")
            return 0
    
    if 'session_duration' in df.columns:
        df['avg_session_duration_sec'] = df['session_duration'].apply(duration_to_seconds)
        logger.info(f"Duración procesada desde session_duration. Promedio: {df['avg_session_duration_sec'].mean():.2f} seg")
    else:
        df['avg_session_duration_sec'] = 0
        logger.warning("Columna session_duration no encontrada, usando 0")
    
    # Calcular bounce rate
    df['bounce_rate'] = np.where(df['sessions'] > 0, 
                                  1 - (df['pageviews'] / df['sessions']), 
                                  0)
    df['bounce_rate'] = df['bounce_rate'].clip(0, 1)
    logger.info(f"Bounce rate calculado. Promedio: {df['bounce_rate'].mean():.3f}")
    
    # Crear campaign desde source
    df['campaign'] = 'GA_Campaign_' + df['source'].astype(str)
    logger.info("Columna campaign creada desde source")
    
    # Limpiar valores nulos
    df['device'] = df['device'].fillna('desktop')
    df['ad_content'] = df['ad_content'].fillna('Unknown')
    
    logger.info("--- PROCESAMIENTO COMPLETADO ---")
    logger.info(f"Filas finales: {len(df)}")
    
    # Seleccionar columnas finales
    df_final = df[['date', 'campaign', 'source', 'device', 'ad_content',
                   'users', 'new_users', 'sessions', 'pageviews', 
                   'avg_session_duration_sec', 'bounce_rate']]
    
    logger.info("Resumen de métricas:")
    logger.info(f"  - Total sesiones: {df_final['sessions'].sum():,}")
    logger.info(f"  - Total usuarios: {df_final['users'].sum():,}")
    logger.info(f"  - Total pageviews: {df_final['pageviews'].sum():,}")
    
    logger.info(f"Primeras 3 filas procesadas:\n{df_final.head(3)}")
    
    # Guardar staging
    save_csv(df_final, '../02_staging/ga_staging.csv')
    logger.info(f"Guardado: ../02_staging/ga_staging.csv ({len(df_final)} filas)")
    logger.info(f"GA staging creado: {len(df_final)} filas")
    logger.info("==================== FINALIZANDO EXTRACCIÓN GA ====================")
    
    return df_final

def create_sample_ga_data():
    """Crea datos GA de ejemplo para demostración"""
    import random
    
    # Crear datos de ejemplo basados en los creativos RFI
    rfi_df = pd.read_csv('../02_staging/rfi_staging.csv')
    creatives = rfi_df['creative'].unique()
    
    sample_data = []
    for creative in creatives:
        # Extraer tamaño del creativo
        if 'x' in str(creative):
            size = creative.split('_')[0]
        else:
            size = '300x250'
        
        # Crear múltiples registros por creativo
        for _ in range(random.randint(3, 8)):
            sample_data.append({
                'date': '2024-01-01',
                'campaign': 'AR_RFL_Campaign',
                'source': random.choice(['google', 'facebook', '(direct)', 'bing']),
                'device': random.choice(['desktop', 'mobile', 'tablet']),
                'ad_content': size + '_AR_FN',
                'users': random.randint(100, 5000),
                'new_users': random.randint(50, 2000),
                'sessions': random.randint(150, 8000),
                'pageviews': random.randint(200, 12000),
                'avg_session_duration_sec': random.randint(30, 300),
                'bounce_rate': random.uniform(0.1, 0.8)
            })
    
    return pd.DataFrame(sample_data)

def process_real_ga_data(df):
    """Procesa datos GA reales con mapeo correcto de columnas CSV."""
    logger.info("--- INICIANDO PROCESAMIENTO DETALLADO GA ---")
    
    # 1. Limpiar nombres de columnas
    df.columns = df.columns.str.strip()
    logger.info(f"Columnas originales: {list(df.columns)}")
    
    # 2. Mapeo de columnas según el CSV real
    column_mapping = {
        'Source': 'source',
        'Month of Year': 'month_year', 
        'Device Category': 'device',
        'Ad Content': 'ad_content',
        'Sessions': 'sessions',
        'Users': 'users',
        'New Users': 'new_users',
        'Pageviews': 'pageviews',
        'Session Duration': 'session_duration',
        'Calculated AToS': 'avg_session_duration'
    }
    
    # Renombrar columnas que existen
    existing_mapping = {k: v for k, v in column_mapping.items() if k in df.columns}
    df = df.rename(columns=existing_mapping)
    logger.info(f"Columnas renombradas: {existing_mapping}")
    logger.info(f"Columnas después del renombre: {list(df.columns)}")
    
    # 3. Procesar métricas numéricas
    numeric_cols = ['users', 'new_users', 'sessions', 'pageviews']
    for col in numeric_cols:
        if col in df.columns:
            # Limpiar formato numérico (comas como separadores decimales)
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            logger.info(f"Columna {col} convertida - suma total: {df[col].sum()}")
        else:
            df[col] = 0
            logger.warning(f"Columna {col} no encontrada, asignando 0")
    
    # 4. Procesar fechas desde month_year (formato YYYYMM)
    if 'month_year' in df.columns:
        df['date'] = pd.to_datetime(df['month_year'], format='%Y%m', errors='coerce')
        df['date'] = df['date'].dt.strftime('%Y-%m-01')
        logger.info(f"Fechas procesadas desde month_year. Ejemplo: {df['date'].iloc[0] if len(df) > 0 else 'N/A'}")
    else:
        df['date'] = '2024-01-01'
        logger.warning("Columna month_year no encontrada, usando fecha por defecto")
    
    # 5. Procesar duración de sesión
    def parse_duration(duration_str):
        """Convierte duración en formato H:MM:SS o segundos a segundos"""
        if pd.isna(duration_str):
            return 0
        try:
            duration_str = str(duration_str).strip()
            if ':' in duration_str:
                # Formato H:MM:SS o MM:SS
                parts = duration_str.split(':')
                if len(parts) == 3:  # H:MM:SS
                    return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                elif len(parts) == 2:  # MM:SS
                    return int(parts[0]) * 60 + int(parts[1])
            else:
                # Asumir que son segundos
                return float(duration_str.replace(',', '.'))
        except:
            return 0
    
    # Buscar columna de duración
    duration_col = None
    for col in ['session_duration', 'avg_session_duration', 'Session Duration', 'Calculated AToS']:
        if col in df.columns:
            duration_col = col
            break
    
    if duration_col:
        df['avg_session_duration_sec'] = df[duration_col].apply(parse_duration)
        logger.info(f"Duración procesada desde {duration_col}. Promedio: {df['avg_session_duration_sec'].mean():.2f} seg")
    else:
        df['avg_session_duration_sec'] = 0
        logger.warning("No se encontró columna de duración")
    
    # 6. Calcular bounce rate
    df['bounce_rate'] = np.where(
        df['sessions'] > 0, 
        np.maximum(0, 1 - (df['pageviews'] / df['sessions'])), 
        0
    ).clip(0, 1)
    logger.info(f"Bounce rate calculado. Promedio: {df['bounce_rate'].mean():.3f}")
    
    # 7. Crear columna campaign si no existe
    if 'campaign' not in df.columns:
        df['campaign'] = 'GA_Campaign_' + df['source'].astype(str)
        logger.info("Columna campaign creada desde source")
    
    # 8. Rellenar valores faltantes
    df['device'] = df['device'].fillna('desktop')
    df['source'] = df['source'].fillna('unknown')
    df['ad_content'] = df['ad_content'].fillna('Unknown')
    df['campaign'] = df['campaign'].fillna('Unknown')
    
    # 9. Seleccionar columnas finales
    final_cols = ['date', 'campaign', 'source', 'device', 'ad_content', 'users', 
                  'new_users', 'sessions', 'pageviews', 'avg_session_duration_sec', 'bounce_rate']
    
    df_final = df[final_cols].copy()
    
    # 10. Filtrar filas con datos válidos
    df_final = df_final[df_final['sessions'] > 0].copy()
    
    logger.info(f"--- PROCESAMIENTO COMPLETADO ---")
    logger.info(f"Filas finales: {len(df_final)}")
    logger.info(f"Resumen de métricas:")
    logger.info(f"  - Total sesiones: {df_final['sessions'].sum():,}")
    logger.info(f"  - Total usuarios: {df_final['users'].sum():,}")
    logger.info(f"  - Total pageviews: {df_final['pageviews'].sum():,}")
    logger.info(f"Primeras 3 filas procesadas:\n{df_final.head(3).to_string()}")
    
    return df_final

if __name__ == "__main__":
    rfi_data = extract_rfi_data()
    ga_data = extract_ga_data() 