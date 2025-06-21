import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.utils import *

logger = setup_logging()

def get_project_root():
    """Get the project root directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

def validate_staging_data():
    """Valida integridad de datos staging"""
    logger.info("Iniciando validación de datos...")
    
    project_root = get_project_root()
    validation_results = []
    
    # Cargar datos
    rfi_file = os.path.join(project_root, 'data', 'processed', 'staging', 'rfi_staging.csv')
    ga_file = os.path.join(project_root, 'data', 'processed', 'staging', 'ga_staging.csv')
    
    rfi_df = pd.read_csv(rfi_file)
    ga_df = pd.read_csv(ga_file)
    
    # Validación 1: Verificar nulos críticos
    logger.info("Validando campos nulos...")
    
    rfi_nulls = rfi_df[['date', 'campaign', 'site', 'creative']].isnull().sum()
    ga_nulls = ga_df[['date', 'campaign', 'source', 'device']].isnull().sum()
    
    validation_results.append("=== VALIDACIÓN DE NULOS ===")
    validation_results.append(f"RFI Nulls:\n{rfi_nulls}")
    validation_results.append(f"\nGA Nulls:\n{ga_nulls}")
    
    # Validación 2: Rangos de valores
    logger.info("Validando rangos de valores...")
    
    validation_results.append("\n=== VALIDACIÓN DE RANGOS ===")
    
    # RFI
    if (rfi_df['impressions'] < 0).any():
        validation_results.append("ADVERTENCIA: Impresiones negativas en RFI")
    if (rfi_df['clicks'] > rfi_df['impressions']).any():
        validation_results.append("ADVERTENCIA: Clicks > Impressions en RFI")
    
    # GA
    if (ga_df['sessions'] < 0).any():
        validation_results.append("ADVERTENCIA: Sesiones negativas en GA")
    if (ga_df['bounce_rate'] > 1).any() or (ga_df['bounce_rate'] < 0).any():
        validation_results.append("ADVERTENCIA: Bounce rate fuera de rango [0,1]")
    
    # Validación 3: Consistencia de fechas
    logger.info("Validando consistencia de fechas...")
    
    rfi_dates = set(rfi_df['date'].unique())
    ga_dates = set(ga_df['date'].unique())
    
    validation_results.append("\n=== VALIDACIÓN DE FECHAS ===")
    validation_results.append(f"Fechas en RFI: {sorted(rfi_dates)}")
    validation_results.append(f"Fechas en GA: {sorted(ga_dates)}")
    validation_results.append(f"Fechas comunes: {sorted(rfi_dates.intersection(ga_dates))}")
    
    # Validación 4: Métricas agregadas
    logger.info("Calculando métricas agregadas...")
    
    validation_results.append("\n=== MÉTRICAS AGREGADAS ===")
    validation_results.append(f"Total Impressions (RFI): {rfi_df['impressions'].sum():,.0f}")
    validation_results.append(f"Total Clicks (RFI): {rfi_df['clicks'].sum():,.0f}")
    validation_results.append(f"CTR Global (RFI): {(rfi_df['clicks'].sum() / rfi_df['impressions'].sum() * 100):.2f}%")
    validation_results.append(f"\nTotal Sessions (GA): {ga_df['sessions'].sum():,.0f}")
    validation_results.append(f"Total Users (GA): {ga_df['users'].sum():,.0f}")
    validation_results.append(f"Avg Bounce Rate (GA): {ga_df['bounce_rate'].mean():.2%}")
    
    # Validación 5: Mapeo Creative-AdContent
    logger.info("Validando mapeo Creative-AdContent...")
    
    rfi_creatives = set(rfi_df['creative'].unique())
    ga_adcontents = set(ga_df['ad_content'].unique())
    
    # Buscar coincidencias parciales
    matches = []
    for creative in rfi_creatives:
        for adcontent in ga_adcontents:
            if any(part in adcontent for part in creative.split('_')[:3]):
                matches.append((creative, adcontent))
    
    validation_results.append("\n=== MAPEO CREATIVE-ADCONTENT ===")
    validation_results.append(f"Creativos únicos (RFI): {len(rfi_creatives)}")
    validation_results.append(f"AdContent únicos (GA): {len(ga_adcontents)}")
    validation_results.append(f"Posibles matches encontrados: {len(matches)}")
    
    # Crear directorio de outputs si no existe
    outputs_dir = os.path.join(project_root, 'data', 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Guardar reporte
    report_file = os.path.join(outputs_dir, 'validation_report.txt')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(validation_results))
    
    logger.info(f"Validación completada. Ver reporte en {report_file}")
    
    return True

if __name__ == "__main__":
    validate_staging_data() 