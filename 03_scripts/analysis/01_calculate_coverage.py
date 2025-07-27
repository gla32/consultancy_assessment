"""
Coverage Analysis Script
========================

Purpose: Calculate population-weighted coverage for ANC4 and SBA by track status.

This script analyzes maternal health coverage indicators (ANC4 and SBA) by comparing
on-track vs off-track countries, using population-weighted averages based on births data.

Author: Data Analysis Team
Date: 2025
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

def load_data():
    """Load the merged health dataset."""
    data_path = Path("02_processed_data/merged_health_data.csv")
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"Loaded dataset with {len(df)} countries")
    return df

def calculate_population_weighted_coverage(df, indicator, track_status):
    """
    Calculate population-weighted coverage for a specific indicator and track status.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing coverage and births data
    indicator : str
        The coverage indicator ('ANC4' or 'SBA')
    track_status : str
        The track status ('on-track' or 'off-track')
    
    Returns:
    --------
    dict : Dictionary containing calculated statistics
    """
    # Filter data for the specific track status and remove missing values
    subset = df[
        (df['Mortality_Status_Binary'] == track_status) & 
        (df[indicator].notna()) & 
        (df['Births_2022'].notna())
    ].copy()
    
    if len(subset) == 0:
        return {
            'track_status': track_status,
            'indicator': indicator,
            'n_countries': 0,
            'total_births': 0,
            'weighted_coverage': np.nan,
            'min_coverage': np.nan,
            'max_coverage': np.nan,
            'median_coverage': np.nan,
            'countries': []
        }
    
    # Calculate population-weighted average
    # Formula: Σ(coverage_i × births_i) / Σ(births_i)
    weights = subset['Births_2022']
    coverage_values = subset[indicator]
    
    # Handle negative births (population decline) by taking absolute values for weighting
    abs_weights = weights.abs()
    
    weighted_coverage = np.average(coverage_values, weights=abs_weights)
    
    # Calculate other statistics
    total_births = weights.sum()
    n_countries = len(subset)
    min_coverage = coverage_values.min()
    max_coverage = coverage_values.max()
    median_coverage = coverage_values.median()
    
    # Get list of countries for reference
    countries = subset['Country'].tolist()
    
    return {
        'track_status': track_status,
        'indicator': indicator,
        'n_countries': n_countries,
        'total_births': total_births,
        'weighted_coverage': weighted_coverage,
        'min_coverage': min_coverage,
        'max_coverage': max_coverage,
        'median_coverage': median_coverage,
        'countries': countries
    }

def analyze_coverage_by_indicator(df, indicator):
    """
    Analyze coverage for a specific indicator across track statuses.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset
    indicator : str
        The coverage indicator ('ANC4' or 'SBA')
    
    Returns:
    --------
    dict : Dictionary containing analysis results for both track statuses
    """
    print(f"\n{'='*60}")
    print(f"ANALYZING {indicator} COVERAGE")
    print(f"{'='*60}")
    
    results = {}
    
    # Analyze both track statuses
    for status in ['on-track', 'off-track']:
        results[status] = calculate_population_weighted_coverage(df, indicator, status)
        
        result = results[status]
        print(f"\n{status.upper()} COUNTRIES:")
        print(f"  Number of countries: {result['n_countries']}")
        print(f"  Total births represented: {result['total_births']:,.0f}")
        print(f"  Population-weighted coverage: {result['weighted_coverage']:.1f}%")
        print(f"  Coverage range: {result['min_coverage']:.1f}% - {result['max_coverage']:.1f}%")
        print(f"  Median coverage: {result['median_coverage']:.1f}%")
    
    # Calculate coverage gap
    if (results['on-track']['weighted_coverage'] is not np.nan and 
        results['off-track']['weighted_coverage'] is not np.nan):
        
        coverage_gap = results['on-track']['weighted_coverage'] - results['off-track']['weighted_coverage']
        print(f"\nCOVERAGE GAP ANALYSIS:")
        print(f"  On-track vs Off-track gap: {coverage_gap:.1f} percentage points")
        print(f"  Relative difference: {(coverage_gap/results['off-track']['weighted_coverage']*100):.1f}%")
        
        results['coverage_gap'] = coverage_gap
        results['relative_difference'] = coverage_gap/results['off-track']['weighted_coverage']*100
    
    return results

def create_summary_table(anc4_results, sba_results):
    """
    Create a summary comparison table.
    
    Parameters:
    -----------
    anc4_results : dict
        Results from ANC4 analysis
    sba_results : dict
        Results from SBA analysis
    
    Returns:
    --------
    pandas.DataFrame : Summary table
    """
    summary_data = []
    
    for indicator, results in [('ANC4', anc4_results), ('SBA', sba_results)]:
        for status in ['on-track', 'off-track']:
            if status in results:
                result = results[status]
                summary_data.append({
                    'Indicator': indicator,
                    'Track_Status': status,
                    'N_Countries': result['n_countries'],
                    'Total_Births': result['total_births'],
                    'Weighted_Coverage_Percent': result['weighted_coverage'],
                    'Min_Coverage_Percent': result['min_coverage'],
                    'Max_Coverage_Percent': result['max_coverage'],
                    'Median_Coverage_Percent': result['median_coverage']
                })
    
    # Add gap analysis
    for indicator, results in [('ANC4', anc4_results), ('SBA', sba_results)]:
        if 'coverage_gap' in results:
            summary_data.append({
                'Indicator': indicator,
                'Track_Status': 'gap_analysis',
                'N_Countries': np.nan,
                'Total_Births': np.nan,
                'Weighted_Coverage_Percent': results['coverage_gap'],
                'Min_Coverage_Percent': np.nan,
                'Max_Coverage_Percent': np.nan,
                'Median_Coverage_Percent': np.nan
            })
    
    return pd.DataFrame(summary_data)

def save_detailed_results(df, anc4_results, sba_results):
    """
    Save detailed results including country-level data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Original dataset
    anc4_results : dict
        ANC4 analysis results
    sba_results : dict
        SBA analysis results
    """
    # Create output directory if it doesn't exist
    output_dir = Path("05_output/reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save summary table
    summary_table = create_summary_table(anc4_results, sba_results)
    summary_path = output_dir / "coverage_analysis_summary.csv"
    summary_table.to_csv(summary_path, index=False)
    print(f"\nSummary results saved to: {summary_path}")
    
    # Save detailed country-level data with analysis flags
    detailed_df = df.copy()
    
    # Add analysis flags
    detailed_df['ANC4_Data_Available'] = detailed_df['ANC4'].notna()
    detailed_df['SBA_Data_Available'] = detailed_df['SBA'].notna()
    detailed_df['Births_Data_Available'] = detailed_df['Births_2022'].notna()
    
    # Add coverage categories
    def categorize_coverage(value):
        if pd.isna(value):
            return 'No Data'
        elif value < 50:
            return 'Low (<50%)'
        elif value < 80:
            return 'Medium (50-79%)'
        else:
            return 'High (≥80%)'
    
    detailed_df['ANC4_Category'] = detailed_df['ANC4'].apply(categorize_coverage)
    detailed_df['SBA_Category'] = detailed_df['SBA'].apply(categorize_coverage)
    
    detailed_path = output_dir / "coverage_analysis_detailed.csv"
    detailed_df.to_csv(detailed_path, index=False)
    print(f"Detailed results saved to: {detailed_path}")

def print_interpretation(anc4_results, sba_results):
    """
    Print detailed interpretation of results.
    
    Parameters:
    -----------
    anc4_results : dict
        ANC4 analysis results
    sba_results : dict
        SBA analysis results
    """
    print(f"\n{'='*80}")
    print("COVERAGE ANALYSIS INTERPRETATION")
    print(f"{'='*80}")
    
    print("\nKEY FINDINGS:")
    print("-" * 40)
    
    # ANC4 Interpretation
    if 'coverage_gap' in anc4_results:
        anc4_gap = anc4_results['coverage_gap']
        anc4_on_track = anc4_results['on-track']['weighted_coverage']
        anc4_off_track = anc4_results['off-track']['weighted_coverage']
        
        print(f"1. ANTENATAL CARE (ANC4+):")
        print(f"   • On-track countries achieve {anc4_on_track:.1f}% coverage")
        print(f"   • Off-track countries achieve {anc4_off_track:.1f}% coverage")
        print(f"   • Coverage gap: {anc4_gap:.1f} percentage points")
        
        if anc4_gap > 20:
            print(f"   • INTERPRETATION: Large coverage gap indicates significant disparities")
        elif anc4_gap > 10:
            print(f"   • INTERPRETATION: Moderate coverage gap suggests room for improvement")
        else:
            print(f"   • INTERPRETATION: Relatively small coverage gap")
    
    # SBA Interpretation
    if 'coverage_gap' in sba_results:
        sba_gap = sba_results['coverage_gap']
        sba_on_track = sba_results['on-track']['weighted_coverage']
        sba_off_track = sba_results['off-track']['weighted_coverage']
        
        print(f"\n2. SKILLED BIRTH ATTENDANCE (SBA):")
        print(f"   • On-track countries achieve {sba_on_track:.1f}% coverage")
        print(f"   • Off-track countries achieve {sba_off_track:.1f}% coverage")
        print(f"   • Coverage gap: {sba_gap:.1f} percentage points")
        
        if sba_gap > 20:
            print(f"   • INTERPRETATION: Large coverage gap indicates significant disparities")
        elif sba_gap > 10:
            print(f"   • INTERPRETATION: Moderate coverage gap suggests room for improvement")
        else:
            print(f"   • INTERPRETATION: Relatively small coverage gap")
    
    # Comparative analysis
    if 'coverage_gap' in anc4_results and 'coverage_gap' in sba_results:
        print(f"\n3. COMPARATIVE ANALYSIS:")
        if anc4_results['coverage_gap'] > sba_results['coverage_gap']:
            print(f"   • ANC4 shows larger coverage gaps than SBA")
            print(f"   • This suggests prenatal care access is more challenging than delivery care")
        elif sba_results['coverage_gap'] > anc4_results['coverage_gap']:
            print(f"   • SBA shows larger coverage gaps than ANC4")
            print(f"   • This suggests delivery care access is more challenging than prenatal care")
        else:
            print(f"   • ANC4 and SBA show similar coverage gaps")
    
    # Population impact
    print(f"\n4. POPULATION IMPACT:")
    total_births_on_track = 0
    total_births_off_track = 0
    
    for results in [anc4_results, sba_results]:
        if 'on-track' in results and results['on-track']['total_births'] > 0:
            total_births_on_track = max(total_births_on_track, results['on-track']['total_births'])
        if 'off-track' in results and results['off-track']['total_births'] > 0:
            total_births_off_track = max(total_births_off_track, results['off-track']['total_births'])
    
    print(f"   • On-track countries represent ~{total_births_on_track:,.0f} births annually")
    print(f"   • Off-track countries represent ~{total_births_off_track:,.0f} births annually")
    
    if total_births_off_track > total_births_on_track:
        print(f"   • CRITICAL: More births occur in off-track countries with lower coverage")
        print(f"   • This amplifies the global impact of coverage gaps")

def main():
    """Main analysis function."""
    print("MATERNAL HEALTH COVERAGE ANALYSIS")
    print("=" * 50)
    
    try:
        # Load data
        df = load_data()
        
        # Analyze ANC4 coverage
        anc4_results = analyze_coverage_by_indicator(df, 'ANC4')
        
        # Analyze SBA coverage
        sba_results = analyze_coverage_by_indicator(df, 'SBA')
        
        # Save results
        save_detailed_results(df, anc4_results, sba_results)
        
        # Print interpretation
        print_interpretation(anc4_results, sba_results)
        
        print(f"\n{'='*80}")
        print("ANALYSIS COMPLETED SUCCESSFULLY")
        print(f"{'='*80}")
        print("\nOutput files created:")
        print("• 05_output/reports/coverage_analysis_summary.csv")
        print("• 05_output/reports/coverage_analysis_detailed.csv")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main()
