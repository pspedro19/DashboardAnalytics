# API Documentation - Dashboard Analytics ETL System

## Overview
This document describes the API and module structure of the Dashboard Analytics ETL system.

## Module Structure

### ETL Modules

#### Extract Module (`src/etl/extract/`)
- **extract_and_clean.py**: Main extraction and cleaning module
  - `extract_ga_data()`: Extract web analytics data from PGD Dataset 2
  - `extract_rfi_data()`: Extract advertising data from PGD Dataset 1
  - `clean_data()`: Clean and standardize data

#### Transform Module (`src/etl/transform/`)
- **create_dimensions.py**: Create dimension tables
  - `create_date_dimension()`: Date dimension table
  - `create_site_dimension()`: Site dimension table
  - `create_creative_dimension()`: Creative dimension table
  - `create_device_dimension()`: Device dimension table

- **create_facts.py**: Create fact tables
  - `create_advertising_facts()`: Advertising performance facts
  - `create_web_analytics_facts()`: Web analytics facts

#### Load Module (`src/etl/load/`)
- **calculate_kpis.py**: Calculate key performance indicators
  - `calculate_summary_kpis()`: Overall performance metrics
  - `calculate_site_performance()`: Site-specific metrics
  - `calculate_creative_performance()`: Creative-specific metrics

- **generate_analysis_report.py**: Generate analysis reports
  - `generate_executive_summary()`: Executive summary report
  - `generate_recommendations()`: Actionable recommendations

#### Utils Module (`src/etl/utils/`)
- **utils.py**: General utility functions
  - `setup_logging()`: Configure logging
  - `save_dataframe()`: Save data to files
  - `load_dataframe()`: Load data from files

- **validate_data.py**: Data validation functions
  - `validate_ctr()`: Validate click-through rates
  - `validate_data_quality()`: General data quality checks

### Configuration Module (`src/config/`)
- **settings.py**: Project configuration
  - Directory paths
  - File patterns
  - Processing settings
  - Validation thresholds

## Usage Examples

### Running the Full ETL Process
```python
from src.etl.run_full_etl import run_etl_pipeline

# Run complete ETL process
run_etl_pipeline()
```

### Extracting Data
```python
from src.etl.extract.extract_and_clean import extract_ga_data, extract_rfi_data

# Extract web analytics data from PGD Dataset 2
ga_data = extract_ga_data()

# Extract advertising data from PGD Dataset 1
rfi_data = extract_rfi_data()
```

### Creating Dimensions
```python
from src.etl.transform.create_dimensions import create_date_dimension

# Create date dimension
date_dim = create_date_dimension()
```

### Calculating KPIs
```python
from src.etl.load.calculate_kpis import calculate_summary_kpis

# Calculate summary KPIs
kpis = calculate_summary_kpis()
```

## Data Flow

1. **Extract**: Raw data from the two PGD datasets
2. **Clean**: Standardize formats and handle missing values
3. **Transform**: Create dimensional model (Kimball star schema)
4. **Load**: Generate fact and dimension tables
5. **Calculate KPIs**: Compute key performance indicators
6. **Generate Reports**: Create analysis reports and insights

## Error Handling

The system includes comprehensive error handling:
- Data validation at each step
- Logging of all operations
- Graceful handling of missing data
- Rollback capabilities for failed operations

## Performance Considerations

- Large files are processed in chunks
- Memory-efficient data processing
- Parallel processing where applicable
- Caching of intermediate results 