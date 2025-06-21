#!/usr/bin/env python
"""
Test script to verify imports work correctly
"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from etl.utils.utils import setup_logging
    print("✓ utils import successful")
    
    from etl.extract.extract_and_clean import extract_rfi_data
    print("✓ extract_and_clean import successful")
    
    from etl.utils.validate_data import validate_staging_data
    print("✓ validate_data import successful")
    
    from etl.transform.create_dimensions import create_all_dimensions
    print("✓ create_dimensions import successful")
    
    from etl.transform.create_facts import create_fact_ad_performance
    print("✓ create_facts import successful")
    
    from etl.load.calculate_kpis import calculate_summary_kpis
    print("✓ calculate_kpis import successful")
    
    from etl.load.generate_analysis_report import generate_analysis_report
    print("✓ generate_analysis_report import successful")
    
    print("\nAll imports successful!")
    
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1) 