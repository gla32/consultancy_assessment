
# Consultancy Assessment Project

##  Repository Structure

This repository follows a structured workflow designed for reproducibility and collaborative development:

```
Consultancy-Assessment/
├── README.md                           # Project documentation (this file)
├── user_profile.py                     # Cross-platform configuration system
├── requirements.txt                    # Python dependencies
├── run_project.py                      # Main execution script
├── config.py                           # Legacy configuration (deprecated)
├── .gitignore                          # Git ignore patterns
│
├── 01_raw_data/                        # Raw input datasets
│   ├── GLOBAL_DATAFLOW_2018-2022.xlsx  # UNICEF health indicators
│   ├── On-track and off-track countries.xlsx # SDG 3.1 track status
│   └── WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx # UN population data
│
├── 02_processed_data/                  # Cleaned and merged datasets
│   └── merged_health_data.csv          # Analysis-ready dataset
│
├── 03_scripts/                         # Analysis scripts organized by workflow stage
│   ├── data_preparation/
│   │   ├── 01_explore_data_focused.py  # Targeted data exploration
│   │   ├── 01_explore_data.py          # Comprehensive data exploration
│   │   └── 02_clean_merge_data.py      # Data cleaning and merging
│   ├── analysis/
│   │   └── 01_calculate_coverage.py    # Coverage analysis calculations
│   └── visualization/
│       ├── 01_create_plots.py          # Chart generation
│       └── 02_generate_report.py       # HTML report generation
│
├── 04_documentation/                   # Analysis documentation
│   ├── data_exploration_findings.md    # Data exploration results
│   └── data_cleaning_summary.md        # Data cleaning documentation
│
└── 05_output/                          # Analysis outputs
    ├── figures/
    │   └── maternal_health_coverage_comparison.png # Main visualization
    ├── reports/
    │   ├── coverage_analysis_summary.csv  # Summary statistics
    │   ├── coverage_analysis_detailed.csv # Country-level results
    │   └── maternal_health_coverage_report.html # Final report
    └── logs/                              # Execution logs
        └── project_execution_[timestamp].log
```

###  Folder and File Purposes

#### **Root Directory Files**
- **`user_profile.py`**: Cross-platform configuration system that ensures code runs on any machine by:
  - Detecting system information and Python environment
  - Checking and installing required dependencies
  - Validating data file availability
  - Setting up consistent paths and environment variables
  
- **`run_project.py`**: Main execution script that orchestrates the complete workflow:
  - Executes all analysis steps in correct order
  - Provides comprehensive error handling and logging
  - Generates execution summary and validation reports
  
- **`requirements.txt`**: Python package dependencies with version specifications
- **`config.py`**: Legacy configuration file (deprecated, replaced by user_profile.py)

#### **Data Directories**
- **`01_raw_data/`**: Original, unmodified datasets as provided
  - UNICEF health indicators (ANC4, SBA coverage 2018-2022)
  - UN population projections (births data for weighting)
  - SDG 3.1 track status classifications
  
- **`02_processed_data/`**: Cleaned, standardized, and merged datasets ready for analysis
  - Country names standardized across sources
  - Missing values handled appropriately
  - Regional aggregates filtered out

#### **Scripts Directory (`03_scripts/`)**
Organized by workflow stage for clear separation of concerns:

- **`data_preparation/`**:
  - `01_explore_data_focused.py`: Targeted exploration focusing on key indicators and 2022 data
  - `01_explore_data.py`: Comprehensive exploration of all datasets and sheets
  - `02_clean_merge_data.py`: Data cleaning, standardization, and merging pipeline

- **`analysis/`**:
  - `01_calculate_coverage.py`: Population-weighted coverage calculations and statistical analysis

- **`visualization/`**:
  - `01_create_plots.py`: Professional chart generation with publication-ready styling
  - `02_generate_report.py`: HTML report compilation with embedded visualizations

#### **Documentation Directory (`04_documentation/`)**
- Contains markdown files documenting data exploration findings and cleaning procedures
- Supports reproducibility by documenting analytical decisions and data quality assessments

#### **Output Directory (`05_output/`)**
- **`figures/`**: High-resolution visualizations (PNG format, 300 DPI)
- **`reports/`**: Analysis results in multiple formats (CSV summaries, HTML report)
- **`logs/`**: Detailed execution logs for debugging and validation

------------------------------------------------------------------------

##  How to Reproduce This Analysis

### **Prerequisites**
- Python 3.7 or higher
- Internet connection (for dependency installation)
- ~500MB available memory
- ~50MB storage space

### **Step 1: Environment Setup**
```bash
# Clone the repository
git clone <your-repository-url>
cd Consultancy-Assessment

# Set up and validate environment
python user_profile.py
```

The `user_profile.py` script will:
-  Check system compatibility (Windows/macOS/Linux)
-  Validate Python version and dependencies
-  Confirm data files are present
-  Create necessary output directories
-  Display comprehensive system report

### **Step 2: Install Dependencies (if needed)**
```bash
# If dependencies are missing, install them automatically
python user_profile.py --install-deps

# Alternative: Manual installation
pip install -r requirements.txt
```

### **Step 3: Execute Complete Analysis**
```bash
# Run the entire workflow end-to-end
python run_project.py
```

This will execute the following pipeline:
1. **Data Exploration** → Analyze raw data structure and quality
2. **Data Cleaning** → Standardize and merge datasets
3. **Coverage Analysis** → Calculate population-weighted statistics
4. **Visualization** → Generate professional charts
5. **Report Generation** → Compile final HTML report

**Expected execution time**: 2-5 minutes

### **Step 4: Review Outputs**
After successful execution, check:
- **`05_output/reports/maternal_health_coverage_report.html`** - Final comprehensive report
- **`05_output/figures/maternal_health_coverage_comparison.png`** - Main visualization
- **`05_output/logs/project_execution_[timestamp].log`** - Detailed execution log

### **Alternative: Step-by-Step Execution**
For debugging or detailed analysis:
```bash
# 1. Data exploration
python 03_scripts/data_preparation/01_explore_data_focused.py

# 2. Data cleaning and merging
python 03_scripts/data_preparation/02_clean_merge_data.py

# 3. Coverage analysis
python 03_scripts/analysis/01_calculate_coverage.py

# 4. Visualization
python 03_scripts/visualization/01_create_plots.py

# 5. Report generation
python 03_scripts/visualization/02_generate_report.py
```

### **Troubleshooting**
```bash
# Check environment without making changes
python user_profile.py --check-only

# Regenerate requirements file
python user_profile.py --generate-requirements

# View detailed system information
python user_profile.py
```

### **Cross-Platform Compatibility**
This analysis has been tested and validated on:
-  **Windows** (Windows 10/11)
-  **macOS** (macOS 10.15+)
-  **Linux** (Ubuntu 18.04+, CentOS 7+)

The `user_profile.py` system automatically handles platform-specific differences in:
- File path separators
- Line endings
- Python package management
- Environment variables

------------------------------------------------------------------------

##  Position Applied For

**Household Survey Data Analyst Consultant – Req.#581656**

This project demonstrates proficiency in:

-  Cross-platform Python development and deployment

-  Health data analysis and epidemiological methods

-  Population-weighted statistical analysis

-  Professional data visualization and reporting

-  Reproducible research practices

-  International health data integration and standardization

-  Collaborative workflow design and documentation

------------------------------------------------------------------------

##  Technical Specifications

- **Language**: Python 3.7+
- **Key Libraries**: pandas, numpy, matplotlib, seaborn, openpyxl, xlrd
- **Output Formats**: HTML (primary), PNG (visualizations), CSV (data)
- **Memory Requirements**: ~500MB
- **Storage Requirements**: ~50MB
- **Execution Time**: 2-5 minutes (system dependent)

------------------------------------------------------------------------

##  Methodology Summary

1. **Data Integration**: Merge UNICEF health indicators, UN population data, and SDG track classifications using standardized country identifiers
2. **Population Weighting**: Calculate coverage using births as weights: Σ(coverage_i × births_i) / Σ(births_i)
3. **Comparative Analysis**: Statistical comparison between on-track and off-track countries
4. **Quality Assurance**: Comprehensive validation, logging, and cross-platform testing
5. **Professional Reporting**: Publication-ready visualizations and comprehensive documentation

------------------------------------------------------------------------
