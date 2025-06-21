import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.utils import *

logger = setup_logging()

def get_project_root():
    """Get the project root directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

def calculate_summary_kpis():
    logger.info("Calculando KPIs resumen...")
    project_root = get_project_root()
    
    fact_ad_file = os.path.join(project_root, 'data', 'dimensional', 'facts', 'fact_ad_performance.csv')
    fact_web_file = os.path.join(project_root, 'data', 'dimensional', 'facts', 'fact_web_analytics.csv')
    
    fact_ad = pd.read_csv(fact_ad_file)
    fact_web = pd.read_csv(fact_web_file)
    
    total_impressions = fact_ad['impressions'].sum()
    total_clicks = fact_ad['clicks'].sum()
    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    total_sessions = fact_web['sessions'].sum()
    total_users = fact_web['users'].sum()
    total_pageviews = fact_web['pageviews'].sum()
    avg_session_duration = fact_web['avg_session_duration_sec'].mean()
    avg_bounce_rate = fact_web['bounce_rate'].mean()
    click_to_session_rate = (total_sessions / total_clicks * 100) if total_clicks > 0 else 0
    summary_kpis = pd.DataFrame([{
        'metric': 'Total Impressions',
        'value': f"{total_impressions:,.0f}",
        'category': 'Advertising'
    }, {
        'metric': 'Total Clicks',
        'value': f"{total_clicks:,.0f}",
        'category': 'Advertising'
    }, {
        'metric': 'CTR (%)',
        'value': f"{ctr:.2f}%",
        'category': 'Advertising'
    }, {
        'metric': 'Total Sessions',
        'value': f"{total_sessions:,.0f}",
        'category': 'Web Analytics'
    }, {
        'metric': 'Total Users',
        'value': f"{total_users:,.0f}",
        'category': 'Web Analytics'
    }, {
        'metric': 'Total Pageviews',
        'value': f"{total_pageviews:,.0f}",
        'category': 'Web Analytics'
    }, {
        'metric': 'Avg Session Duration (sec)',
        'value': f"{avg_session_duration:.0f}",
        'category': 'Web Analytics'
    }, {
        'metric': 'Avg Bounce Rate (%)',
        'value': f"{avg_bounce_rate:.1%}",
        'category': 'Web Analytics'
    }, {
        'metric': 'Click to Session Rate (%)',
        'value': f"{click_to_session_rate:.1f}%",
        'category': 'Conversion'
    }])
    
    outputs_dir = os.path.join(project_root, 'data', 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    
    save_csv(summary_kpis, os.path.join(outputs_dir, 'kpi_summary.csv'))
    return summary_kpis

def calculate_kpis_by_site():
    logger.info("Calculando KPIs por sitio...")
    project_root = get_project_root()
    
    fact_ad_file = os.path.join(project_root, 'data', 'dimensional', 'facts', 'fact_ad_performance.csv')
    site_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_site.csv')
    
    fact_ad = pd.read_csv(fact_ad_file)
    dim_site = pd.read_csv(site_file)
    
    df = fact_ad.merge(dim_site, on='site_key')
    kpis_by_site = df.groupby(['site_name', 'site_category']).agg({
        'impressions': 'sum',
        'clicks': 'sum'
    }).reset_index()
    kpis_by_site['ctr'] = (kpis_by_site['clicks'] / kpis_by_site['impressions'] * 100)
    kpis_by_site['ctr'] = kpis_by_site['ctr'].round(2)
    kpis_by_site = kpis_by_site.sort_values('impressions', ascending=False)
    
    outputs_dir = os.path.join(project_root, 'data', 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    
    save_csv(kpis_by_site, os.path.join(outputs_dir, 'kpi_by_site.csv'))
    return kpis_by_site

def calculate_kpis_by_creative():
    logger.info("Calculando KPIs por creativo...")
    project_root = get_project_root()
    
    fact_ad_file = os.path.join(project_root, 'data', 'dimensional', 'facts', 'fact_ad_performance.csv')
    fact_web_file = os.path.join(project_root, 'data', 'dimensional', 'facts', 'fact_web_analytics.csv')
    creative_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_creative.csv')
    ad_content_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_ad_content.csv')
    
    fact_ad = pd.read_csv(fact_ad_file)
    fact_web = pd.read_csv(fact_web_file)
    dim_creative = pd.read_csv(creative_file)
    dim_ad_content = pd.read_csv(ad_content_file)
    
    # Check if bridge table exists and has data
    bridge_file = os.path.join(project_root, 'data', 'dimensional', 'bridge', 'bridge_creative_adcontent.csv')
    try:
        bridge = pd.read_csv(bridge_file)
        if len(bridge) == 0:
            logger.warning("Bridge table is empty, creating simplified creative KPIs without web analytics data")
            bridge = None
    except Exception as e:
        logger.warning(f"Could not read bridge table: {e}, creating simplified creative KPIs")
        bridge = None
    
    # Calculate ad performance KPIs
    ad_kpis = fact_ad.merge(dim_creative, on='creative_key')
    ad_kpis = ad_kpis.groupby(['creative_key', 'creative_name']).agg({
        'impressions': 'sum',
        'clicks': 'sum'
    }).reset_index()
    ad_kpis['ctr'] = (ad_kpis['clicks'] / ad_kpis['impressions'] * 100).round(2)
    
    if bridge is not None and len(bridge) > 0:
        # Full analysis with bridge table
        web_kpis = fact_web.merge(dim_ad_content, on='ad_content_key')
        web_kpis = web_kpis.groupby(['ad_content_key', 'ad_content_name']).agg({
            'sessions': 'sum',
            'users': 'sum',
            'bounce_rate': 'mean'
        }).reset_index()
        creative_web = bridge.merge(web_kpis, on='ad_content_key')
        creative_complete = ad_kpis.merge(creative_web, on='creative_key', how='left')
        creative_complete['click_to_session_rate'] = (
            creative_complete['sessions'] / creative_complete['clicks'] * 100
        ).fillna(0)
        final_cols = ['creative_name', 'impressions', 'clicks', 'ctr', 
                      'sessions', 'users', 'bounce_rate', 'click_to_session_rate']
        creative_complete = creative_complete[final_cols].round(2)
    else:
        # Simplified analysis without bridge table
        logger.info("Using simplified creative KPIs (ad performance only)")
        final_cols = ['creative_name', 'impressions', 'clicks', 'ctr']
        creative_complete = ad_kpis[final_cols].round(2)
    
    outputs_dir = os.path.join(project_root, 'data', 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    
    save_csv(creative_complete, os.path.join(outputs_dir, 'kpi_by_creative.csv'))
    return creative_complete

def calculate_kpis_by_device():
    logger.info("Calculando KPIs por dispositivo...")
    project_root = get_project_root()
    
    fact_web_file = os.path.join(project_root, 'data', 'dimensional', 'facts', 'fact_web_analytics.csv')
    device_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_device.csv')
    
    fact_web = pd.read_csv(fact_web_file)
    dim_device = pd.read_csv(device_file)
    
    df = fact_web.merge(dim_device, on='device_key')
    kpis_by_device = df.groupby('device_category').agg({
        'users': 'sum',
        'sessions': 'sum',
        'pageviews': 'sum',
        'avg_session_duration_sec': 'mean',
        'bounce_rate': 'mean'
    }).reset_index()
    kpis_by_device['pages_per_session'] = (
        kpis_by_device['pageviews'] / kpis_by_device['sessions']
    ).round(2)
    kpis_by_device['avg_session_duration_sec'] = kpis_by_device['avg_session_duration_sec'].round(0)
    kpis_by_device['bounce_rate'] = (kpis_by_device['bounce_rate'] * 100).round(1)
    
    outputs_dir = os.path.join(project_root, 'data', 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    
    save_csv(kpis_by_device, os.path.join(outputs_dir, 'kpi_by_device.csv'))
    return kpis_by_device

if __name__ == "__main__":
    calculate_summary_kpis()
    calculate_kpis_by_site()
    calculate_kpis_by_creative()
    calculate_kpis_by_device()
    logger.info("Todos los KPIs calculados exitosamente") 