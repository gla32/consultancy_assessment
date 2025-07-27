"""
Visualization Script for Maternal Health Coverage Analysis
=========================================================

Purpose: Create professional comparison charts showing coverage differences
between on-track and off-track countries for health indicators (ANC4 and SBA).

This script generates a grouped bar chart with:
- X-axis: Health indicators (ANC4, SBA)
- Y-axis: Population-weighted coverage (%)
- Two bars per indicator: on-track vs off-track countries
- Professional styling with clear labels and appropriate colors

Author: Data Analysis Team
Date: 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from pathlib import Path
import seaborn as sns

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from user_profile import REPORTS_DIR, FIGURES_DIR

# Set style for professional appearance
plt.style.use('default')
sns.set_palette("husl")

def load_coverage_data():
    """
    Load the coverage analysis summary data.
    
    Returns:
    --------
    pandas.DataFrame : Coverage analysis summary data
    """
    data_path = REPORTS_DIR / "coverage_analysis_summary.csv"
    
    if not data_path.exists():
        raise FileNotFoundError(f"Coverage analysis data not found: {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"Loaded coverage analysis data with {len(df)} rows")
    return df

def prepare_visualization_data(df):
    """
    Prepare data for visualization by extracting coverage values for each indicator and track status.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Coverage analysis summary data
    
    Returns:
    --------
    dict : Dictionary containing organized data for plotting
    """
    # Filter out gap analysis rows
    plot_data = df[df['Track_Status'].isin(['on-track', 'off-track'])].copy()
    
    # Create data structure for plotting
    indicators = ['ANC4', 'SBA']
    track_statuses = ['on-track', 'off-track']
    
    data_dict = {
        'indicators': indicators,
        'on_track_values': [],
        'off_track_values': [],
        'on_track_countries': [],
        'off_track_countries': []
    }
    
    for indicator in indicators:
        indicator_data = plot_data[plot_data['Indicator'] == indicator]
        
        # Get coverage values
        on_track_row = indicator_data[indicator_data['Track_Status'] == 'on-track']
        off_track_row = indicator_data[indicator_data['Track_Status'] == 'off-track']
        
        on_track_coverage = on_track_row['Weighted_Coverage_Percent'].iloc[0] if len(on_track_row) > 0 else 0
        off_track_coverage = off_track_row['Weighted_Coverage_Percent'].iloc[0] if len(off_track_row) > 0 else 0
        
        on_track_n_countries = int(on_track_row['N_Countries'].iloc[0]) if len(on_track_row) > 0 else 0
        off_track_n_countries = int(off_track_row['N_Countries'].iloc[0]) if len(off_track_row) > 0 else 0
        
        data_dict['on_track_values'].append(on_track_coverage)
        data_dict['off_track_values'].append(off_track_coverage)
        data_dict['on_track_countries'].append(on_track_n_countries)
        data_dict['off_track_countries'].append(off_track_n_countries)
    
    return data_dict

def create_comparison_chart(data_dict):
    """
    Create a professional grouped bar chart comparing coverage between track statuses.
    
    Parameters:
    -----------
    data_dict : dict
        Dictionary containing organized data for plotting
    
    Returns:
    --------
    matplotlib.figure.Figure : The created figure
    """
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Define positions and width for bars
    x_pos = np.arange(len(data_dict['indicators']))
    bar_width = 0.35
    
    # Define colors (green for on-track, red for off-track)
    on_track_color = '#2E8B57'  # Sea Green
    off_track_color = '#DC143C'  # Crimson
    
    # Create bars
    bars1 = ax.bar(x_pos - bar_width/2, data_dict['on_track_values'], 
                   bar_width, label='On-track Countries', 
                   color=on_track_color, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    bars2 = ax.bar(x_pos + bar_width/2, data_dict['off_track_values'], 
                   bar_width, label='Off-track Countries', 
                   color=off_track_color, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Add value labels on bars
    def add_value_labels(bars, values, countries):
        for bar, value, n_countries in zip(bars, values, countries):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{value:.1f}%\n(n={n_countries})',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    add_value_labels(bars1, data_dict['on_track_values'], data_dict['on_track_countries'])
    add_value_labels(bars2, data_dict['off_track_values'], data_dict['off_track_countries'])
    
    # Customize the chart
    ax.set_xlabel('Health Indicators', fontsize=14, fontweight='bold')
    ax.set_ylabel('Population-weighted Coverage (%)', fontsize=14, fontweight='bold')
    ax.set_title('Maternal Health Coverage: On-track vs Off-track Countries\n' +
                'Population-weighted Coverage by SDG 3.1 Track Status', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Set x-axis labels
    ax.set_xticks(x_pos)
    ax.set_xticklabels(['Antenatal Care\n(ANC4+)', 'Skilled Birth\nAttendance (SBA)'], 
                       fontsize=12)
    
    # Set y-axis limits and ticks
    ax.set_ylim(0, 110)
    ax.set_yticks(np.arange(0, 111, 10))
    ax.tick_params(axis='y', labelsize=11)
    
    # Add legend
    ax.legend(loc='upper right', fontsize=12, framealpha=0.9)
    
    # Add grid for better readability
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add coverage gap annotations
    for i, (indicator, on_track, off_track) in enumerate(zip(data_dict['indicators'], 
                                                           data_dict['on_track_values'], 
                                                           data_dict['off_track_values'])):
        gap = on_track - off_track
        # Add gap annotation between bars
        ax.annotate(f'Gap: {gap:.1f}pp', 
                   xy=(i, max(on_track, off_track) + 8), 
                   ha='center', va='bottom', 
                   fontsize=10, fontweight='bold', 
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # Add data source note
    ax.text(0.02, 0.02, 'Data Source: WHO Global Health Observatory, UN World Population Prospects 2022\n' +
                       'Note: Coverage values are population-weighted by annual births (2022)',
           transform=ax.transAxes, fontsize=9, style='italic',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    return fig

def save_chart(fig, filename='maternal_health_coverage_comparison.png'):
    """
    Save the chart as a high-resolution PNG file.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        The figure to save
    filename : str
        The filename for the saved chart
    """
    # Save the figure
    output_path = FIGURES_DIR / filename
    fig.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"Chart saved as: {output_path}")
    return output_path

def print_chart_summary(data_dict):
    """
    Print a summary of the chart data.
    
    Parameters:
    -----------
    data_dict : dict
        Dictionary containing the chart data
    """
    print("\n" + "="*60)
    print("CHART DATA SUMMARY")
    print("="*60)
    
    for i, indicator in enumerate(data_dict['indicators']):
        on_track_val = data_dict['on_track_values'][i]
        off_track_val = data_dict['off_track_values'][i]
        gap = on_track_val - off_track_val
        
        on_track_countries = data_dict['on_track_countries'][i]
        off_track_countries = data_dict['off_track_countries'][i]
        
        print(f"\n{indicator} (Antenatal Care 4+ visits)" if indicator == 'ANC4' 
              else f"\n{indicator} (Skilled Birth Attendance):")
        print(f"  On-track countries:  {on_track_val:.1f}% (n={on_track_countries})")
        print(f"  Off-track countries: {off_track_val:.1f}% (n={off_track_countries})")
        print(f"  Coverage gap:        {gap:.1f} percentage points")
        print(f"  Relative difference: {(gap/off_track_val*100):.1f}%")

def main():
    """Main function to create and save the visualization."""
    print("MATERNAL HEALTH COVERAGE VISUALIZATION")
    print("=" * 50)
    
    try:
        # Load data
        df = load_coverage_data()
        
        # Prepare data for visualization
        data_dict = prepare_visualization_data(df)
        
        # Create the chart
        print("\nCreating comparison chart...")
        fig = create_comparison_chart(data_dict)
        
        # Save the chart
        output_path = save_chart(fig)
        
        # Print summary
        print_chart_summary(data_dict)
        
        print(f"\n{'='*60}")
        print("VISUALIZATION COMPLETED SUCCESSFULLY")
        print(f"{'='*60}")
        print(f"\nHigh-resolution chart saved to: {output_path}")
        print("\nChart Features:")
        print("• Grouped bar chart comparing on-track vs off-track countries")
        print("• Population-weighted coverage percentages")
        print("• Professional styling with clear labels and legends")
        print("• Coverage gap annotations")
        print("• Sample size indicators (n=countries)")
        print("• High-resolution PNG format (300 DPI)")
        
        # Display the chart (optional - will show if running interactively)
        plt.show()
        
    except Exception as e:
        print(f"Error creating visualization: {str(e)}")
        raise
    
    finally:
        # Close the figure to free memory
        plt.close('all')

if __name__ == "__main__":
    main()
