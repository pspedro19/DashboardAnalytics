import pandas as pd
from utils import *

logger = setup_logging()

def create_date_dimension():
    """Crea dimensión fecha"""
    logger.info("Creando dim_date...")
    rfi_df = pd.read_csv('../02_staging/rfi_staging.csv')
    ga_df = pd.read_csv('../02_staging/ga_staging.csv')
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
    save_csv(dim_date, '../03_dimensional_model/dimensions/dim_date.csv')
    return dim_date

def create_campaign_dimension():
    logger.info("Creando dim_campaign...")
    rfi_df = pd.read_csv('../02_staging/rfi_staging.csv')
    ga_df = pd.read_csv('../02_staging/ga_staging.csv')
    campaigns = pd.concat([
        rfi_df['campaign'],
        ga_df['campaign']
    ]).unique()
    dim_campaign = pd.DataFrame({
        'campaign_key': range(1, len(campaigns) + 1),
        'campaign_name': campaigns
    })
    save_csv(dim_campaign, '../03_dimensional_model/dimensions/dim_campaign.csv')
    return dim_campaign

def create_site_dimension():
    logger.info("Creando dim_site...")
    rfi_df = pd.read_csv('../02_staging/rfi_staging.csv')
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
    save_csv(dim_site, '../03_dimensional_model/dimensions/dim_site.csv')
    return dim_site

def create_creative_dimension():
    logger.info("Creando dim_creative...")
    rfi_df = pd.read_csv('../02_staging/rfi_staging.csv')
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
    save_csv(dim_creative, '../03_dimensional_model/dimensions/dim_creative.csv')
    return dim_creative

def create_placement_dimension():
    logger.info("Creando dim_placement...")
    rfi_df = pd.read_csv('../02_staging/rfi_staging.csv')
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
    save_csv(dim_placement, '../03_dimensional_model/dimensions/dim_placement.csv')
    return dim_placement

def create_device_dimension():
    logger.info("Creando dim_device...")
    ga_df = pd.read_csv('../02_staging/ga_staging.csv')
    devices = sorted(ga_df['device'].unique())
    dim_device = pd.DataFrame({
        'device_key': range(1, len(devices) + 1),
        'device_category': devices
    })
    save_csv(dim_device, '../03_dimensional_model/dimensions/dim_device.csv')
    return dim_device

def create_source_dimension():
    logger.info("Creando dim_source...")
    ga_df = pd.read_csv('../02_staging/ga_staging.csv')
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
    save_csv(dim_source, '../03_dimensional_model/dimensions/dim_source.csv')
    return dim_source

def create_ad_content_dimension():
    logger.info("Creando dim_ad_content...")
    ga_df = pd.read_csv('../02_staging/ga_staging.csv')
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
    save_csv(dim_ad_content, '../03_dimensional_model/dimensions/dim_ad_content.csv')
    return dim_ad_content

def create_creative_size_dimension():
    logger.info("Creando dim_creative_size...")
    rfi_df = pd.read_csv('../02_staging/rfi_staging.csv')
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
    save_csv(dim_creative_size, '../03_dimensional_model/dimensions/dim_creative_size.csv')
    return dim_creative_size

def create_bridge_table():
    logger.info("Creando bridge_creative_adcontent...")
    dim_creative = pd.read_csv('../03_dimensional_model/dimensions/dim_creative.csv')
    dim_ad_content = pd.read_csv('../03_dimensional_model/dimensions/dim_ad_content.csv')
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
    save_csv(bridge_df, '../03_dimensional_model/bridge/bridge_creative_adcontent.csv')
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