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

def create_date_dimension():
    """Crea dimensión fecha"""
    logger.info("Creando dim_date...")
    project_root = get_project_root()
    
    rfi_file = os.path.join(project_root, 'data', 'processed', 'staging', 'rfi_staging.csv')
    ga_file = os.path.join(project_root, 'data', 'processed', 'staging', 'ga_staging.csv')
    
    rfi_df = pd.read_csv(rfi_file)
    ga_df = pd.read_csv(ga_file)
    
    all_dates = pd.concat([
        pd.to_datetime(rfi_df['date']),
        pd.to_datetime(ga_df['date'])
    ]).unique()
    dim_date = pd.DataFrame({
        'date': pd.to_datetime(all_dates)
    })
    dim_date['date_key'] = dim_date['date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['month'] = dim_date['date'].dt.month
    dim_date['month_name'] = dim_date['date'].dt.strftime('%B')
    dim_date['quarter'] = 'Q' + dim_date['date'].dt.quarter.astype(str)
    dim_date['year'] = dim_date['date'].dt.year
    dim_date['date'] = dim_date['date'].dt.strftime('%Y-%m-%d')
    dim_date = dim_date.sort_values('date_key')
    
    dimensions_dir = os.path.join(project_root, 'data', 'dimensional', 'dimensions')
    os.makedirs(dimensions_dir, exist_ok=True)
    
    save_csv(dim_date, os.path.join(dimensions_dir, 'dim_date.csv'))
    return dim_date

def create_campaign_dimension():
    logger.info("Creando dim_campaign...")
    project_root = get_project_root()
    
    rfi_file = os.path.join(project_root, 'data', 'processed', 'staging', 'rfi_staging.csv')
    ga_file = os.path.join(project_root, 'data', 'processed', 'staging', 'ga_staging.csv')
    
    rfi_df = pd.read_csv(rfi_file)
    ga_df = pd.read_csv(ga_file)
    
    campaigns = pd.concat([
        rfi_df['campaign'],
        ga_df['campaign']
    ]).unique()
    dim_campaign = pd.DataFrame({
        'campaign_key': range(1, len(campaigns) + 1),
        'campaign_name': campaigns
    })
    
    dimensions_dir = os.path.join(project_root, 'data', 'dimensional', 'dimensions')
    os.makedirs(dimensions_dir, exist_ok=True)
    
    save_csv(dim_campaign, os.path.join(dimensions_dir, 'dim_campaign.csv'))
    return dim_campaign

def create_site_dimension():
    logger.info("Creando dim_site...")
    project_root = get_project_root()
    
    rfi_file = os.path.join(project_root, 'data', 'processed', 'staging', 'rfi_staging.csv')
    rfi_df = pd.read_csv(rfi_file)
    
    sites = sorted(rfi_df['site'].unique())
    def categorize_site(site):
        if 'news' in site.lower() or 'akhbar' in site.lower():
            return 'News'
        elif 'sport' in site.lower():
            return 'Sports'
        elif 'game' in site.lower():
            return 'Gaming'
        else:
            return 'General'
    dim_site = pd.DataFrame({
        'site_key': range(1, len(sites) + 1),
        'site_name': sites,
        'site_category': [categorize_site(s) for s in sites]
    })
    
    dimensions_dir = os.path.join(project_root, 'data', 'dimensional', 'dimensions')
    os.makedirs(dimensions_dir, exist_ok=True)
    
    save_csv(dim_site, os.path.join(dimensions_dir, 'dim_site.csv'))
    return dim_site

def create_creative_dimension():
    logger.info("Creando dim_creative...")
    project_root = get_project_root()
    
    rfi_file = os.path.join(project_root, 'data', 'processed', 'staging', 'rfi_staging.csv')
    rfi_df = pd.read_csv(rfi_file)
    
    creatives = sorted(rfi_df['creative'].unique())
    def extract_version(creative):
        if '_v' in creative:
            parts = creative.split('_v')
            if len(parts) > 1:
                return f"v{parts[-1]}"
        return "v1.0"
    dim_creative = pd.DataFrame({
        'creative_key': range(1, len(creatives) + 1),
        'creative_name': creatives,
        'creative_version': [extract_version(c) for c in creatives]
    })
    
    dimensions_dir = os.path.join(project_root, 'data', 'dimensional', 'dimensions')
    os.makedirs(dimensions_dir, exist_ok=True)
    
    save_csv(dim_creative, os.path.join(dimensions_dir, 'dim_creative.csv'))
    return dim_creative

def create_placement_dimension():
    logger.info("Creando dim_placement...")
    project_root = get_project_root()
    
    rfi_file = os.path.join(project_root, 'data', 'processed', 'staging', 'rfi_staging.csv')
    rfi_df = pd.read_csv(rfi_file)
    
    placements = sorted(rfi_df['placement'].unique())
    def get_placement_type(placement):
        if '_HP_' in placement or 'homepage' in placement.lower():
            return 'Homepage'
        elif '_ROS_' in placement:
            return 'Run of Site'
        else:
            return 'Other'
    dim_placement = pd.DataFrame({
        'placement_key': range(1, len(placements) + 1),
        'placement_name': placements,
        'placement_type': [get_placement_type(p) for p in placements]
    })
    
    dimensions_dir = os.path.join(project_root, 'data', 'dimensional', 'dimensions')
    os.makedirs(dimensions_dir, exist_ok=True)
    
    save_csv(dim_placement, os.path.join(dimensions_dir, 'dim_placement.csv'))
    return dim_placement

def create_device_dimension():
    logger.info("Creando dim_device...")
    project_root = get_project_root()
    
    ga_file = os.path.join(project_root, 'data', 'processed', 'staging', 'ga_staging.csv')
    ga_df = pd.read_csv(ga_file)
    
    devices = sorted(ga_df['device'].unique())
    dim_device = pd.DataFrame({
        'device_key': range(1, len(devices) + 1),
        'device_category': devices
    })
    
    dimensions_dir = os.path.join(project_root, 'data', 'dimensional', 'dimensions')
    os.makedirs(dimensions_dir, exist_ok=True)
    
    save_csv(dim_device, os.path.join(dimensions_dir, 'dim_device.csv'))
    return dim_device

def create_source_dimension():
    logger.info("Creando dim_source...")
    project_root = get_project_root()
    
    ga_file = os.path.join(project_root, 'data', 'processed', 'staging', 'ga_staging.csv')
    ga_df = pd.read_csv(ga_file)
    
    sources = sorted(ga_df['source'].unique())
    def categorize_source(source):
        if source in ['google', 'bing', 'yahoo']:
            return 'Search'
        elif source in ['facebook', 'twitter', 'linkedin']:
            return 'Social'
        elif source == '(direct)':
            return 'Direct'
        else:
            return 'Other'
    dim_source = pd.DataFrame({
        'source_key': range(1, len(sources) + 1),
        'source_name': sources,
        'source_type': [categorize_source(s) for s in sources]
    })
    
    dimensions_dir = os.path.join(project_root, 'data', 'dimensional', 'dimensions')
    os.makedirs(dimensions_dir, exist_ok=True)
    
    save_csv(dim_source, os.path.join(dimensions_dir, 'dim_source.csv'))
    return dim_source

def create_ad_content_dimension():
    logger.info("Creando dim_ad_content...")
    project_root = get_project_root()
    
    ga_file = os.path.join(project_root, 'data', 'processed', 'staging', 'ga_staging.csv')
    ga_df = pd.read_csv(ga_file)
    
    ad_contents = sorted(ga_df['ad_content'].unique())
    creative_mapping = {
        '300x250_AR_FN': '300x250_AR_RFL_FN',
        '728x90_AR_FN': '728x90_AR_RFL_FN',
        '160x600_AR_FN': '160x600_AR_RFL_FN'
    }
    dim_ad_content = pd.DataFrame({
        'ad_content_key': range(1, len(ad_contents) + 1),
        'ad_content_name': ad_contents,
        'creative_mapping': [creative_mapping.get(ac, 'NULL') for ac in ad_contents]
    })
    
    dimensions_dir = os.path.join(project_root, 'data', 'dimensional', 'dimensions')
    os.makedirs(dimensions_dir, exist_ok=True)
    
    save_csv(dim_ad_content, os.path.join(dimensions_dir, 'dim_ad_content.csv'))
    return dim_ad_content

def create_creative_size_dimension():
    logger.info("Creando dim_creative_size...")
    project_root = get_project_root()
    
    rfi_file = os.path.join(project_root, 'data', 'processed', 'staging', 'rfi_staging.csv')
    rfi_df = pd.read_csv(rfi_file)
    
    sizes = sorted(rfi_df['size'].unique())
    dim_size = []
    for i, size in enumerate(sizes, 1):
        if 'x' in str(size):
            width, height = size.split('x')
            dim_size.append({
                'size_key': i,
                'dimensions': size,
                'width': int(width),
                'height': int(height)
            })
        else:
            dim_size.append({
                'size_key': i,
                'dimensions': size,
                'width': 0,
                'height': 0
            })
    dim_creative_size = pd.DataFrame(dim_size)
    
    dimensions_dir = os.path.join(project_root, 'data', 'dimensional', 'dimensions')
    os.makedirs(dimensions_dir, exist_ok=True)
    
    save_csv(dim_creative_size, os.path.join(dimensions_dir, 'dim_creative_size.csv'))
    return dim_creative_size

def create_bridge_table():
    logger.info("Creando bridge_creative_adcontent...")
    project_root = get_project_root()
    
    creative_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_creative.csv')
    ad_content_file = os.path.join(project_root, 'data', 'dimensional', 'dimensions', 'dim_ad_content.csv')
    
    dim_creative = pd.read_csv(creative_file)
    dim_ad_content = pd.read_csv(ad_content_file)
    
    mappings = [
        ('160x600_AR_RFL_FN', '160x600_AR_FN', 1.0),
        ('728x90_AR_RFL_FN', '728x90_AR_FN', 1.0),
        ('300x250_AR_RFL_FN', '300x250_AR_FN', 1.0)
    ]
    bridge_data = []
    for creative_name, ad_content_name, confidence in mappings:
        creative_key = dim_creative[dim_creative['creative_name'] == creative_name]['creative_key'].values
        ad_content_key = dim_ad_content[dim_ad_content['ad_content_name'] == ad_content_name]['ad_content_key'].values
        if len(creative_key) > 0 and len(ad_content_key) > 0:
            bridge_data.append({
                'creative_key': creative_key[0],
                'ad_content_key': ad_content_key[0],
                'confidence_score': confidence
            })
    bridge_df = pd.DataFrame(bridge_data)
    
    bridge_dir = os.path.join(project_root, 'data', 'dimensional', 'bridge')
    os.makedirs(bridge_dir, exist_ok=True)
    
    save_csv(bridge_df, os.path.join(bridge_dir, 'bridge_creative_adcontent.csv'))
    return bridge_df

def create_all_dimensions():
    create_date_dimension()
    create_campaign_dimension()
    create_site_dimension()
    create_creative_dimension()
    create_placement_dimension()
    create_device_dimension()
    create_source_dimension()
    create_ad_content_dimension()
    create_creative_size_dimension()
    create_bridge_table()
    logger.info("Todas las dimensiones creadas exitosamente")

if __name__ == "__main__":
    create_all_dimensions() 