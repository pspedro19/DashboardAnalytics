#!/usr/bin/env python
"""
Script to fix file paths in all ETL files
"""
import os
import re

def fix_file_paths(file_path):
    """Fix file paths in a given file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace old paths with new paths
    replacements = [
        (r'\.\./02_staging/', '../../data/processed/staging/'),
        (r'\.\./03_dimensional_model/', '../../data/dimensional/'),
        (r'\.\./05_kpi_outputs/', '../../data/outputs/'),
        (r'\.\./06_logs/', '../../logs/'),
        (r'\.\./01_raw_data/rfi_raw/', '../../data/raw/rfi/'),
        (r'\.\./01_raw_data/ga_raw/', '../../data/raw/google_analytics/'),
    ]
    
    for old_path, new_path in replacements:
        content = content.replace(old_path, new_path)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed paths in {file_path}")

# List of files to fix
files_to_fix = [
    'src/etl/transform/create_dimensions.py',
    'src/etl/transform/create_facts.py',
    'src/etl/load/calculate_kpis.py',
    'src/etl/load/generate_analysis_report.py',
]

for file_path in files_to_fix:
    if os.path.exists(file_path):
        fix_file_paths(file_path)
    else:
        print(f"File not found: {file_path}")

print("Path fixing completed!") 