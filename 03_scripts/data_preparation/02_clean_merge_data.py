"""
Data Cleaning and Merging Script for Consultancy Assessment
==========================================================

This script cleans and merges the three datasets into a single analysis-ready file:
1. UNICEF health indicators (ANC4 and SBA)
2. UN Population data (2022 birth projections)
3. Under-5 mortality reduction status

Author: Data Analyst
Date: 2025-01-27
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import re
warnings.filterwarnings('ignore')

# File paths
# Add project root to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from user_profile import RAW_DATA_DIR, PROCESSED_DATA_DIR, UNICEF_DATA_FILE, MORTALITY_CLASS_FILE, POPULATION_DATA_FILE, MERGED_DATA_FILE

UNICEF_FILE = RAW_DATA_DIR / "GLOBAL_DATAFLOW_2018-2022.xlsx"
POPULATION_FILE = RAW_DATA_DIR / "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"
MORTALITY_FILE = RAW_DATA_DIR / "On-track and off-track countries.xlsx"

def clean_unicef_data():
    """
    Clean UNICEF data:
    - Filter for years 2018-2022
    - Extract ANC4 and SBA indicators
    - Keep most recent estimate for each country-indicator
    - Convert to wide format
    """
    print("Cleaning UNICEF data...")
    
    # Read UNICEF data
    df = pd.read_excel(UNICEF_FILE, sheet_name='Unicef data')
    
    # Filter for target years (2018-2022)
    df = df[df['TIME_PERIOD'].between(2018, 2022)]
    
    # Identify ANC4 and SBA indicators based on exploration findings
    anc4_mask = df['Indicator'].str.contains('Antenatal care 4+', na=False)
    sba_mask = df['Indicator'].str.contains('Skilled birth attendant', na=False)
    
    # Filter for these indicators only
    df = df[anc4_mask | sba_mask]
    
    # Create simplified indicator names
    df['Indicator_Clean'] = df['Indicator'].apply(lambda x: 
        'ANC4' if 'Antenatal care 4+' in str(x) else 'SBA')
    
    # For each country-indicator combination, keep the most recent estimate
    df_recent = df.sort_values('TIME_PERIOD').groupby(['Geographic area', 'Indicator_Clean']).tail(1)
    
    # Convert to wide format with ANC4 and SBA as separate columns
    df_wide = df_recent.pivot_table(
        index='Geographic area',
        columns='Indicator_Clean',
        values='OBS_VALUE',
        aggfunc='first'
    ).reset_index()
    
    # Rename columns
    df_wide.columns.name = None
    df_wide = df_wide.rename(columns={'Geographic area': 'Country'})
    
    print(f"UNICEF data cleaned: {len(df_wide)} countries with health indicators")
    print(f"Countries with ANC4 data: {df_wide['ANC4'].notna().sum()}")
    print(f"Countries with SBA data: {df_wide['SBA'].notna().sum()}")
    
    return df_wide

def clean_population_data():
    """
    Clean population data:
    - Extract 2022 birth projections
    - Convert to numeric format
    - Handle missing values
    """
    print("\nCleaning population data...")
    
    # Read population data with proper header handling
    # Based on exploration, header is at row 16
    df_estimates = pd.read_excel(POPULATION_FILE, sheet_name='Estimates', header=16)
    df_projections = pd.read_excel(POPULATION_FILE, sheet_name='Projections', header=16)
    
    # Use projections sheet for 2022 data as it's more recent
    df = df_projections.copy()
    
    # Find the country column (based on exploration findings)
    country_col = None
    for col in df.columns:
        if any(term in str(col).lower() for term in ['country', 'region', 'area']):
            country_col = col
            break
    
    if country_col is None:
        # Fallback to first column if no clear country column found
        country_col = df.columns[0]
    
    # Filter for 2022 data
    df_2022 = df[df['Year'] == 2022].copy()
    
    # Extract births data (look for births column)
    births_col = None
    for col in df.columns:
        if 'births' in str(col).lower():
            births_col = col
            break
    
    if births_col is None:
        # Look for columns that might contain birth data
        for col in df.columns:
            if any(term in str(col).lower() for term in ['birth', 'natality']):
                births_col = col
                break
    
    if births_col is not None:
        # Select relevant columns
        pop_data = df_2022[[country_col, births_col]].copy()
        pop_data.columns = ['Country', 'Births_2022']
        
        # Convert to numeric format
        pop_data['Births_2022'] = pd.to_numeric(pop_data['Births_2022'], errors='coerce')
        
        # Handle missing values - remove rows with missing birth data
        pop_data = pop_data.dropna(subset=['Births_2022'])
        
        print(f"Population data cleaned: {len(pop_data)} countries with 2022 birth data")
    else:
        print("Warning: Could not find births column in population data")
        # Create dummy data structure
        pop_data = pd.DataFrame(columns=['Country', 'Births_2022'])
    
    return pop_data

def clean_mortality_classification():
    """
    Clean mortality classification:
    - Create binary classification: 'on-track' vs 'off-track'
    """
    print("\nCleaning mortality classification...")
    
    # Read mortality data
    df = pd.read_excel(MORTALITY_FILE, sheet_name='Sheet1')
    
    # Create binary classification
    def classify_status(status):
        if pd.isna(status):
            return np.nan
        status_lower = str(status).lower()
        if status_lower in ['achieved', 'on-track']:
            return 'on-track'
        elif 'acceleration needed' in status_lower:
            return 'off-track'
        else:
            return 'off-track'  # Default to off-track for unknown statuses
    
    df['Mortality_Status_Binary'] = df['Status.U5MR'].apply(classify_status)
    
    # Select relevant columns
    mortality_data = df[['OfficialName', 'ISO3Code', 'Mortality_Status_Binary']].copy()
    mortality_data = mortality_data.rename(columns={'OfficialName': 'Country'})
    
    print(f"Mortality classification cleaned: {len(mortality_data)} countries")
    print(f"On-track countries: {(mortality_data['Mortality_Status_Binary'] == 'on-track').sum()}")
    print(f"Off-track countries: {(mortality_data['Mortality_Status_Binary'] == 'off-track').sum()}")
    
    return mortality_data

def create_country_mapping():
    """
    Create mapping for common country name variations to standardize names across datasets.
    """
    print("\nCreating country name mapping...")
    
    # Common country name variations mapping
    country_mapping = {
        # Common variations
        'United States of America': 'United States',
        'USA': 'United States',
        'US': 'United States',
        'United Kingdom': 'United Kingdom of Great Britain and Northern Ireland',
        'UK': 'United Kingdom of Great Britain and Northern Ireland',
        'Russia': 'Russian Federation',
        'South Korea': 'Republic of Korea',
        'North Korea': "Democratic People's Republic of Korea",
        'Iran': 'Iran (Islamic Republic of)',
        'Venezuela': 'Venezuela (Bolivarian Republic of)',
        'Bolivia': 'Bolivia (Plurinational State of)',
        'Tanzania': 'United Republic of Tanzania',
        'Congo': 'Congo',
        'Democratic Republic of the Congo': 'Democratic Republic of the Congo',
        'Ivory Coast': "Côte d'Ivoire",
        'Cape Verde': 'Cabo Verde',
        'Swaziland': 'Eswatini',
        'Macedonia': 'North Macedonia',
        'Myanmar': 'Myanmar',
        'Burma': 'Myanmar',
        'East Timor': 'Timor-Leste',
        'Moldova': 'Republic of Moldova',
        'Syria': 'Syrian Arab Republic',
        'Laos': "Lao People's Democratic Republic",
        'Vietnam': 'Viet Nam',
        'Brunei': 'Brunei Darussalam',
        'Micronesia': 'Micronesia (Federated States of)',
        'Palestine': 'State of Palestine',
        'Turkey': 'Türkiye',
    }
    
    return country_mapping

def standardize_country_names(df, country_col='Country', mapping=None):
    """
    Apply country name standardization to a dataframe.
    """
    if mapping is None:
        mapping = create_country_mapping()
    
    df = df.copy()
    df[country_col] = df[country_col].replace(mapping)
    
    # Additional cleaning: strip whitespace and handle encoding issues
    df[country_col] = df[country_col].astype(str).str.strip()
    
    return df

def filter_individual_countries(df, country_col='Country'):
    """
    Filter out regional aggregates and keep only individual countries.
    """
    # Patterns that indicate regional aggregates
    regional_patterns = [
        r'\(.*SDGRC.*\)',  # SDG regional classifications
        r'Africa$',
        r'Asia$',
        r'Europe$',
        r'America',
        r'World',
        r'Developed',
        r'Developing',
        r'Least developed',
        r'Land.locked',
        r'Small island',
        r'Sub-Saharan',
        r'Northern Africa',
        r'Eastern Africa',
        r'Western Africa',
        r'Middle Africa',
        r'Southern Africa',
        r'Eastern Asia',
        r'South-eastern Asia',
        r'Southern Asia',
        r'Western Asia',
        r'Central Asia',
        r'Eastern Europe',
        r'Northern Europe',
        r'Southern Europe',
        r'Western Europe',
        r'Caribbean',
        r'Central America',
        r'South America',
        r'Northern America',
        r'Oceania',
        r'Polynesia',
        r'Melanesia',
        r'Micronesia',
        r'More developed',
        r'Less developed',
        r'High income',
        r'Upper middle income',
        r'Lower middle income',
        r'Low income',
    ]
    
    # Create combined pattern
    combined_pattern = '|'.join(regional_patterns)
    
    # Filter out regional aggregates
    mask = ~df[country_col].str.contains(combined_pattern, case=False, na=False)
    df_filtered = df[mask].copy()
    
    print(f"Filtered from {len(df)} to {len(df_filtered)} individual countries")
    
    return df_filtered

def merge_datasets(unicef_data, population_data, mortality_data):
    """
    Merge datasets using inner joins to keep only countries with complete data.
    """
    print("\nMerging datasets...")
    
    # Apply country name standardization to all datasets
    country_mapping = create_country_mapping()
    
    unicef_clean = standardize_country_names(unicef_data, mapping=country_mapping)
    population_clean = standardize_country_names(population_data, mapping=country_mapping)
    mortality_clean = standardize_country_names(mortality_data, mapping=country_mapping)
    
    # Filter to individual countries only
    unicef_clean = filter_individual_countries(unicef_clean)
    population_clean = filter_individual_countries(population_clean)
    mortality_clean = filter_individual_countries(mortality_clean)
    
    print(f"After filtering:")
    print(f"  UNICEF: {len(unicef_clean)} countries")
    print(f"  Population: {len(population_clean)} countries")
    print(f"  Mortality: {len(mortality_clean)} countries")
    
    # Start with mortality data as it has the most standardized country names
    merged = mortality_clean.copy()
    
    # Merge with UNICEF data
    merged = merged.merge(unicef_clean, on='Country', how='inner')
    print(f"After merging with UNICEF data: {len(merged)} countries")
    
    # Merge with population data
    if len(population_clean) > 0:
        merged = merged.merge(population_clean, on='Country', how='inner')
        print(f"After merging with population data: {len(merged)} countries")
    else:
        print("Warning: No population data to merge")
    
    return merged

def validate_merge_results(merged_data):
    """
    Validate the merge results and provide summary statistics.
    """
    print("\nValidating merge results...")
    print(f"Final dataset shape: {merged_data.shape}")
    print(f"Columns: {list(merged_data.columns)}")
    
    # Check for missing values
    print("\nMissing values:")
    missing_counts = merged_data.isnull().sum()
    for col, count in missing_counts.items():
        if count > 0:
            print(f"  {col}: {count} ({count/len(merged_data)*100:.1f}%)")
    
    # Summary statistics for numeric columns
    numeric_cols = merged_data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print("\nSummary statistics for numeric columns:")
        print(merged_data[numeric_cols].describe())
    
    # Check mortality status distribution
    if 'Mortality_Status_Binary' in merged_data.columns:
        print("\nMortality status distribution:")
        status_counts = merged_data['Mortality_Status_Binary'].value_counts()
        for status, count in status_counts.items():
            print(f"  {status}: {count} countries ({count/len(merged_data)*100:.1f}%)")
    
    # Check health indicator availability
    if 'ANC4' in merged_data.columns:
        anc4_available = merged_data['ANC4'].notna().sum()
        print(f"\nCountries with ANC4 data: {anc4_available} ({anc4_available/len(merged_data)*100:.1f}%)")
    
    if 'SBA' in merged_data.columns:
        sba_available = merged_data['SBA'].notna().sum()
        print(f"Countries with SBA data: {sba_available} ({sba_available/len(merged_data)*100:.1f}%)")
    
    return merged_data

def save_final_dataset(merged_data, filename="merged_health_data.csv"):
    """
    Save the final merged dataset as CSV.
    """
    output_path = PROCESSED_DATA_DIR / filename
    merged_data.to_csv(output_path, index=False)
    print(f"\nFinal dataset saved to: {output_path}")
    print(f"Dataset contains {len(merged_data)} countries with complete data")
    
    return output_path

def main():
    """
    Main function to execute the complete data cleaning and merging pipeline.
    """
    print("DATA CLEANING AND MERGING SCRIPT")
    print("=" * 80)
    
    try:
        # Step 1: Clean UNICEF data
        unicef_data = clean_unicef_data()
        
        # Step 2: Clean population data
        population_data = clean_population_data()
        
        # Step 3: Clean mortality classification
        mortality_data = clean_mortality_classification()
        
        # Step 4: Merge datasets
        merged_data = merge_datasets(unicef_data, population_data, mortality_data)
        
        # Step 5: Validate results
        validated_data = validate_merge_results(merged_data)
        
        # Step 6: Save final dataset
        output_path = save_final_dataset(validated_data)
        
        print("\n" + "=" * 80)
        print("DATA CLEANING AND MERGING COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print(f"Final dataset: {output_path}")
        print(f"Countries included: {len(validated_data)}")
        print(f"Variables: {list(validated_data.columns)}")
        
        return validated_data
        
    except Exception as e:
        print(f"\nError in data cleaning and merging: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = main()
