"""
Focused Data Exploration Script for Consultancy Assessment
=========================================================

This script provides a more targeted exploration of the three Excel files,
with special handling for the WPP2022 file structure.

"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from user_profile import UNICEF_DATA_FILE, MORTALITY_CLASS_FILE, POPULATION_DATA_FILE

def explore_unicef_data():
    """Explore the UNICEF GLOBAL_DATAFLOW file."""
    print("\n" + "="*80)
    print("EXPLORING: GLOBAL_DATAFLOW_2018-2022.xlsx")
    print("="*80)
    
    df = pd.read_excel(UNICEF_DATA_FILE, sheet_name='Unicef data')
    
    print(f"Shape: {df.shape}")
    print(f"Time period: {df['TIME_PERIOD'].min()} - {df['TIME_PERIOD'].max()}")
    
    # Check unique indicators
    indicators = df['Indicator'].unique()
    print(f"\nUnique indicators ({len(indicators)}):")
    for i, indicator in enumerate(indicators, 1):
        print(f"  {i}. {indicator}")
    
    # Check countries/regions
    areas = df['Geographic area'].unique()
    print(f"\nGeographic areas ({len(areas)}):")
    print(f"  Sample: {list(areas[:10])}")
    
    # Check 2022 data availability
    data_2022 = df[df['TIME_PERIOD'] == 2022]
    print(f"\n2022 data: {len(data_2022)} records")
    if len(data_2022) > 0:
        print(f"  Indicators in 2022: {data_2022['Indicator'].unique()}")
        print(f"  Countries in 2022: {len(data_2022['Geographic area'].unique())} areas")
    
    return df

def explore_mortality_status():
    """Explore the mortality status file."""
    print("\n" + "="*80)
    print("EXPLORING: On-track and off-track countries.xlsx")
    print("="*80)
    
    df = pd.read_excel(MORTALITY_CLASS_FILE, sheet_name='Sheet1')
    
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Check status distribution
    status_counts = df['Status.U5MR'].value_counts()
    print(f"\nUnder-5 mortality status distribution:")
    for status, count in status_counts.items():
        print(f"  {status}: {count} countries")
    
    # Sample countries
    print(f"\nSample countries:")
    print(df.head(10).to_string(index=False))
    
    return df

def explore_wpp2022_file():
    """Explore the WPP2022 demographic file with special handling."""
    print("\n" + "="*80)
    print("EXPLORING: WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx")
    print("="*80)
    
    # Check both sheets
    for sheet_name in ['Estimates', 'Projections']:
        print(f"\n{'-'*60}")
        print(f"SHEET: {sheet_name}")
        print(f"{'-'*60}")
        
        # Read raw data to find header
        df_raw = pd.read_excel(POPULATION_DATA_FILE, sheet_name=sheet_name, header=None)
        print(f"Raw shape: {df_raw.shape}")
        
        # Look for header row by finding row with many non-null values
        header_row = None
        for i in range(min(20, len(df_raw))):
            non_null_count = df_raw.iloc[i].notna().sum()
            if non_null_count > 10:  # Assuming header has many columns
                row_sample = df_raw.iloc[i].dropna().astype(str).tolist()[:10]
                print(f"  Row {i} ({non_null_count} non-null): {row_sample}")
                if header_row is None and non_null_count > 20:
                    header_row = i
        
        if header_row is not None:
            print(f"\nUsing row {header_row} as header")
            df = pd.read_excel(POPULATION_DATA_FILE, sheet_name=sheet_name, header=header_row)
            
            print(f"Processed shape: {df.shape}")
            print(f"Columns: {list(df.columns)[:10]}...")  # Show first 10 columns
            
            # Look for country/location column
            country_cols = [col for col in df.columns if any(term in str(col).lower() 
                           for term in ['country', 'location', 'region', 'area'])]
            if country_cols:
                print(f"Country-related columns: {country_cols}")
                
                # Check unique countries
                for col in country_cols[:1]:  # Check first country column
                    unique_vals = df[col].dropna().unique()
                    print(f"  {col}: {len(unique_vals)} unique values")
                    if len(unique_vals) <= 20:
                        print(f"    Values: {list(unique_vals)}")
                    else:
                        print(f"    Sample: {list(unique_vals[:10])}")
            
            # Look for year columns
            year_cols = [col for col in df.columns if any(term in str(col).lower() 
                        for term in ['year', 'time', '2022'])]
            if year_cols:
                print(f"Year-related columns: {year_cols[:5]}")
            
            # Check for 2022 data
            has_2022 = False
            for col in df.columns:
                if '2022' in str(col):
                    has_2022 = True
                    print(f"Found 2022 column: {col}")
                    break
            
            if not has_2022:
                # Check if 2022 appears in data
                for col in df.columns:
                    if df[col].dtype == 'object':
                        if df[col].astype(str).str.contains('2022', na=False).any():
                            has_2022 = True
                            break
            
            print(f"Contains 2022 data: {has_2022}")
        else:
            print("Could not identify proper header row")
    
    return None

def main():
    """Main exploration function."""
    print("FOCUSED DATA EXPLORATION SCRIPT")
    print("=" * 80)
    
    # Explore each file
    try:
        unicef_df = explore_unicef_data()
    except Exception as e:
        print(f"Error exploring UNICEF data: {e}")
        unicef_df = None
    
    try:
        mortality_df = explore_mortality_status()
    except Exception as e:
        print(f"Error exploring mortality data: {e}")
        mortality_df = None
    
    try:
        wpp_df = explore_wpp2022_file()
    except Exception as e:
        print(f"Error exploring WPP2022 data: {e}")
        wpp_df = None
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY OF KEY FINDINGS")
    print("="*80)
    
    print("\n1. ANC4 AND SBA INDICATORS:")
    if unicef_df is not None:
        anc4_data = unicef_df[unicef_df['Indicator'].str.contains('Antenatal care 4+', na=False)]
        sba_data = unicef_df[unicef_df['Indicator'].str.contains('Skilled birth attendant', na=False)]
        
        print(f"   - ANC4 records: {len(anc4_data)}")
        print(f"   - SBA records: {len(sba_data)}")
        
        if len(anc4_data) > 0:
            anc4_2022 = anc4_data[anc4_data['TIME_PERIOD'] == 2022]
            print(f"   - ANC4 countries with 2022 data: {len(anc4_2022['Geographic area'].unique())}")
        
        if len(sba_data) > 0:
            sba_2022 = sba_data[sba_data['TIME_PERIOD'] == 2022]
            print(f"   - SBA countries with 2022 data: {len(sba_2022['Geographic area'].unique())}")
    
    print("\n2. COUNTRY STANDARDIZATION NEEDS:")
    if unicef_df is not None and mortality_df is not None:
        unicef_countries = set(unicef_df['Geographic area'].unique())
        mortality_countries = set(mortality_df['OfficialName'].unique())
        
        print(f"   - UNICEF file: {len(unicef_countries)} geographic areas")
        print(f"   - Mortality file: {len(mortality_countries)} countries")
        
        # Check for potential matches
        common_names = unicef_countries.intersection(mortality_countries)
        print(f"   - Exact name matches: {len(common_names)}")
    
    print("\n3. DATA CLEANING PRIORITIES:")
    print("   - Parse WPP2022 file structure properly")
    print("   - Standardize country names across datasets")
    print("   - Extract 2022 ANC4 and SBA data")
    print("   - Map mortality status to countries")
    print("   - Handle regional aggregates vs individual countries")

if __name__ == "__main__":
    main()
