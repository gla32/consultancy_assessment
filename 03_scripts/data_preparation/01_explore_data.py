"""
Data Exploration Script for Consultancy Assessment
==================================================

This script examines the structure and content of all three Excel files to understand:
- Sheet names and which sheets contain data
- Column names and data types
- Available indicators (especially ANC4 and SBA related)
- Country names and year coverage
- Data quality issues

Author: Data Analyst
Date: 2025-01-27
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def explore_excel_file(file_path, file_name):
    """
    Explore a single Excel file and return detailed information about its structure and content.
    
    Parameters:
    file_path (str): Path to the Excel file
    file_name (str): Name of the file for reporting
    
    Returns:
    dict: Dictionary containing exploration results
    """
    print(f"\n{'='*80}")
    print(f"EXPLORING: {file_name}")
    print(f"{'='*80}")
    
    try:
        # Read Excel file to get sheet names
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        
        print(f"\nNumber of sheets: {len(sheet_names)}")
        print(f"Sheet names: {sheet_names}")
        
        exploration_results = {
            'file_name': file_name,
            'sheet_names': sheet_names,
            'sheets_data': {}
        }
        
        # Explore each sheet
        for sheet_name in sheet_names:
            print(f"\n{'-'*60}")
            print(f"SHEET: {sheet_name}")
            print(f"{'-'*60}")
            
            try:
                # Special handling for WPP2022 file which may have header issues
                if "WPP2022" in file_name:
                    # Try reading with different header options
                    df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
                    print(f"Raw shape: {df_raw.shape}")
                    
                    # Look for the actual header row
                    header_row = None
                    for i in range(min(10, len(df_raw))):
                        row_values = df_raw.iloc[i].dropna().astype(str).tolist()
                        if len(row_values) > 5 and any('country' in str(val).lower() or 'location' in str(val).lower() for val in row_values):
                            header_row = i
                            print(f"Found potential header row at index {i}: {row_values[:5]}")
                            break
                    
                    if header_row is not None:
                        df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
                        print(f"Using header row {header_row}")
                    else:
                        # Try different approaches
                        df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
                        print("Using default header (row 0)")
                        
                        # Show first few rows to understand structure
                        print(f"\nFirst 10 rows of raw data:")
                        for i in range(min(10, len(df_raw))):
                            row_data = df_raw.iloc[i].dropna().astype(str).tolist()[:10]
                            print(f"  Row {i}: {row_data}")
                else:
                    # Read the sheet normally
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Basic information
                print(f"Shape: {df.shape}")
                print(f"Columns ({len(df.columns)}): {list(df.columns)}")
                
                # Data types
                print(f"\nData types:")
                for col, dtype in df.dtypes.items():
                    print(f"  {col}: {dtype}")
                
                # Check for missing values
                missing_counts = df.isnull().sum()
                if missing_counts.sum() > 0:
                    print(f"\nMissing values:")
                    for col, count in missing_counts.items():
                        if count > 0:
                            print(f"  {col}: {count} ({count/len(df)*100:.1f}%)")
                
                # Look for specific indicators
                print(f"\nSearching for key indicators...")
                
                # Check column names for ANC4 and SBA indicators
                anc4_cols = [col for col in df.columns if 'anc' in str(col).lower() or 'antenatal' in str(col).lower()]
                sba_cols = [col for col in df.columns if 'sba' in str(col).lower() or 'skilled' in str(col).lower() or 'birth' in str(col).lower()]
                mortality_cols = [col for col in df.columns if 'mortality' in str(col).lower() or 'death' in str(col).lower()]
                
                if anc4_cols:
                    print(f"  ANC4/Antenatal related columns: {anc4_cols}")
                if sba_cols:
                    print(f"  SBA/Birth related columns: {sba_cols}")
                if mortality_cols:
                    print(f"  Mortality related columns: {mortality_cols}")
                
                # Check for country columns
                country_cols = [col for col in df.columns if 'country' in str(col).lower() or 'nation' in str(col).lower()]
                if country_cols:
                    print(f"  Country columns: {country_cols}")
                    for col in country_cols:
                        unique_countries = df[col].dropna().unique()
                        print(f"    {col}: {len(unique_countries)} unique values")
                        if len(unique_countries) <= 10:
                            print(f"      Values: {list(unique_countries)}")
                        else:
                            print(f"      Sample values: {list(unique_countries[:10])}")
                
                # Check for year columns
                year_cols = [col for col in df.columns if 'year' in str(col).lower() or 'time' in str(col).lower()]
                if year_cols:
                    print(f"  Year columns: {year_cols}")
                    for col in year_cols:
                        if df[col].dtype in ['int64', 'float64']:
                            year_range = f"{df[col].min():.0f} - {df[col].max():.0f}"
                            print(f"    {col}: {year_range}")
                        else:
                            unique_years = df[col].dropna().unique()
                            print(f"    {col}: {len(unique_years)} unique values")
                            if len(unique_years) <= 20:
                                print(f"      Values: {sorted(list(unique_years))}")
                
                # Check for 2022 data specifically
                has_2022_data = False
                for col in df.columns:
                    if df[col].dtype == 'object':
                        if df[col].astype(str).str.contains('2022', na=False).any():
                            has_2022_data = True
                            break
                    elif df[col].dtype in ['int64', 'float64']:
                        if (df[col] == 2022).any():
                            has_2022_data = True
                            break
                
                print(f"  Contains 2022 data: {has_2022_data}")
                
                # Look for indicator codes or names in the data
                print(f"\nSearching for specific indicator patterns...")
                
                # Check if any cell contains ANC4 or SBA related terms
                anc4_found = False
                sba_found = False
                
                for col in df.columns:
                    if df[col].dtype == 'object':
                        col_str = df[col].astype(str).str.lower()
                        if col_str.str.contains('anc|antenatal', na=False).any():
                            anc4_found = True
                            sample_values = df[col][col_str.str.contains('anc|antenatal', na=False)].head(3).tolist()
                            print(f"  ANC4 related data found in {col}: {sample_values}")
                        
                        if col_str.str.contains('sba|skilled.*birth|birth.*attend', na=False).any():
                            sba_found = True
                            sample_values = df[col][col_str.str.contains('sba|skilled.*birth|birth.*attend', na=False)].head(3).tolist()
                            print(f"  SBA related data found in {col}: {sample_values}")
                
                # Store sheet data
                exploration_results['sheets_data'][sheet_name] = {
                    'shape': df.shape,
                    'columns': list(df.columns),
                    'dtypes': dict(df.dtypes.astype(str)),
                    'missing_values': dict(missing_counts),
                    'anc4_columns': anc4_cols,
                    'sba_columns': sba_cols,
                    'mortality_columns': mortality_cols,
                    'country_columns': country_cols,
                    'year_columns': year_cols,
                    'has_2022_data': has_2022_data,
                    'anc4_found': anc4_found,
                    'sba_found': sba_found
                }
                
                # Show first few rows for context
                print(f"\nFirst 3 rows:")
                print(df.head(3).to_string())
                
            except Exception as e:
                print(f"Error reading sheet '{sheet_name}': {str(e)}")
                exploration_results['sheets_data'][sheet_name] = {'error': str(e)}
        
        return exploration_results
        
    except Exception as e:
        print(f"Error reading file '{file_name}': {str(e)}")
        return {'file_name': file_name, 'error': str(e)}

def compare_country_names(all_results):
    """
    Compare country names across all datasets to identify inconsistencies.
    
    Parameters:
    all_results (list): List of exploration results from all files
    """
    print(f"\n{'='*80}")
    print("COUNTRY NAME COMPARISON")
    print(f"{'='*80}")
    
    all_countries = {}
    
    # Collect all country names from all files
    for result in all_results:
        if 'error' in result:
            continue
            
        file_name = result['file_name']
        all_countries[file_name] = set()
        
        for sheet_name, sheet_data in result['sheets_data'].items():
            if 'error' in sheet_data:
                continue
                
            if 'country_columns' in sheet_data:
                for col in sheet_data['country_columns']:
                    # We would need to re-read the data to get actual country names
                    # For now, we'll note which files have country columns
                    all_countries[file_name].add(f"{sheet_name}.{col}")
    
    print("Files with country columns:")
    for file_name, country_refs in all_countries.items():
        if country_refs:
            print(f"  {file_name}: {list(country_refs)}")

def summarize_findings(all_results):
    """
    Summarize key findings from the exploration.
    
    Parameters:
    all_results (list): List of exploration results from all files
    """
    print(f"\n{'='*80}")
    print("SUMMARY OF KEY FINDINGS")
    print(f"{'='*80}")
    
    print("\n1. FILES OVERVIEW:")
    for result in all_results:
        if 'error' in result:
            print(f"   {result['file_name']}: ERROR - {result['error']}")
        else:
            print(f"   {result['file_name']}: {len(result['sheet_names'])} sheets")
    
    print("\n2. ANC4 INDICATORS:")
    anc4_files = []
    for result in all_results:
        if 'error' not in result:
            for sheet_name, sheet_data in result['sheets_data'].items():
                if 'error' not in sheet_data:
                    if sheet_data.get('anc4_columns') or sheet_data.get('anc4_found'):
                        anc4_files.append(f"{result['file_name']} ({sheet_name})")
    
    if anc4_files:
        print(f"   Found in: {anc4_files}")
    else:
        print("   No ANC4 indicators clearly identified")
    
    print("\n3. SBA INDICATORS:")
    sba_files = []
    for result in all_results:
        if 'error' not in result:
            for sheet_name, sheet_data in result['sheets_data'].items():
                if 'error' not in sheet_data:
                    if sheet_data.get('sba_columns') or sheet_data.get('sba_found'):
                        sba_files.append(f"{result['file_name']} ({sheet_name})")
    
    if sba_files:
        print(f"   Found in: {sba_files}")
    else:
        print("   No SBA indicators clearly identified")
    
    print("\n4. 2022 DATA AVAILABILITY:")
    files_with_2022 = []
    for result in all_results:
        if 'error' not in result:
            for sheet_name, sheet_data in result['sheets_data'].items():
                if 'error' not in sheet_data:
                    if sheet_data.get('has_2022_data'):
                        files_with_2022.append(f"{result['file_name']} ({sheet_name})")
    
    if files_with_2022:
        print(f"   Available in: {files_with_2022}")
    else:
        print("   No 2022 data clearly identified")
    
    print("\n5. RECOMMENDATIONS FOR DATA CLEANING:")
    print("   - Examine country name standardization across datasets")
    print("   - Look for indicator code mappings (especially for ANC4 and SBA)")
    print("   - Check data quality and completeness for 2022")
    print("   - Identify primary keys for merging datasets")
    print("   - Handle missing values appropriately")

def main():
    """
    Main function to explore all Excel files.
    """
    print("DATA EXPLORATION SCRIPT")
    print("=" * 80)
    
    # Define file paths
    data_dir = Path("01_raw_data")
    files_to_explore = [
        "GLOBAL_DATAFLOW_2018-2022.xlsx",
        "On-track and off-track countries.xlsx",
        "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"
    ]
    
    all_results = []
    
    # Explore each file
    for file_name in files_to_explore:
        file_path = data_dir / file_name
        
        if file_path.exists():
            result = explore_excel_file(file_path, file_name)
            all_results.append(result)
        else:
            print(f"\nWARNING: File not found: {file_path}")
            all_results.append({'file_name': file_name, 'error': 'File not found'})
    
    # Compare country names across datasets
    compare_country_names(all_results)
    
    # Summarize findings
    summarize_findings(all_results)
    
    print(f"\n{'='*80}")
    print("EXPLORATION COMPLETE")
    print(f"{'='*80}")
    print("\nNext steps:")
    print("1. Use these findings to create the data cleaning script")
    print("2. Focus on standardizing country names")
    print("3. Extract and clean ANC4 and SBA indicators")
    print("4. Prepare 2022 data for analysis")

if __name__ == "__main__":
    main()
