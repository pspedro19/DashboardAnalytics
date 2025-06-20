"""
Configuration settings for Dashboard Analytics ETL System
"""
import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DIMENSIONAL_DATA_DIR = DATA_DIR / "dimensional"
OUTPUTS_DIR = DATA_DIR / "outputs"

# Source directories
SRC_DIR = PROJECT_ROOT / "src"
ETL_DIR = SRC_DIR / "etl"
LOGS_DIR = PROJECT_ROOT / "logs"

# Raw data sources
GOOGLE_ANALYTICS_DIR = RAW_DATA_DIR / "google_analytics"
RFI_DIR = RAW_DATA_DIR / "rfi"

# Dimensional model directories
DIMENSIONS_DIR = DIMENSIONAL_DATA_DIR / "dimensions"
FACTS_DIR = DIMENSIONAL_DATA_DIR / "facts"
BRIDGE_DIR = DIMENSIONAL_DATA_DIR / "bridge"

# File patterns
GA_DATA_PATTERN = "Raw GA Data*.xlsx"
RFI_DATA_PATTERN = "RFI*.csv"

# Output file names
KPI_SUMMARY_FILE = "kpi_summary.csv"
SITE_PERFORMANCE_FILE = "site_performance.csv"
CREATIVE_PERFORMANCE_FILE = "creative_performance.csv"
ANALYSIS_REPORT_FILE = "analysis_report.txt"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "etl_execution.log"

# Data processing settings
CHUNK_SIZE = 10000  # For processing large files in chunks
RANDOM_STATE = 42   # For reproducible results

# Validation settings
MIN_CTR_THRESHOLD = 0.001  # Minimum CTR threshold for validation
MAX_CTR_THRESHOLD = 0.5    # Maximum CTR threshold for validation

# Ensure directories exist
def ensure_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        DIMENSIONAL_DATA_DIR,
        OUTPUTS_DIR,
        LOGS_DIR,
        GOOGLE_ANALYTICS_DIR,
        RFI_DIR,
        DIMENSIONS_DIR,
        FACTS_DIR,
        BRIDGE_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    ensure_directories() 