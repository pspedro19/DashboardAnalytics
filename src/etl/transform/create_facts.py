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

def create_fact_ad_performance():
    """Crea tabla de hechos de rendimiento de anuncios"""
    logger.info("Creando fact_ad_performance...")
    project_root = get_project_root()
    
    rfi_file = os.path.join(project_root, 'data', 'processed', 'staging', 'rfi_staging.csv')
    date_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_date.csv')
    campaign_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_campaign.csv')
    site_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_site.csv')
    creative_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_creative.csv')
    placement_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_placement.csv')
    size_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_creative_size.csv')
    
    rfi_df = pd.read_csv(rfi_file)
    dim_date = pd.read_csv(date_file)
    dim_campaign = pd.read_csv(campaign_file)
    dim_site = pd.read_csv(site_file)
    dim_creative = pd.read_csv(creative_file)
    dim_placement = pd.read_csv(placement_file)
    dim_size = pd.read_csv(size_file)
    
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
    
    facts_dir = os.path.join(project_root, 'data', 'dimensional', 'facts')
    os.makedirs(facts_dir, exist_ok=True)
    
    save_csv(fact_final, os.path.join(facts_dir, 'fact_ad_performance.csv'))
    logger.info(f"fact_ad_performance creada: {len(fact_final)} filas")
    return fact_final

def create_fact_web_analytics():
    """Crea tabla de hechos de analítica web"""
    logger.info("Creando fact_web_analytics...")
    project_root = get_project_root()
    
    ga_file = os.path.join(project_root, 'data', 'processed', 'staging', 'ga_staging.csv')
    date_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_date.csv')
    campaign_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_campaign.csv')
    source_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_source.csv')
    device_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_device.csv')
    ad_content_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_ad_content.csv')
    
    ga_df = pd.read_csv(ga_file)
    dim_date = pd.read_csv(date_file)
    dim_campaign = pd.read_csv(campaign_file)
    dim_source = pd.read_csv(source_file)
    dim_device = pd.read_csv(device_file)
    dim_ad_content = pd.read_csv(ad_content_file)
    
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
    
    facts_dir = os.path.join(project_root, 'data', 'dimensional', 'facts')
    os.makedirs(facts_dir, exist_ok=True)
    
    save_csv(fact_final, os.path.join(facts_dir, 'fact_web_analytics.csv'))
    logger.info(f"fact_web_analytics creada: {len(fact_final)} filas")
    return fact_final

if __name__ == "__main__":
    create_fact_ad_performance()
    create_fact_web_analytics() 