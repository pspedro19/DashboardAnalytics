# Marketing Analytics - Power BI Setup Guide

## Project Summary

This project consolidates and harmonizes data from two PGD datasets:
- **PGD Dataset 1**: Advertising performance data
- **PGD Dataset 2**: Web behavior data

## Quick Start

1. **Run ETL**: Execute the ETL pipeline
2. **Connect to Power BI**: Use generated tables in `data/dimensional/`

## Data Structure for Power BI

### Main Tables (Facts)
```
data/dimensional/facts/
├── fact_ad_performance.csv    # Advertising performance
└── fact_web_analytics.csv     # Web metrics
```

### Dimensions
```
data/dimensional/dimensions/
├── dim_date.csv              # Dates
├── dim_campaign.csv          # Campaigns
├── dim_site.csv             # Websites
├── dim_creative.csv         # Creatives
├── dim_placement.csv        # Placements
├── dim_device.csv           # Devices
├── dim_source.csv           # Traffic sources
├── dim_ad_content.csv       # Ad content
└── dim_creative_size.csv    # Creative sizes
```

### Bridge Table
```
data/dimensional/bridge/
└── bridge_creative_adcontent.csv  # Creative-web analytics mapping
```

## Power BI Connection

### 1. Import Data
1. Open Power BI Desktop
2. **Get Data** → **Text/CSV**
3. Select files from `data/dimensional/`

### 2. Establish Relationships
```
fact_ad_performance ↔ dim_date (date_key)
fact_ad_performance ↔ dim_campaign (campaign_key)
fact_ad_performance ↔ dim_site (site_key)
fact_ad_performance ↔ dim_creative (creative_key)
fact_ad_performance ↔ dim_placement (placement_key)
fact_ad_performance ↔ dim_creative_size (size_key)

fact_web_analytics ↔ dim_date (date_key)
fact_web_analytics ↔ dim_campaign (campaign_key)
fact_web_analytics ↔ dim_source (source_key)
fact_web_analytics ↔ dim_device (device_key)
fact_web_analytics ↔ dim_ad_content (ad_content_key)
```

### 3. Pre-calculated KPIs
The following KPIs are already calculated in `data/outputs/`:
- `kpi_summary.csv` - Main metrics
- `kpi_by_site.csv` - Performance by site
- `kpi_by_creative.csv` - Performance by creative
- `kpi_by_device.csv` - Performance by device

## Key Metrics

### Advertising (PGD Dataset 1)
- **Impressions**: `fact_ad_performance[impressions]`
- **Clicks**: `fact_ad_performance[clicks]`
- **CTR**: `fact_ad_performance[clicks] / fact_ad_performance[impressions]`

### Web Analytics (PGD Dataset 2)
- **Users**: `fact_web_analytics[users]`
- **Sessions**: `fact_web_analytics[sessions]`
- **Pageviews**: `fact_web_analytics[pageviews]`
- **Bounce Rate**: `fact_web_analytics[bounce_rate]`
- **Session Duration**: `fact_web_analytics[avg_session_duration_sec]`

### Conversion
- **Click to Session Rate**: `fact_web_analytics[sessions] / fact_ad_performance[clicks]`

## Visualization Suggestions

### Main Dashboard
1. **Cards**: Main KPIs (CTR, Impressions, Clicks)
2. **Bar Chart**: Top 10 sites by impressions
3. **Line Chart**: CTR by date
4. **Heat Map**: CTR by site and creative

### Device Analysis
1. **Pie Chart**: User distribution by device
2. **Bar Chart**: Bounce rate by device
3. **Line Chart**: Session duration by device

### Creative Analysis
1. **Bar Chart**: CTR by creative
2. **Scatter Plot**: Impressions vs Clicks
3. **Table**: Detailed performance by creative

## Automatic Updates

### Configure Refresh
1. **File** → **Options and settings** → **Refresh settings**
2. **Add path**: `C:\path\to\DashboardAnalytics\data\dimensional\`
3. **Schedule refresh**: Daily or as needed

### Complete Automation
1. Schedule ETL pipeline with Task Scheduler
2. Configure Power BI to refresh automatically
3. Data will update without manual intervention

