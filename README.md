
# Consultancy Assessment Project

## Project Summary

This project analyzes maternal health coverage disparities between countries on-track and off-track for achieving SDG 3.1 (reducing maternal mortality). Using UNICEF health indicators, UN population data, and SDG tracking classifications, the analysis calculates population-weighted coverage rates for key maternal health interventions (ANC4 and skilled birth attendance) and compares outcomes between country groups.

## How to Reproduce This Analysis

### **Prerequisites**
- Python 3.7 or higher
- Internet connection (for dependency installation)
- ~500MB available memory
- ~50MB storage space
- **Quarto** (for professional report generation) - Install from https://quarto.org/docs/get-started/

### **Step 1: Environment Setup**
```bash
# Clone the repository
git clone https://github.com/gla32/consultancy_assessment.git
cd consultancy_assessment

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
# Install Python dependencies
python user_profile.py --install-deps

# Alternative: Manual installation
pip install -r requirements.txt

# Install Quarto (required for professional report generation)
# Visit https://quarto.org/docs/get-started/ for installation instructions
# Or use package managers:

# On macOS with Homebrew:
# brew install quarto

# On Windows with Chocolatey:
# choco install quarto

# On Linux (Ubuntu/Debian):
# Download from https://github.com/quarto-dev/quarto-cli/releases
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
5. **Quarto Report Generation** → Generate professional Quarto HTML report



### **Step 4: Review Outputs**
After successful execution, check:
- **`05_output/reports/maternal_health_report.html`** - Professional Quarto HTML report
- **`05_output/figures/maternal_health_coverage_comparison.png`** - Main visualization
- **`05_output/logs/project_execution_[timestamp].log`** - Detailed execution log

### **Step 5: Open the Generated Report**
To view the professional Quarto HTML report:

#### **Option 1: Using Command Line**
```bash
# On macOS
open 05_output/reports/maternal_health_report.html

# On Windows
start 05_output/reports/maternal_health_report.html

# On Linux
xdg-open 05_output/reports/maternal_health_report.html
```

#### **Option 2: Using File Explorer/Finder**
1. Navigate to the `05_output/reports/` folder in your file manager
2. Double-click on `maternal_health_report.html`
3. The report will open in your default web browser

#### **Option 3: Direct Browser Access**
1. Open your web browser (Chrome, Firefox, Safari, etc.)
2. Use Ctrl+O (Windows/Linux) or Cmd+O (macOS) to open a file
3. Navigate to and select `05_output/reports/maternal_health_report.html`

**Note**: The generated HTML report is self-contained with embedded resources, so it will display correctly even without an internet connection.

## Repository Structure

This repository follows a structured workflow designed for reproducibility and collaborative development:

```
Consultancy-Assessment/
├── README.md                           # Project documentation (this file)
├── user_profile.py                     # Cross-platform configuration system
├── requirements.txt                    # Python dependencies
├── run_project.py                      # Main execution script
├── Consultancy_Assessment.Rproj        # R project file
├── .gitignore                          # Git ignore patterns
├── .gitattributes                      # Git attributes for notebook handling
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
│       └── 02_generate_quarto_report.py # Professional Quarto report generation
│
├── 04_documentation/                   # Analysis documentation
│   ├── data_exploration_findings.md    # Data exploration results
│   ├── data_cleaning_summary.md        # Data cleaning documentation
│   └── maternal_health_report.qmd      # Quarto document for professional reporting
│
├── 05_output/                          # Analysis outputs
│   ├── figures/
│   │   └── maternal_health_coverage_comparison.png # Main visualization
│   ├── reports/
│   │   ├── coverage_analysis_summary.csv  # Summary statistics
│   │   ├── coverage_analysis_detailed.csv # Country-level results
│   │   └── maternal_health_report.html    # Professional Quarto HTML report
│   └── logs/                              # Execution logs
│       └── project_execution_[timestamp].log
│
└── 06_notebooks/                       # Jupyter notebooks for interactive analysis
    ├── 01_explore_data.ipynb           # Data exploration and analysis
    ├── 02_clean_merge_data.ipynb       # Data cleaning and merging
    ├── 01_calculate_coverage.ipynb     # Coverage analysis calculations
    └── 01_create_plots.ipynb           # Visualization generation
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
  - `02_generate_quarto_report.py`: Professional Quarto report generation with embedded resources

#### **Documentation Directory (`04_documentation/`)**
- Contains markdown files documenting data exploration findings and cleaning procedures
- Supports reproducibility by documenting analytical decisions and data quality assessments

#### **Output Directory (`05_output/`)**
- **`figures/`**: High-resolution visualizations (PNG format, 300 DPI)
- **`reports/`**: Analysis results in multiple formats (CSV summaries, HTML report)
- **`logs/`**: Detailed execution logs for debugging and validation

#### **Notebooks Directory (`06_notebooks/`)**
- **Fully reproducible Jupyter notebooks** for interactive analysis and exploration
- All notebooks tested with "Restart Kernel and Run All Cells" to ensure reproducibility
- Configured with **nbstripout** to automatically strip outputs before committing
- Intelligent path detection works from any execution context (project root, notebooks directory, or scripts directory)
- Contents include:
  - `01_explore_data.ipynb`: Comprehensive data exploration with visualizations
  - `02_clean_merge_data.ipynb`: Interactive data cleaning and merging workflow
  - `01_calculate_coverage.ipynb`: Coverage analysis with statistical comparisons
  - `01_create_plots.ipynb`: Interactive visualization development and refinement


------------------------------------------------------------------------

## Interactive Analysis with Jupyter Notebooks
For interactive exploration and development:
```bash
# Start Jupyter Lab from project root
jupyter lab

# Navigate to 06_notebooks/ and run notebooks in order:
# 1. 01_explore_data.ipynb - Data exploration
# 2. 02_clean_merge_data.ipynb - Data cleaning
# 3. 01_calculate_coverage.ipynb - Coverage analysis
# 4. 01_create_plots.ipynb - Visualization
```

**Note**: All notebooks are fully reproducible and can be run with "Restart Kernel and Run All Cells". Outputs are automatically stripped before committing thanks to nbstripout configuration.


## Cross-Platform Compatibility

This analysis has been tested and validated on:
- **Windows** (Windows 10/11)
- **macOS** (macOS 10.15+)
- **Linux** (Ubuntu 18.04+, CentOS 7+)

The `user_profile.py` system automatically handles platform-specific differences in:
- File path separators
- Line endings
- Python package management
- Environment variables

------------------------------------------------------------------------

## Technical Specifications

- **Language**: Python 3.7+
- **Key Libraries**: pandas, numpy, matplotlib, seaborn, openpyxl, xlrd
- **Output Formats**: HTML (primary), PNG (visualizations), CSV (data)

------------------------------------------------------------------------

## Position Applied For

**Household Survey Data Analyst Consultant – Req.#581656**

This project demonstrates proficiency in:

- Cross-platform Python development
- Statistical analysis, data visualization and reporting
- Reproducible research practices, collaborative workflow design and documentation

------------------------------------------------------------------------

## Support
If you encounter any issues while using this project, or if you have questions about the implementation, you can follow the steps below:
1. Reporting Issues:
 - Use the [Issues](https://github.com/gla32/consultancy_assessment/issues) tab in this repository to report bugs, request new features, or raise any concerns.
 - Provide as much detail as possible, including steps to reproduce the issue, the environment you're running on, and relevant logs or screenshots.
