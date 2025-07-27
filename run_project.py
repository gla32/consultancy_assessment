#!/usr/bin/env python3
"""
Main Execution Script for Maternal Health Coverage Analysis Project
==================================================================

Purpose: Execute the complete workflow end-to-end, producing the final output
(PDF, HTML, or DOCX report) with proper error handling and progress reporting.

This script executes scripts in the following order:
1. Data exploration (01_explore_data.py)
2. Data cleaning and merging (02_clean_merge_data.py)
3. Coverage analysis (01_calculate_coverage.py)
4. Visualization creation (01_create_plots.py)
5. Report generation (02_generate_report.py)

Key Features:
- Error handling and progress reporting
- Execution summary with timing and file locations
- Graceful handling of script failures
- Comprehensive logging
- Final output validation

"""

import os
import sys
import time
import subprocess
import traceback
from pathlib import Path
from datetime import datetime, timedelta
import logging

# Configure logging
def setup_logging():
    """Set up logging configuration for the execution script."""
    log_dir = Path("05_output/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"project_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return log_file

class ProjectExecutor:
    """Main class for executing the project workflow."""
    
    def __init__(self):
        """Initialize the project executor."""
        self.start_time = datetime.now()
        self.execution_log = []
        self.failed_scripts = []
        self.successful_scripts = []
        self.output_files = []
        
        # Define the execution workflow
        self.workflow_steps = [
            {
                'name': 'Data Exploration',
                'script': '03_scripts/data_preparation/01_explore_data_focused.py',
                'description': 'Explore raw data structure and content with focused analysis',
                'expected_outputs': ['04_documentation/data_exploration_findings.md'],
                'required': True
            },
            {
                'name': 'Data Cleaning and Merging',
                'script': '03_scripts/data_preparation/02_clean_merge_data.py',
                'description': 'Clean and merge datasets into analysis-ready format',
                'expected_outputs': ['02_processed_data/merged_health_data.csv'],
                'required': True
            },
            {
                'name': 'Coverage Analysis',
                'script': '03_scripts/analysis/01_calculate_coverage.py',
                'description': 'Calculate population-weighted coverage by track status',
                'expected_outputs': [
                    '05_output/reports/coverage_analysis_summary.csv',
                    '05_output/reports/coverage_analysis_detailed.csv'
                ],
                'required': True
            },
            {
                'name': 'Visualization Creation',
                'script': '03_scripts/visualization/01_create_plots.py',
                'description': 'Create comparison charts and visualizations',
                'expected_outputs': ['05_output/figures/maternal_health_coverage_comparison.png'],
                'required': True
            },
            {
                'name': 'Report Generation',
                'script': '03_scripts/visualization/02_generate_report.py',
                'description': 'Generate comprehensive HTML report',
                'expected_outputs': ['05_output/reports/maternal_health_coverage_report.html'],
                'required': True
            }
        ]
    
    def print_header(self):
        """Print the execution header."""
        header = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MATERNAL HEALTH COVERAGE ANALYSIS                         ║
║                         PROJECT EXECUTION SCRIPT                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Purpose: Execute complete workflow end-to-end                               ║
║  Author:  Data Analysis Team                                                 ║
║  Date:    {date}                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """.format(date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        print(header)
        logging.info("Starting project execution")
    
    def check_prerequisites(self):
        """Check if all required files and directories exist."""
        logging.info("Checking prerequisites...")
        
        # Check for required raw data files
        required_files = [
            "01_raw_data/GLOBAL_DATAFLOW_2018-2022.xlsx",
            "01_raw_data/On-track and off-track countries.xlsx",
            "01_raw_data/WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            logging.error(f"Missing required data files: {missing_files}")
            return False, missing_files
        
        # Check for required Python packages
        required_packages = ['pandas', 'numpy', 'matplotlib', 'seaborn']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            logging.error(f"Missing required packages: {missing_packages}")
            return False, missing_packages
        
        # Create output directories
        output_dirs = [
            "02_processed_data",
            "04_documentation", 
            "05_output/reports",
            "05_output/figures",
            "05_output/logs"
        ]
        
        for dir_path in output_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        logging.info("Prerequisites check completed successfully")
        return True, []
    
    def execute_script(self, step):
        """
        Execute a single script with error handling and timing.
        
        Parameters:
        -----------
        step : dict
            Dictionary containing step information
        
        Returns:
        --------
        tuple : (success, execution_time, error_message)
        """
        script_path = Path(step['script'])
        step_name = step['name']
        
        logging.info(f"Starting: {step_name}")
        logging.info(f"Script: {script_path}")
        logging.info(f"Description: {step['description']}")
        
        if not script_path.exists():
            error_msg = f"Script not found: {script_path}"
            logging.error(error_msg)
            return False, 0, error_msg
        
        # Record start time
        step_start = time.time()
        
        try:
            # Execute the script
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=1800  # 30 minute timeout
            )
            
            execution_time = time.time() - step_start
            
            if result.returncode == 0:
                logging.info(f"✓ {step_name} completed successfully in {execution_time:.1f}s")
                
                # Check for expected outputs
                missing_outputs = []
                for output_file in step['expected_outputs']:
                    if not Path(output_file).exists():
                        missing_outputs.append(output_file)
                
                if missing_outputs:
                    warning_msg = f"Warning: Expected outputs not found: {missing_outputs}"
                    logging.warning(warning_msg)
                else:
                    # Record successful outputs
                    self.output_files.extend(step['expected_outputs'])
                
                # Log script output if verbose
                if result.stdout:
                    logging.debug(f"Script output:\n{result.stdout}")
                
                return True, execution_time, None
            else:
                error_msg = f"Script failed with return code {result.returncode}"
                if result.stderr:
                    error_msg += f"\nError output:\n{result.stderr}"
                if result.stdout:
                    error_msg += f"\nStandard output:\n{result.stdout}"
                
                logging.error(f"✗ {step_name} failed: {error_msg}")
                return False, execution_time, error_msg
                
        except subprocess.TimeoutExpired:
            execution_time = time.time() - step_start
            error_msg = f"Script timed out after {execution_time:.1f}s"
            logging.error(f"✗ {step_name} timed out")
            return False, execution_time, error_msg
            
        except Exception as e:
            execution_time = time.time() - step_start
            error_msg = f"Unexpected error: {str(e)}\n{traceback.format_exc()}"
            logging.error(f"✗ {step_name} failed with exception: {error_msg}")
            return False, execution_time, error_msg
    
    def execute_workflow(self):
        """Execute the complete workflow."""
        logging.info("Starting workflow execution...")
        
        total_steps = len(self.workflow_steps)
        
        for i, step in enumerate(self.workflow_steps, 1):
            print(f"\n{'='*80}")
            print(f"STEP {i}/{total_steps}: {step['name'].upper()}")
            print(f"{'='*80}")
            
            success, exec_time, error_msg = self.execute_script(step)
            
            # Record execution details
            execution_record = {
                'step': step['name'],
                'script': step['script'],
                'success': success,
                'execution_time': exec_time,
                'error_message': error_msg,
                'timestamp': datetime.now()
            }
            self.execution_log.append(execution_record)
            
            if success:
                self.successful_scripts.append(step['name'])
                print(f"✓ {step['name']} completed successfully ({exec_time:.1f}s)")
            else:
                self.failed_scripts.append(step['name'])
                print(f"✗ {step['name']} failed ({exec_time:.1f}s)")
                
                if step['required']:
                    logging.error(f"Required step failed: {step['name']}")
                    print(f"\nERROR: {error_msg}")
                    print(f"\nWorkflow terminated due to required step failure.")
                    return False
                else:
                    logging.warning(f"Optional step failed: {step['name']}")
                    print(f"\nWARNING: {error_msg}")
                    print(f"Continuing with remaining steps...")
        
        return len(self.failed_scripts) == 0
    
    def validate_outputs(self):
        """Validate that all expected outputs were created."""
        logging.info("Validating output files...")
        
        all_expected_outputs = []
        for step in self.workflow_steps:
            all_expected_outputs.extend(step['expected_outputs'])
        
        missing_outputs = []
        existing_outputs = []
        
        for output_file in all_expected_outputs:
            output_path = Path(output_file)
            if output_path.exists():
                existing_outputs.append(output_file)
                # Get file size
                file_size = output_path.stat().st_size
                logging.info(f"✓ Output exists: {output_file} ({file_size:,} bytes)")
            else:
                missing_outputs.append(output_file)
                logging.warning(f"✗ Missing output: {output_file}")
        
        return existing_outputs, missing_outputs
    
    def generate_execution_summary(self):
        """Generate and display execution summary."""
        end_time = datetime.now()
        total_duration = end_time - self.start_time
        
        print(f"\n{'='*80}")
        print("EXECUTION SUMMARY")
        print(f"{'='*80}")
        
        # Basic statistics
        print(f"Start Time:      {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"End Time:        {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Duration:  {total_duration}")
        print(f"Total Steps:     {len(self.workflow_steps)}")
        print(f"Successful:      {len(self.successful_scripts)}")
        print(f"Failed:          {len(self.failed_scripts)}")
        
        # Step-by-step results
        print(f"\nSTEP EXECUTION DETAILS:")
        print(f"{'-'*80}")
        for record in self.execution_log:
            status = "✓ PASS" if record['success'] else "✗ FAIL"
            print(f"{status} | {record['step']:<25} | {record['execution_time']:>6.1f}s | {record['script']}")
        
        # Failed steps details
        if self.failed_scripts:
            print(f"\nFAILED STEPS:")
            print(f"{'-'*80}")
            for record in self.execution_log:
                if not record['success']:
                    print(f"• {record['step']}: {record['error_message']}")
        
        # Output validation
        existing_outputs, missing_outputs = self.validate_outputs()
        
        print(f"\nOUTPUT FILES:")
        print(f"{'-'*80}")
        if existing_outputs:
            print("✓ Successfully created:")
            for output in existing_outputs:
                output_path = Path(output)
                file_size = output_path.stat().st_size
                mod_time = datetime.fromtimestamp(output_path.stat().st_mtime)
                print(f"  • {output} ({file_size:,} bytes, {mod_time.strftime('%H:%M:%S')})")
        
        if missing_outputs:
            print("✗ Missing outputs:")
            for output in missing_outputs:
                print(f"  • {output}")
        
        # Final status
        print(f"\n{'='*80}")
        if len(self.failed_scripts) == 0 and len(missing_outputs) == 0:
            print("🎉 PROJECT EXECUTION COMPLETED SUCCESSFULLY!")
            print("All steps completed and all expected outputs generated.")
            final_status = "SUCCESS"
        elif len(self.failed_scripts) == 0:
            print("⚠️  PROJECT EXECUTION COMPLETED WITH WARNINGS")
            print("All steps completed but some expected outputs are missing.")
            final_status = "SUCCESS_WITH_WARNINGS"
        else:
            print("❌ PROJECT EXECUTION FAILED")
            print("One or more required steps failed.")
            final_status = "FAILED"
        
        print(f"{'='*80}")
        
        # Log final status
        logging.info(f"Project execution completed with status: {final_status}")
        
        return final_status
    
    def save_execution_report(self):
        """Save detailed execution report to file."""
        report_dir = Path("05_output/reports")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = report_dir / f"execution_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_file, 'w') as f:
            f.write("MATERNAL HEALTH COVERAGE ANALYSIS - EXECUTION REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Execution Date: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Duration: {datetime.now() - self.start_time}\n")
            f.write(f"Working Directory: {os.getcwd()}\n\n")
            
            f.write("WORKFLOW STEPS:\n")
            f.write("-" * 40 + "\n")
            for i, step in enumerate(self.workflow_steps, 1):
                f.write(f"{i}. {step['name']}\n")
                f.write(f"   Script: {step['script']}\n")
                f.write(f"   Description: {step['description']}\n")
                f.write(f"   Required: {step['required']}\n\n")
            
            f.write("EXECUTION RESULTS:\n")
            f.write("-" * 40 + "\n")
            for record in self.execution_log:
                status = "SUCCESS" if record['success'] else "FAILED"
                f.write(f"{record['step']}: {status} ({record['execution_time']:.1f}s)\n")
                if not record['success']:
                    f.write(f"   Error: {record['error_message']}\n")
                f.write("\n")
            
            existing_outputs, missing_outputs = self.validate_outputs()
            
            f.write("OUTPUT FILES:\n")
            f.write("-" * 40 + "\n")
            for output in existing_outputs:
                output_path = Path(output)
                file_size = output_path.stat().st_size
                f.write(f"✓ {output} ({file_size:,} bytes)\n")
            
            for output in missing_outputs:
                f.write(f"✗ {output} (MISSING)\n")
        
        logging.info(f"Execution report saved to: {report_file}")
        return report_file

def main():
    """Main function to execute the project."""
    # Set up logging
    log_file = setup_logging()
    
    try:
        # Initialize executor
        executor = ProjectExecutor()
        
        # Print header
        executor.print_header()
        
        # Check prerequisites
        prereq_ok, missing_items = executor.check_prerequisites()
        if not prereq_ok:
            print(f"\n❌ Prerequisites check failed!")
            print(f"Missing items: {missing_items}")
            print(f"Please ensure all required files and packages are available.")
            return 1
        
        print(f"\n✓ Prerequisites check passed")
        
        # Execute workflow
        workflow_success = executor.execute_workflow()
        
        # Generate summary
        final_status = executor.generate_execution_summary()
        
        # Save execution report
        report_file = executor.save_execution_report()
        
        print(f"\nDetailed execution report saved to: {report_file}")
        print(f"Execution log saved to: {log_file}")
        
        # Return appropriate exit code
        if final_status == "SUCCESS":
            return 0
        elif final_status == "SUCCESS_WITH_WARNINGS":
            return 0  # Still consider success for warnings
        else:
            return 1
            
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Execution interrupted by user")
        logging.warning("Execution interrupted by user")
        return 130
        
    except Exception as e:
        print(f"\n\n❌ Unexpected error during execution:")
        print(f"{str(e)}")
        logging.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
