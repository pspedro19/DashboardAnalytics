import pandas as pd
import numpy as np
import logging
from datetime import datetime
import os

def setup_logging():
    """Configura el sistema de logging"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Crear directorio de logs si no existe
    log_dir = '../06_logs'
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = f'{log_dir}/etl_log_{timestamp}.txt'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def clean_numeric(value):
    """Limpia valores numéricos"""
    if pd.isna(value):
        return 0
    if isinstance(value, str):
        value = value.replace(',', '').replace('%', '')
    try:
        return float(value)
    except:
        return 0

def standardize_date(date_str):
    """Estandariza fechas a formato YYYY-MM-DD"""
    try:
        for fmt in ['%d-%b-%y', '%Y-%m-%d', '%d/%m/%Y']:
            try:
                return pd.to_datetime(date_str, format=fmt).strftime('%Y-%m-%d')
            except:
                continue
        return pd.to_datetime(date_str).strftime('%Y-%m-%d')
    except:
        return None

def create_date_key(date_str):
    """Crea date_key en formato YYYYMMDD"""
    date = pd.to_datetime(date_str)
    return int(date.strftime('%Y%m%d'))

def save_csv(df, path):
    """Guarda DataFrame como CSV con validación"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8')
    logging.info(f"Guardado: {path} ({len(df)} filas)") 