#!/usr/bin/env python
"""
Script principal para ejecutar el ETL completo de Marketing Analytics
"""
import sys
import os
import time
from datetime import datetime
from utils import setup_logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import extract_and_clean
import validate_data
import create_dimensions
import create_facts
import calculate_kpis
import generate_analysis_report

def main():
    start_time = time.time()
    logger = setup_logging()
    logger.info("=" * 50)
    logger.info("INICIANDO ETL DE MARKETING ANALYTICS")
    logger.info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)
    try:
        logger.info("\n[PASO 1/5] Extracción y limpieza de datos")
        extract_and_clean.extract_rfi_data()
        extract_and_clean.extract_ga_data()
        
        logger.info("\n[PASO 2/5] Validación de datos")
        validate_data.validate_staging_data()
        
        logger.info("\n[PASO 3/5] Creación de dimensiones")
        create_dimensions.create_all_dimensions()
        
        logger.info("\n[PASO 4/5] Creación de tablas de hechos")
        create_facts.create_fact_ad_performance()
        create_facts.create_fact_web_analytics()
        
        logger.info("\n[PASO 5/5] Cálculo de KPIs")
        calculate_kpis.calculate_summary_kpis()
        calculate_kpis.calculate_kpis_by_site()
        calculate_kpis.calculate_kpis_by_creative()
        calculate_kpis.calculate_kpis_by_device()
        
        logger.info("\n[PASO FINAL] Generación de reporte de análisis")
        generate_analysis_report.generate_analysis_report()
        
        elapsed_time = time.time() - start_time
        logger.info("\n" + "=" * 50)
        logger.info("ETL COMPLETADO EXITOSAMENTE")
        logger.info(f"Tiempo total: {elapsed_time:.2f} segundos")
        logger.info("=" * 50)
        print("\n📁 ARCHIVOS GENERADOS:")
        print("├── 02_staging/           # Datos limpios")
        print("├── 03_dimensional_model/ # Modelo Kimball")
        print("│   ├── dimensions/       # 9 dimensiones")
        print("│   ├── bridge/          # Tabla puente")
        print("│   └── facts/           # 2 tablas de hechos")
        print("├── 05_kpi_outputs/      # KPIs calculados")
        print("│   ├── kpi_summary.csv  # KPIs principales")
        print("│   ├── kpi_by_site.csv  # KPIs por sitio")
        print("│   ├── kpi_by_creative.csv # KPIs por creativo")
        print("│   ├── kpi_by_device.csv # KPIs por dispositivo")
        print("│   ├── analysis_report.txt # Reporte completo")
        print("│   └── executive_summary.csv # Resumen ejecutivo")
        print("└── 06_logs/            # Logs de ejecución")
        print("\n🎯 LISTO PARA POWER BI:")
        print("• Conecta las tablas de facts/ y dimensions/")
        print("• Usa los KPIs de 05_kpi_outputs/ para métricas")
        print("• Consulta analysis_report.txt para insights")
        return True
    except Exception as e:
        logger.error(f"ERROR EN ETL: {str(e)}")
        raise
if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 