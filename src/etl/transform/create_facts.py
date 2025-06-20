import pandas as pd
from utils import *

logger = setup_logging()

def create_fact_ad_performance():
    """Crea tabla de hechos de rendimiento de anuncios"""
    logger.info("Creando fact_ad_performance...")
    rfi_df = pd.read_csv('../02_staging/rfi_staging.csv')
    dim_date = pd.read_csv('../03_dimensional_model/dimensions/dim_date.csv')
    dim_campaign = pd.read_csv('../03_dimensional_model/dimensions/dim_campaign.csv')
    dim_site = pd.read_csv('../03_dimensional_model/dimensions/dim_site.csv')
    dim_creative = pd.read_csv('../03_dimensional_model/dimensions/dim_creative.csv')
    dim_placement = pd.read_csv('../03_dimensional_model/dimensions/dim_placement.csv')
    dim_size = pd.read_csv('../03_dimensional_model/dimensions/dim_creative_size.csv')
    fact = rfi_df.copy()
    fact = fact.merge(dim_date[['date', 'date_key']], on='date', how='left')
    fact = fact.merge(dim_campaign[['campaign_name', 'campaign_key']], 
                      left_on='campaign', right_on='campaign_name', how='left')
    fact = fact.merge(dim_site[['site_name', 'site_key']], 
                      left_on='site', right_on='site_name', how='left')
    fact = fact.merge(dim_creative[['creative_name', 'creative_key']], 
                      left_on='creative', right_on='creative_name', how='left')
    fact = fact.merge(dim_placement[['placement_name', 'placement_key']], 
                      left_on='placement', right_on='placement_name', how='left')
    fact = fact.merge(dim_size[['dimensions', 'size_key']], 
                      left_on='size', right_on='dimensions', how='left')
    fact_final = fact[['date_key', 'campaign_key', 'site_key', 'creative_key', 
                       'placement_key', 'size_key', 'impressions', 'clicks']]
    numeric_cols = ['impressions', 'clicks']
    for col in numeric_cols:
        fact_final[col] = pd.to_numeric(fact_final[col], errors='coerce').fillna(0)
    save_csv(fact_final, '../03_dimensional_model/facts/fact_ad_performance.csv')
    logger.info(f"fact_ad_performance creada: {len(fact_final)} filas")
    return fact_final

def create_fact_web_analytics():
    """Crea tabla de hechos de analítica web"""
    logger.info("Creando fact_web_analytics...")
    ga_df = pd.read_csv('../02_staging/ga_staging.csv')
    dim_date = pd.read_csv('../03_dimensional_model/dimensions/dim_date.csv')
    dim_campaign = pd.read_csv('../03_dimensional_model/dimensions/dim_campaign.csv')
    dim_source = pd.read_csv('../03_dimensional_model/dimensions/dim_source.csv')
    dim_device = pd.read_csv('../03_dimensional_model/dimensions/dim_device.csv')
    dim_ad_content = pd.read_csv('../03_dimensional_model/dimensions/dim_ad_content.csv')
    fact = ga_df.copy()
    fact = fact.merge(dim_date[['date', 'date_key']], on='date', how='left')
    fact = fact.merge(dim_campaign[['campaign_name', 'campaign_key']], 
                      left_on='campaign', right_on='campaign_name', how='left')
    fact = fact.merge(dim_source[['source_name', 'source_key']], 
                      left_on='source', right_on='source_name', how='left')
    fact = fact.merge(dim_device[['device_category', 'device_key']], 
                      left_on='device', right_on='device_category', how='left')
    fact = fact.merge(dim_ad_content[['ad_content_name', 'ad_content_key']], 
                      left_on='ad_content', right_on='ad_content_name', how='left')
    fact_final = fact[['date_key', 'campaign_key', 'source_key', 'device_key', 
                       'ad_content_key', 'users', 'new_users', 'sessions', 
                       'pageviews', 'avg_session_duration_sec', 'bounce_rate']]
    numeric_cols = ['users', 'new_users', 'sessions', 'pageviews', 
                    'avg_session_duration_sec', 'bounce_rate']
    for col in numeric_cols:
        fact_final[col] = pd.to_numeric(fact_final[col], errors='coerce').fillna(0)
    save_csv(fact_final, '../03_dimensional_model/facts/fact_web_analytics.csv')
    logger.info(f"fact_web_analytics creada: {len(fact_final)} filas")
    return fact_final

if __name__ == "__main__":
    create_fact_ad_performance()
    create_fact_web_analytics() 