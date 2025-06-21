import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.utils import setup_logging

logger = setup_logging()

def get_project_root():
    """Get the project root directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

def generate_analysis_report():
    """Genera reporte de análisis con conclusiones"""
    logger.info("Generando reporte de análisis...")
    
    project_root = get_project_root()
    
    # Cargar KPIs
    summary_file = os.path.join(project_root, 'data', 'outputs', 'kpi_summary.csv')
    site_file = os.path.join(project_root, 'data', 'outputs', 'kpi_by_site.csv')
    creative_file = os.path.join(project_root, 'data', 'outputs', 'kpi_by_creative.csv')
    device_file = os.path.join(project_root, 'data', 'outputs', 'kpi_by_device.csv')
    
    summary_kpis = pd.read_csv(summary_file)
    site_kpis = pd.read_csv(site_file)
    creative_kpis = pd.read_csv(creative_file)
    device_kpis = pd.read_csv(device_file)
    
    # Cargar datos de staging para análisis adicional
    rfi_file = os.path.join(project_root, 'data', 'processed', 'staging', 'rfi_staging.csv')
    ga_file = os.path.join(project_root, 'data', 'processed', 'staging', 'ga_staging.csv')
    
    rfi_staging = pd.read_csv(rfi_file)
    ga_staging = pd.read_csv(ga_file)
    
    report = []
    report.append("=" * 80)
    report.append("REPORTE DE ANÁLISIS DE MARKETING ANALYTICS")
    report.append(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 80)
    
    # 1. RESUMEN EJECUTIVO
    report.append("\nRESUMEN EJECUTIVO")
    report.append("-" * 40)
    
    total_impressions = float(summary_kpis[summary_kpis['metric'] == 'Total Impressions']['value'].iloc[0].replace(',', ''))
    total_clicks = float(summary_kpis[summary_kpis['metric'] == 'Total Clicks']['value'].iloc[0].replace(',', ''))
    ctr = float(summary_kpis[summary_kpis['metric'] == 'CTR (%)']['value'].iloc[0].replace('%', ''))
    
    report.append(f"• Impresiones totales: {total_impressions:,.0f}")
    report.append(f"• Clicks totales: {total_clicks:,.0f}")
    report.append(f"• CTR promedio: {ctr:.2f}%")
    
    # 2. ANÁLISIS POR SITIO
    report.append("\nANÁLISIS POR SITIO")
    report.append("-" * 40)
    
    # Top 5 sitios por impresiones
    top_sites = site_kpis.nlargest(5, 'impressions')
    report.append("Top 5 sitios por impresiones:")
    for _, row in top_sites.iterrows():
        report.append(f"  • {row['site_name']}: {row['impressions']:,.0f} impresiones, CTR: {row['ctr']:.2f}%")
    
    # Mejor CTR
    best_ctr_site = site_kpis.nlargest(1, 'ctr').iloc[0]
    report.append(f"\nMejor CTR: {best_ctr_site['site_name']} ({best_ctr_site['ctr']:.2f}%)")
    
    # 3. ANÁLISIS POR CREATIVO
    report.append("\nANÁLISIS POR CREATIVO")
    report.append("-" * 40)
    
    if 'ctr' in creative_kpis.columns:
        best_creative = creative_kpis.nlargest(1, 'ctr').iloc[0]
        report.append(f"Mejor creativo por CTR: {best_creative['creative_name']} ({best_creative['ctr']:.2f}%)")
        
        # Análisis por tamaño
        creative_kpis['size'] = creative_kpis['creative_name'].str.extract(r'(\d+x\d+)')
        if 'size' in creative_kpis.columns:
            size_performance = creative_kpis.groupby('size')['ctr'].mean().sort_values(ascending=False)
            report.append("\nRendimiento por tamaño de creativo:")
            for size, ctr in size_performance.items():
                if pd.notna(size):
                    report.append(f"  • {size}: {ctr:.2f}% CTR promedio")
    
    # 4. ANÁLISIS POR DISPOSITIVO
    report.append("\nANÁLISIS POR DISPOSITIVO")
    report.append("-" * 40)
    
    if len(device_kpis) > 0:
        for _, row in device_kpis.iterrows():
            report.append(f"• {row['device_category']}: {row['users']:,.0f} usuarios, {row['sessions']:,.0f} sesiones")
            if row['sessions'] > 0:
                report.append(f"  - Duración promedio: {row['avg_session_duration_sec']:.0f}s")
                report.append(f"  - Bounce rate: {row['bounce_rate']:.1f}%")
    
    # 5. CONCLUSIONES
    report.append("\nCONCLUSIONES")
    report.append("-" * 40)
    
    # Análisis de rendimiento general
    if ctr > 0.5:
        report.append("El CTR general es BUENO (>0.5%), indicando que los anuncios son relevantes")
    elif ctr > 0.2:
        report.append("El CTR general es MODERADO (0.2-0.5%), hay espacio para mejora")
    else:
        report.append("El CTR general es BAJO (<0.2%), requiere optimización urgente")
    
    # Análisis de distribución de impresiones
    top_3_sites_share = top_sites['impressions'].sum() / total_impressions * 100
    report.append(f"Los 3 principales sitios concentran el {top_3_sites_share:.1f}% de las impresiones")
    
    if top_3_sites_share > 70:
        report.append("Alta concentración en pocos sitios - considerar diversificación")
    else:
        report.append("Buena distribución de impresiones entre sitios")
    
    # Recomendaciones
    report.append("\nRECOMENDACIONES")
    report.append("-" * 40)
    
    # Identificar sitios con bajo rendimiento
    low_performing_sites = site_kpis[site_kpis['ctr'] < 0.1]
    if len(low_performing_sites) > 0:
        report.append("Sitios con bajo rendimiento (CTR < 0.1%):")
        for _, row in low_performing_sites.iterrows():
            report.append(f"  • {row['site_name']}: {row['ctr']:.2f}% CTR")
        report.append("  → Considerar pausar o optimizar estos sitios")
    
    # Identificar oportunidades
    high_volume_low_ctr = site_kpis[(site_kpis['impressions'] > 1000000) & (site_kpis['ctr'] < 0.15)]
    if len(high_volume_low_ctr) > 0:
        report.append("\nOportunidades de optimización (alto volumen, CTR mejorable):")
        for _, row in high_volume_low_ctr.iterrows():
            report.append(f"  • {row['site_name']}: {row['impressions']:,.0f} impresiones, {row['ctr']:.2f}% CTR")
        report.append("  → Priorizar optimización de creativos para estos sitios")
    
    # Guardar reporte
    outputs_dir = os.path.join(project_root, 'data', 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    
    report_path = os.path.join(outputs_dir, 'analysis_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    logger.info(f"Reporte de análisis guardado en: {report_path}")
    
    # También crear resumen ejecutivo en CSV
    executive_summary = pd.DataFrame([{
        'metric': 'Total Impressions',
        'value': total_impressions,
        'insight': 'Volumen total de campaña'
    }, {
        'metric': 'Total Clicks', 
        'value': total_clicks,
        'insight': 'Engagement total'
    }, {
        'metric': 'CTR Average',
        'value': ctr,
        'insight': 'Efectividad general de anuncios'
    }, {
        'metric': 'Top Site Share',
        'value': top_3_sites_share,
        'insight': 'Concentración en principales sitios'
    }, {
        'metric': 'Low Performing Sites',
        'value': len(low_performing_sites),
        'insight': 'Sitios que requieren optimización'
    }])
    
    executive_file = os.path.join(outputs_dir, 'executive_summary.csv')
    executive_summary.to_csv(executive_file, index=False)
    logger.info("Resumen ejecutivo guardado en CSV")
    
    return report

if __name__ == "__main__":
    generate_analysis_report() 