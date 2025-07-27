import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

# Directory paths
RAW_DATA_DIR = PROJECT_ROOT / "01_rawdata"
PROCESSED_DATA_DIR = PROJECT_ROOT / "02_processeddata"
SCRIPTS_DIR = PROJECT_ROOT / "03_scripts"
DOCUMENTATION_DIR = PROJECT_ROOT / "04_documentation"
OUTPUT_DIR = PROJECT_ROOT / "05_output"
FIGURES_DIR = OUTPUT_DIR / "figures"
REPORTS_DIR = OUTPUT_DIR / "reports"

# Data file paths
UNICEF_DATA_FILE = RAW_DATA_DIR / "GLOBAL_DATAFLOW_2018-2022.xlsx"
POPULATION_DATA_FILE = RAW_DATA_DIR / "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"
MORTALITY_CLASS_FILE = RAW_DATA_DIR / "On-track and off-track countries.xlsx"

# Processed data file paths
MERGED_DATA_FILE = PROCESSED_DATA_DIR / "merged_health_data.csv"
RESULTS_SUMMARY_FILE = PROCESSED_DATA_DIR / "coverage_results.csv"

# Output file paths
COMPARISON_CHART = FIGURES_DIR / "health_coverage_comparison.png"
FINAL_REPORT = REPORTS_DIR / "health_coverage_analysis_report.html"

# Analysis parameters
TARGET_YEARS = [2018, 2019, 2020, 2021, 2022]
REFERENCE_YEAR = 2022

# Ensure directories exist
for directory in [PROCESSED_DATA_DIR, SCRIPTS_DIR, DOCUMENTATION_DIR, 
                  OUTPUT_DIR, FIGURES_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)