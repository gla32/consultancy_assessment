#!/usr/bin/env python3
"""
User Profile Configuration for Maternal Health Coverage Analysis
==============================================================

This script ensures the project can run on any machine by:
1. Setting up the correct environment and paths
2. Checking and installing required dependencies
3. Validating data file availability
4. Configuring system-specific settings
5. Providing cross-platform compatibility

Author: Data Analysis Team
Date: 2025-01-27
"""

import os
import sys
import platform
import subprocess
import importlib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class UserProfile:
    """User profile configuration class for cross-platform compatibility."""
    
    def __init__(self):
        """Initialize user profile with system detection and path setup."""
        self.system_info = self._detect_system()
        self.project_root = Path(__file__).parent.absolute()
        self.setup_paths()
        self.setup_environment()
    
    def _detect_system(self):
        """Detect system information for compatibility."""
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'python_executable': sys.executable,
            'working_directory': os.getcwd()
        }
    
    def setup_paths(self):
        """Setup all project paths with cross-platform compatibility."""
        # Core directory paths
        self.RAW_DATA_DIR = self.project_root / "01_raw_data"
        self.PROCESSED_DATA_DIR = self.project_root / "02_processed_data"
        self.SCRIPTS_DIR = self.project_root / "03_scripts"
        self.DOCUMENTATION_DIR = self.project_root / "04_documentation"
        self.OUTPUT_DIR = self.project_root / "05_output"
        
        # Sub-directory paths
        self.FIGURES_DIR = self.OUTPUT_DIR / "figures"
        self.REPORTS_DIR = self.OUTPUT_DIR / "reports"
        self.LOGS_DIR = self.OUTPUT_DIR / "logs"
        
        # Script sub-directories
        self.DATA_PREP_DIR = self.SCRIPTS_DIR / "data_preparation"
        self.ANALYSIS_DIR = self.SCRIPTS_DIR / "analysis"
        self.VISUALIZATION_DIR = self.SCRIPTS_DIR / "visualization"
        
        # Data file paths
        self.UNICEF_DATA_FILE = self.RAW_DATA_DIR / "GLOBAL_DATAFLOW_2018-2022.xlsx"
        self.POPULATION_DATA_FILE = self.RAW_DATA_DIR / "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"
        self.MORTALITY_CLASS_FILE = self.RAW_DATA_DIR / "On-track and off-track countries.xlsx"
        
        # Processed data file paths
        self.MERGED_DATA_FILE = self.PROCESSED_DATA_DIR / "merged_health_data.csv"
        self.COVERAGE_SUMMARY_FILE = self.REPORTS_DIR / "coverage_analysis_summary.csv"
        self.COVERAGE_DETAILED_FILE = self.REPORTS_DIR / "coverage_analysis_detailed.csv"
        
        # Output file paths
        self.COMPARISON_CHART = self.FIGURES_DIR / "maternal_health_coverage_comparison.png"
        self.FINAL_REPORT = self.REPORTS_DIR / "maternal_health_coverage_report.html"
        
        # Documentation files
        self.EXPLORATION_FINDINGS = self.DOCUMENTATION_DIR / "data_exploration_findings.md"
        self.CLEANING_SUMMARY = self.DOCUMENTATION_DIR / "data_cleaning_summary.md"
        
        # Ensure all directories exist
        self._create_directories()
    
    def _create_directories(self):
        """Create all necessary directories if they don't exist."""
        directories = [
            self.RAW_DATA_DIR,
            self.PROCESSED_DATA_DIR,
            self.SCRIPTS_DIR,
            self.DOCUMENTATION_DIR,
            self.OUTPUT_DIR,
            self.FIGURES_DIR,
            self.REPORTS_DIR,
            self.LOGS_DIR,
            self.DATA_PREP_DIR,
            self.ANALYSIS_DIR,
            self.VISUALIZATION_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def setup_environment(self):
        """Setup environment variables and configuration."""
        # Analysis parameters
        self.TARGET_YEARS = [2018, 2019, 2020, 2021, 2022]
        self.REFERENCE_YEAR = 2022
        self.ANALYSIS_INDICATORS = ['ANC4', 'SBA']
        
        # Visualization settings
        self.FIGURE_DPI = 300
        self.FIGURE_FORMAT = 'png'
        self.PLOT_STYLE = 'seaborn-v0_8'
        
        # Data processing settings
        self.ENCODING = 'utf-8'
        self.DECIMAL_PLACES = 2
        self.MISSING_VALUE_THRESHOLD = 0.5  # 50% missing data threshold
        
        # System-specific settings
        if self.system_info['platform'] == 'Windows':
            self.PATH_SEPARATOR = '\\'
            self.LINE_ENDING = '\r\n'
        else:
            self.PATH_SEPARATOR = '/'
            self.LINE_ENDING = '\n'
        
        # Set environment variables
        os.environ['PROJECT_ROOT'] = str(self.project_root)
        os.environ['PYTHONPATH'] = str(self.project_root)
    
    def check_dependencies(self):
        """Check and report on required dependencies."""
        required_packages = {
            'pandas': '>=1.3.0',
            'numpy': '>=1.20.0',
            'matplotlib': '>=3.3.0',
            'seaborn': '>=0.11.0',
            'openpyxl': '>=3.0.0',
            'xlrd': '>=2.0.0',
            'pathlib': 'built-in',
            'datetime': 'built-in',
            'logging': 'built-in'
        }
        
        dependency_status = {}
        missing_packages = []
        
        for package, version_req in required_packages.items():
            try:
                if version_req == 'built-in':
                    # Built-in modules
                    importlib.import_module(package)
                    dependency_status[package] = {'status': 'available', 'version': 'built-in'}
                else:
                    # Third-party packages
                    module = importlib.import_module(package)
                    if hasattr(module, '__version__'):
                        version = module.__version__
                        dependency_status[package] = {'status': 'available', 'version': version}
                    else:
                        dependency_status[package] = {'status': 'available', 'version': 'unknown'}
            except ImportError:
                dependency_status[package] = {'status': 'missing', 'version': None}
                missing_packages.append(package)
        
        return dependency_status, missing_packages
    
    def install_missing_dependencies(self, missing_packages):
        """Install missing dependencies using pip."""
        if not missing_packages:
            return True, "All dependencies are already installed."
        
        print(f"Installing missing packages: {missing_packages}")
        
        try:
            for package in missing_packages:
                print(f"Installing {package}...")
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', package],
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(f"✓ {package} installed successfully")
            
            return True, f"Successfully installed {len(missing_packages)} packages."
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to install packages: {e.stderr}"
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error during installation: {str(e)}"
            return False, error_msg
    
    def validate_data_files(self):
        """Validate that all required data files exist."""
        required_files = {
            'UNICEF Data': self.UNICEF_DATA_FILE,
            'Population Data': self.POPULATION_DATA_FILE,
            'Mortality Classification': self.MORTALITY_CLASS_FILE
        }
        
        file_status = {}
        missing_files = []
        
        for file_desc, file_path in required_files.items():
            if file_path.exists():
                file_size = file_path.stat().st_size
                file_status[file_desc] = {
                    'status': 'available',
                    'path': str(file_path),
                    'size': file_size
                }
            else:
                file_status[file_desc] = {
                    'status': 'missing',
                    'path': str(file_path),
                    'size': 0
                }
                missing_files.append(file_desc)
        
        return file_status, missing_files
    
    def generate_requirements_file(self):
        """Generate requirements.txt file for easy dependency management."""
        requirements_content = """# Maternal Health Coverage Analysis - Requirements
# Generated automatically by user_profile.py

# Core data processing
pandas>=1.3.0
numpy>=1.20.0

# Excel file handling
openpyxl>=3.0.0
xlrd>=2.0.0

# Visualization
matplotlib>=3.3.0
seaborn>=0.11.0

# Additional utilities
pathlib2>=2.3.0; python_version<"3.4"

# Development and testing (optional)
jupyter>=1.0.0
ipykernel>=6.0.0
"""
        
        requirements_file = self.project_root / "requirements.txt"
        
        try:
            with open(requirements_file, 'w') as f:
                f.write(requirements_content)
            return True, str(requirements_file)
        except Exception as e:
            return False, str(e)
    
    def print_system_info(self):
        """Print comprehensive system information."""
        print("=" * 80)
        print("SYSTEM INFORMATION")
        print("=" * 80)
        
        for key, value in self.system_info.items():
            print(f"{key.replace('_', ' ').title():<20}: {value}")
        
        print(f"\nProject Root         : {self.project_root}")
        print(f"Raw Data Directory   : {self.RAW_DATA_DIR}")
        print(f"Output Directory     : {self.OUTPUT_DIR}")
    
    def print_dependency_status(self):
        """Print dependency status report."""
        dependency_status, missing_packages = self.check_dependencies()
        
        print("\n" + "=" * 80)
        print("DEPENDENCY STATUS")
        print("=" * 80)
        
        for package, info in dependency_status.items():
            status_symbol = "✓" if info['status'] == 'available' else "✗"
            version_info = f"({info['version']})" if info['version'] else ""
            print(f"{status_symbol} {package:<15}: {info['status'].upper()} {version_info}")
        
        if missing_packages:
            print(f"\nMissing packages: {missing_packages}")
            print("Run: python user_profile.py --install-deps to install missing packages")
        else:
            print("\n✓ All required dependencies are available!")
    
    def print_data_file_status(self):
        """Print data file availability status."""
        file_status, missing_files = self.validate_data_files()
        
        print("\n" + "=" * 80)
        print("DATA FILE STATUS")
        print("=" * 80)
        
        for file_desc, info in file_status.items():
            status_symbol = "✓" if info['status'] == 'available' else "✗"
            size_info = f"({info['size']:,} bytes)" if info['size'] > 0 else ""
            print(f"{status_symbol} {file_desc:<25}: {info['status'].upper()} {size_info}")
            print(f"   Path: {info['path']}")
        
        if missing_files:
            print(f"\nMissing files: {missing_files}")
            print("Please ensure all required data files are in the 01_raw_data directory")
        else:
            print("\n✓ All required data files are available!")
    
    def setup_complete_environment(self):
        """Complete environment setup with all checks and installations."""
        print("MATERNAL HEALTH COVERAGE ANALYSIS - ENVIRONMENT SETUP")
        print("=" * 80)
        
        # Print system information
        self.print_system_info()
        
        # Check dependencies
        self.print_dependency_status()
        
        # Check data files
        self.print_data_file_status()
        
        # Generate requirements file
        success, result = self.generate_requirements_file()
        if success:
            print(f"\n✓ Requirements file generated: {result}")
        else:
            print(f"\n✗ Failed to generate requirements file: {result}")
        
        # Final status
        dependency_status, missing_packages = self.check_dependencies()
        file_status, missing_files = self.validate_data_files()
        
        print("\n" + "=" * 80)
        print("ENVIRONMENT SETUP SUMMARY")
        print("=" * 80)
        
        if not missing_packages and not missing_files:
            print("🎉 ENVIRONMENT SETUP COMPLETE!")
            print("Your system is ready to run the maternal health coverage analysis.")
            print("\nTo start the analysis, run:")
            print("  python run_project.py")
            return True
        else:
            print("⚠️  ENVIRONMENT SETUP INCOMPLETE")
            if missing_packages:
                print(f"Missing packages: {missing_packages}")
                print("Run: python user_profile.py --install-deps")
            if missing_files:
                print(f"Missing data files: {missing_files}")
                print("Please add the required files to the 01_raw_data directory")
            return False

def main():
    """Main function for user profile setup."""
    import argparse
    
    parser = argparse.ArgumentParser(description='User Profile Setup for Maternal Health Coverage Analysis')
    parser.add_argument('--install-deps', action='store_true', 
                       help='Install missing dependencies automatically')
    parser.add_argument('--check-only', action='store_true',
                       help='Only check environment without installing anything')
    parser.add_argument('--generate-requirements', action='store_true',
                       help='Generate requirements.txt file')
    
    args = parser.parse_args()
    
    # Initialize user profile
    profile = UserProfile()
    
    if args.generate_requirements:
        success, result = profile.generate_requirements_file()
        if success:
            print(f"Requirements file generated: {result}")
        else:
            print(f"Failed to generate requirements file: {result}")
        return
    
    if args.check_only:
        profile.print_system_info()
        profile.print_dependency_status()
        profile.print_data_file_status()
        return
    
    if args.install_deps:
        dependency_status, missing_packages = profile.check_dependencies()
        if missing_packages:
            success, message = profile.install_missing_dependencies(missing_packages)
            print(message)
            if success:
                print("Re-checking dependencies after installation...")
                profile.print_dependency_status()
        else:
            print("All dependencies are already installed.")
        return
    
    # Default: complete environment setup
    profile.setup_complete_environment()

if __name__ == "__main__":
    main()

# Create global profile instance for import
user_profile = UserProfile()

# Export commonly used paths and settings
PROJECT_ROOT = user_profile.project_root
RAW_DATA_DIR = user_profile.RAW_DATA_DIR
PROCESSED_DATA_DIR = user_profile.PROCESSED_DATA_DIR
OUTPUT_DIR = user_profile.OUTPUT_DIR
FIGURES_DIR = user_profile.FIGURES_DIR
REPORTS_DIR = user_profile.REPORTS_DIR

# Export data file paths
UNICEF_DATA_FILE = user_profile.UNICEF_DATA_FILE
POPULATION_DATA_FILE = user_profile.POPULATION_DATA_FILE
MORTALITY_CLASS_FILE = user_profile.MORTALITY_CLASS_FILE
MERGED_DATA_FILE = user_profile.MERGED_DATA_FILE

# Export analysis parameters
TARGET_YEARS = user_profile.TARGET_YEARS
REFERENCE_YEAR = user_profile.REFERENCE_YEAR
ANALYSIS_INDICATORS = user_profile.ANALYSIS_INDICATORS
