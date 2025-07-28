"""
Quarto Report Generation Script for Maternal Health Coverage Analysis
===================================================================

Purpose: Generate and render Quarto report with visualization and interpretation
of maternal health coverage gaps between on-track and off-track countries.

This script:
- Verifies data availability
- Renders the Quarto document to HTML in 05_output/reports/
- Provides summary of the generated report

Author: Data Analysis Team
Date: 2025
"""

import subprocess
import sys
import shutil
from pathlib import Path
import pandas as pd

def check_data_availability():
    """
    Check if required data files exist for the report.
    
    Returns:
    --------
    bool : True if all required data files exist
    """
    # Get project root directory (two levels up from this script)
    project_root = Path(__file__).parent.parent.parent
    
    required_files = [
        project_root / "05_output/reports/coverage_analysis_summary.csv",
        project_root / "05_output/reports/coverage_analysis_detailed.csv",
        project_root / "05_output/figures/maternal_health_coverage_comparison.png"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not file_path.exists():
            missing_files.append(str(file_path))
    
    if missing_files:
        print("ERROR: Missing required data files:")
        for file in missing_files:
            print(f"  - {file}")
        print("\nPlease run the data analysis pipeline first to generate these files.")
        return False
    
    print("✓ All required data files found")
    return True

def check_quarto_installation():
    """
    Check if Quarto is installed and available.
    
    Returns:
    --------
    bool : True if Quarto is available
    """
    try:
        result = subprocess.run(['quarto', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✓ Quarto found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: Quarto not found. Please install Quarto:")
        print("  - Visit: https://quarto.org/docs/get-started/")
        print("  - Or install via conda: conda install -c conda-forge quarto")
        return False

def render_quarto_report():
    """
    Render the Quarto report to HTML and move it to the correct output directory.
    
    Returns:
    --------
    bool : True if rendering was successful
    """
    # Get project root directory (two levels up from this script)
    project_root = Path(__file__).parent.parent.parent
    qmd_file = project_root / "04_documentation/maternal_health_report.qmd"
    
    if not qmd_file.exists():
        print(f"ERROR: Quarto file not found: {qmd_file}")
        return False
    
    print(f"Rendering Quarto report: {qmd_file}")
    
    try:
        # Change to the documentation directory to ensure relative paths work
        result = subprocess.run([
            'quarto', 'render', str(qmd_file.name)
        ], 
        cwd=qmd_file.parent,
        capture_output=True, 
        text=True, 
        check=True)
        
        print("✓ Quarto report rendered successfully")
        
        # Check if HTML file was created in the documentation directory
        temp_html_file = qmd_file.with_suffix('.html')
        if temp_html_file.exists():
            # Move the HTML file to the correct output directory
            output_dir = project_root / "05_output/reports"
            output_dir.mkdir(parents=True, exist_ok=True)
            final_html_file = output_dir / "maternal_health_report.html"
            
            # Move the file
            shutil.move(str(temp_html_file), str(final_html_file))
            print(f"✓ HTML report moved to: {final_html_file}")
            
            return True
        else:
            print("WARNING: HTML file not found after rendering")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Quarto rendering failed")
        print(f"Return code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def clean_up_temp_files():
    """
    Clean up any temporary HTML files that might be left in other directories.
    """
    # Get project root directory (two levels up from this script)
    project_root = Path(__file__).parent.parent.parent
    
    # Remove any HTML files in the notebooks directory
    notebooks_html = project_root / "06_notebooks/maternal_health_report.html"
    if notebooks_html.exists():
        notebooks_html.unlink()
        print(f"✓ Removed temporary file: {notebooks_html}")

def get_report_summary():
    """
    Generate a summary of the report contents based on the data.
    
    Returns:
    --------
    dict : Summary statistics for the report
    """
    try:
        # Get project root directory (two levels up from this script)
        project_root = Path(__file__).parent.parent.parent
        
        # Load summary data
        summary_df = pd.read_csv(project_root / "05_output/reports/coverage_analysis_summary.csv")
        detailed_df = pd.read_csv(project_root / "05_output/reports/coverage_analysis_detailed.csv")
        
        # Calculate key statistics
        stats = {}
        
        # Basic counts
        stats['total_countries'] = len(detailed_df)
        stats['on_track_countries'] = len(detailed_df[detailed_df['Mortality_Status_Binary'] == 'on-track'])
        stats['off_track_countries'] = len(detailed_df[detailed_df['Mortality_Status_Binary'] == 'off-track'])
        
        # Coverage gaps
        for indicator in ['ANC4', 'SBA']:
            gap_row = summary_df[(summary_df['Indicator'] == indicator) & 
                               (summary_df['Track_Status'] == 'gap_analysis')]
            if len(gap_row) > 0:
                stats[f'{indicator.lower()}_gap'] = gap_row['Weighted_Coverage_Percent'].iloc[0]
        
        return stats
        
    except Exception as e:
        print(f"Warning: Could not generate report summary: {e}")
        return {}

def print_completion_summary(stats, html_file):
    """
    Print a summary of the completed report generation.
    
    Parameters:
    -----------
    stats : dict
        Summary statistics
    html_file : Path
        Path to the generated HTML file
    """
    print("\n" + "="*70)
    print("QUARTO REPORT GENERATION COMPLETED")
    print("="*70)
    
    print(f"\nReport generated: {html_file}")
    if html_file.exists():
        file_size = html_file.stat().st_size / 1024
        print(f"File size: {file_size:.1f} KB")
    
    print("\nReport Contents:")
    print("• Exact same visualization as 05_output/figures/maternal_health_coverage_comparison.png")
    print("• Results interpretation with key findings")
    print("• Caveats and assumptions section")
    print("• Professional HTML formatting with embedded resources")
    
    if stats:
        print(f"\nKey Statistics:")
        print(f"• {stats.get('total_countries', 'N/A')} countries analyzed")
        if 'anc4_gap' in stats:
            print(f"• {stats['anc4_gap']:.1f}pp ANC4+ coverage gap")
        if 'sba_gap' in stats:
            print(f"• {stats['sba_gap']:.1f}pp SBA coverage gap")
    
    print(f"\n{'='*70}")
    print("QUARTO REPORT READY")
    print(f"{'='*70}")
    
    print(f"\nTo view the report:")
    print(f"  open {html_file}")

def main():
    """Main function to generate the Quarto report."""
    print("MATERNAL HEALTH COVERAGE QUARTO REPORT GENERATION")
    print("=" * 55)
    
    # Check prerequisites
    if not check_data_availability():
        return False
    
    if not check_quarto_installation():
        return False
    
    # Clean up any existing temporary files
    clean_up_temp_files()
    
    # Render the report
    if not render_quarto_report():
        return False
    
    # Generate summary
    stats = get_report_summary()
    
    # Get project root directory (two levels up from this script)
    project_root = Path(__file__).parent.parent.parent
    html_file = project_root / "05_output/reports/maternal_health_report.html"
    
    # Print completion summary
    print_completion_summary(stats, html_file)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
