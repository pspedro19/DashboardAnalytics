# Data Model Documentation - Kimball Star Schema

## Overview
This document provides detailed information about the Kimball star schema implementation in the Dashboard Analytics system.

![Kimball Star Model](assets/kimball_star_model.png)

## Architecture Overview

The data model follows the Kimball methodology for dimensional modeling, providing:
- **Optimal Query Performance**: Star schema design for fast analytical queries
- **Business User Accessibility**: Intuitive structure for business intelligence
- **Scalability**: Designed to handle large volumes of data
- **Flexibility**: Easy to extend with new dimensions and facts

## Dimension Tables

### 1. Date Dimension
**Purpose**: Temporal analysis and time-based reporting

**Key Attributes**:
- `date_key` (Primary Key)
- `date` (Full date)
- `day_of_week`
- `day_of_month`
- `month`
- `quarter`
- `year`
- `fiscal_year`
- `is_weekend`
- `is_holiday`

**Slowly Changing**: No (Type 1)

### 2. Site Dimension
**Purpose**: Advertising site information and configuration

**Key Attributes**:
- `site_key` (Primary Key)
- `site_id`
- `site_name`
- `site_category`
- `site_quality_score`
- `is_active`
- `effective_date`
- `expiration_date`
- `current_flag`

**Slowly Changing**: Yes (Type 2) - Tracks site configuration changes

### 3. Creative Dimension
**Purpose**: Ad creative details and version tracking

**Key Attributes**:
- `creative_key` (Primary Key)
- `creative_id`
- `creative_name`
- `creative_type`
- `creative_size`
- `creative_format`
- `creative_version`
- `effective_date`
- `expiration_date`
- `current_flag`

**Slowly Changing**: Yes (Type 2) - Version control for creatives

### 4. Device Dimension
**Purpose**: Device and platform information

**Key Attributes**:
- `device_key` (Primary Key)
- `device_type`
- `device_category`
- `operating_system`
- `browser`
- `screen_resolution`
- `is_mobile`

**Slowly Changing**: No (Type 1)

### 5. Geographic Dimension
**Purpose**: Location-based analysis

**Key Attributes**:
- `geo_key` (Primary Key)
- `country`
- `region`
- `city`
- `postal_code`
- `timezone`
- `latitude`
- `longitude`

**Slowly Changing**: No (Type 1)

### 6. Campaign Dimension
**Purpose**: Campaign hierarchy and metadata

**Key Attributes**:
- `campaign_key` (Primary Key)
- `campaign_id`
- `campaign_name`
- `campaign_type`
- `campaign_category`
- `start_date`
- `end_date`
- `budget`
- `effective_date`
- `expiration_date`
- `current_flag`

**Slowly Changing**: Yes (Type 2) - Campaign evolution tracking

### 7. User Dimension
**Purpose**: User behavior and segmentation

**Key Attributes**:
- `user_key` (Primary Key)
- `user_id`
- `user_type`
- `user_segment`
- `registration_date`
- `last_activity_date`
- `total_sessions`
- `engagement_score`

**Slowly Changing**: No (Type 1)

### 8. Channel Dimension
**Purpose**: Marketing channel classification

**Key Attributes**:
- `channel_key` (Primary Key)
- `channel_name`
- `channel_type`
- `channel_category`
- `is_paid`
- `is_organic`

**Slowly Changing**: No (Type 1)

### 9. Product Dimension
**Purpose**: Product catalog and categorization

**Key Attributes**:
- `product_key` (Primary Key)
- `product_id`
- `product_name`
- `product_category`
- `product_subcategory`
- `brand`
- `price`
- `is_active`

**Slowly Changing**: No (Type 1)

## Fact Tables

### 1. Advertising Facts
**Purpose**: Advertising performance metrics

**Key Metrics**:
- `impressions`
- `clicks`
- `ctr` (Click-Through Rate)
- `spend`
- `cpc` (Cost Per Click)
- `cpm` (Cost Per Mille)
- `conversions`
- `conversion_rate`
- `revenue`
- `roas` (Return on Ad Spend)

**Foreign Keys**:
- `date_key`
- `site_key`
- `creative_key`
- `device_key`
- `geo_key`
- `campaign_key`
- `channel_key`

### 2. Web Analytics Facts
**Purpose**: Website performance metrics

**Key Metrics**:
- `sessions`
- `users`
- `pageviews`
- `bounce_rate`
- `session_duration`
- `pages_per_session`
- `goal_completions`
- `ecommerce_revenue`

**Foreign Keys**:
- `date_key`
- `device_key`
- `geo_key`
- `user_key`
- `channel_key`
- `product_key`

## Bridge Tables

### 1. Site-Creative Bridge
**Purpose**: Many-to-many relationship between sites and creatives

**Attributes**:
- `site_creative_key` (Primary Key)
- `site_key`
- `creative_key`
- `relationship_type`
- `effective_date`
- `expiration_date`

### 2. Campaign-Site Bridge
**Purpose**: Campaign hierarchy management

**Attributes**:
- `campaign_site_key` (Primary Key)
- `campaign_key`
- `site_key`
- `allocation_percentage`
- `priority`

### 3. User-Session Bridge
**Purpose**: User journey tracking

**Attributes**:
- `user_session_key` (Primary Key)
- `user_key`
- `session_id`
- `session_start_time`
- `session_end_time`
- `touchpoints`

## Slowly Changing Dimensions (SCD)

### SCD Type 2 Implementation
The system implements SCD Type 2 for critical dimensions that change over time:

**Benefits**:
- **Historical Preservation**: Maintains complete history of changes
- **Audit Trail**: Tracks when and how data changed
- **Point-in-Time Analysis**: Enables accurate historical analysis
- **Compliance**: Meets regulatory and governance requirements

**Implementation Details**:
- `effective_date`: When the record became active
- `expiration_date`: When the record became inactive (NULL for current)
- `current_flag`: Boolean flag for current records (Y/N)
- `surrogate_key`: Unique identifier for each version

### SCD Type 2 Process
1. **New Record**: Insert with `effective_date = current_date`, `expiration_date = NULL`, `current_flag = 'Y'`
2. **Update Record**: 
   - Set `expiration_date = current_date` and `current_flag = 'N'` for existing record
   - Insert new record with `effective_date = current_date`, `expiration_date = NULL`, `current_flag = 'Y'`

## Data Quality and Validation

### Validation Rules
- **Referential Integrity**: All foreign keys must reference valid dimension keys
- **Data Completeness**: Required fields cannot be NULL
- **Data Accuracy**: Metrics must be within reasonable ranges
- **Temporal Consistency**: Date relationships must be logical

### Quality Checks
- **CTR Validation**: Click-through rates between 0.001% and 50%
- **Spend Validation**: Positive values only
- **Date Validation**: Effective dates before expiration dates
- **SCD Validation**: Only one current record per business key

## Performance Optimization

### Indexing Strategy
- **Primary Keys**: Clustered indexes on all dimension primary keys
- **Foreign Keys**: Non-clustered indexes on fact table foreign keys
- **Composite Indexes**: For frequently queried combinations
- **Date Indexes**: Optimized for time-based queries

### Partitioning Strategy
- **Fact Tables**: Partitioned by date for improved query performance
- **Large Dimensions**: Partitioned by business key ranges
- **Archive Strategy**: Historical data moved to archive tables

## ETL Integration

### Data Flow
1. **Extract**: Raw data from the two PGD datasets
2. **Transform**: Apply business rules and SCD logic
3. **Load**: Insert/update dimension and fact tables
4. **Validate**: Run data quality checks
5. **Index**: Rebuild indexes for optimal performance

### SCD Processing
- **Type 1 Changes**: Direct updates to current records
- **Type 2 Changes**: Insert new records with version tracking
- **Type 3 Changes**: Add historical columns for limited history

## Business Intelligence Integration

### Power BI Connection
- **Direct Query**: Real-time connection to dimensional model
- **Import Mode**: Scheduled refresh for performance optimization
- **Incremental Refresh**: Only process new/changed data

### Query Optimization
- **Star Schema**: Optimized for analytical queries
- **Aggregations**: Pre-calculated summaries for common queries
- **Caching**: Intelligent caching for frequently accessed data

## Maintenance and Monitoring

### Regular Maintenance
- **Index Rebuild**: Weekly index maintenance
- **Statistics Update**: Regular statistics updates for query optimization
- **Data Archiving**: Monthly archiving of historical data
- **Performance Monitoring**: Continuous monitoring of query performance

### Monitoring Metrics
- **ETL Execution Time**: Track processing performance
- **Data Quality Scores**: Monitor data quality metrics
- **Query Performance**: Track query execution times
- **Storage Growth**: Monitor data volume growth

---

A dimensional model, as implemented in this project, is specifically designed to make marketing analytics and business reporting more effective and accessible. By separating data into fact tables (which store measurable business events, such as impressions, clicks, and conversions) and dimension tables (which describe the context of those events, such as time, site, creative, device, and campaign), the model allows users to analyze performance from multiple perspectives.

This structure enables:

- **Flexible Reporting**: Users can easily generate reports that break down metrics by any combination of dimensions, such as campaign by device, or site by creative.
- **Historical Tracking**: Slowly Changing Dimensions (SCD Type 2) are used for key tables, so changes in business entities (like site or creative details) are tracked over time. This allows for accurate point-in-time analysis and trend reporting.
- **Efficient Querying**: The star schema design reduces the complexity of queries, making it faster to retrieve and aggregate data for dashboards and ad hoc analysis.
- **Data Consistency**: Centralized dimension tables ensure that all reports and dashboards use consistent definitions for business entities, reducing confusion and errors.
- **Integration with BI Tools**: The model is structured to work seamlessly with business intelligence platforms such as Power BI, enabling users to create interactive dashboards, drill down into details, and visualize trends without complex data preparation.

In summary, the dimensional model provides a foundation that supports both routine business reporting and deeper analytical exploration, helping organizations understand marketing performance, identify opportunities, and make data-driven decisions.

