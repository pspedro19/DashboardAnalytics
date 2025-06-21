#!/usr/bin/env python
"""
Test ETL step by step
"""
import sys
import os
import pandas as pd

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Testing ETL step by step...")
    
    # Test 1: Check if data files exist
    print("\n1. Checking data files...")
    rfi_file = os.path.join('data', 'raw', 'rfi', 'RFI.csv')
    ga_file = os.path.join('data', 'raw', 'google_analytics', 'Raw GA Data.csv')
    
    if os.path.exists(rfi_file):
        print(f"✓ RFI file found: {rfi_file}")
        rfi_df = pd.read_csv(rfi_file, sep=';')
        print(f"  - Shape: {rfi_df.shape}")
        print(f"  - Columns: {list(rfi_df.columns)}")
    else:
        print(f"✗ RFI file not found: {rfi_file}")
    
    if os.path.exists(ga_file):
        print(f"✓ GA file found: {ga_file}")
        ga_df = pd.read_csv(ga_file, sep=';')
        print(f"  - Shape: {ga_df.shape}")
        print(f"  - Columns: {list(ga_df.columns)}")
    else:
        print(f"✗ GA file not found: {ga_file}")
    
    # Test 2: Test imports
    print("\n2. Testing imports...")
    from etl.utils.utils import setup_logging, clean_numeric, save_csv
    print("✓ Utils imported successfully")
    
    from etl.extract.extract_and_clean import extract_rfi_data, extract_ga_data
    print("✓ Extract functions imported successfully")
    
    # Test 3: Test extraction
    print("\n3. Testing extraction...")
    logger = setup_logging()
    
    # Create staging directory
    staging_dir = os.path.join('data', 'processed', 'staging')
    os.makedirs(staging_dir, exist_ok=True)
    print(f"✓ Created staging directory: {staging_dir}")
    
    # Test RFI extraction
    try:
        rfi_staging = extract_rfi_data()
        print(f"✓ RFI extraction successful: {len(rfi_staging)} rows")
    except Exception as e:
        print(f"✗ RFI extraction failed: {e}")
    
    # Test GA extraction
    try:
        ga_staging = extract_ga_data()
        print(f"✓ GA extraction successful: {len(ga_staging)} rows")
    except Exception as e:
        print(f"✗ GA extraction failed: {e}")
    
    print("\nETL test completed!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc() 