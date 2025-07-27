# Data Exploration Findings

**Date:** 2025-01-27  
**Script:** `03_scripts/data_preparation/01_explore_data.py` and `01_explore_data_focused.py`

## Overview

This document summarizes the findings from exploring the three Excel files provided for the consultancy assessment.

## File 1: GLOBAL_DATAFLOW_2018-2022.xlsx

### Structure
- **Sheets:** 1 sheet ('Unicef data')
- **Shape:** 1,324 rows × 21 columns
- **Time Coverage:** 2018-2022

### Key Columns
- `Geographic area`: Country/region names (222 unique areas)
- `Indicator`: Type of health indicator (2 unique indicators)
- `TIME_PERIOD`: Year (2018-2022)
- `OBS_VALUE`: Indicator value
- `Sex`: Gender category
- Additional metadata columns for data sources, footnotes, etc.

### Indicators Available
1. **Antenatal care 4+ visits** - percentage of women (aged 15-49 years) attended at least four times during pregnancy by any provider
2. **Skilled birth attendant** - percentage of deliveries attended by skilled health personnel

### 2022 Data Availability
- **Total 2022 records:** 217
- **ANC4 countries with 2022 data:** 82 countries
- **SBA countries with 2022 data:** 110 countries
- **Geographic areas in 2022:** 113 areas

### Geographic Areas
- Mix of individual countries and regional aggregates
- Examples include: Afghanistan, Albania, Africa, (SDGRC) Central Africa, etc.
- Regional codes like "(SDGRC)" indicate SDG regional classifications

## File 2: On-track and off-track countries.xlsx

### Structure
- **Sheets:** 1 sheet ('Sheet1')
- **Shape:** 200 rows × 3 columns

### Columns
- `ISO3Code`: 3-letter country codes
- `OfficialName`: Country names
- `Status.U5MR`: Under-5 mortality reduction status

### Under-5 Mortality Status Distribution
- **Achieved:** 134 countries (67%)
- **Acceleration Needed:** 59 countries (29.5%)
- **On Track:** 7 countries (3.5%)

### Country Examples
- Afghanistan: Acceleration Needed
- Albania: Achieved
- Australia: Achieved

## File 3: WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx

### Structure
- **Sheets:** 2 sheets ('Estimates', 'Projections')
- **Estimates Shape:** 20,596 rows × 65 columns (after header correction)
- **Projections Shape:** 22,598 rows × 65 columns (after header correction)

### Header Issues
- Original file has metadata in first 16 rows
- Actual column headers start at row 16
- Required special parsing to extract proper structure

### Key Columns (Both Sheets)
- `Region, subregion, country or area *`: Geographic identifier (289 unique values)
- `ISO3 Alpha-code`: 3-letter country codes
- `Location code`: Numeric location identifier
- `Year`: Time period
- Multiple demographic indicators (births, deaths, population, life expectancy, etc.)

### Geographic Coverage
- 289 unique geographic entities
- Mix of countries, regions, and global aggregates
- Includes SDG regions and UN regional classifications

### 2022 Data
- Both sheets contain 2022 data
- Estimates sheet: Historical data up to 2022
- Projections sheet: Future projections from 2022 onwards

## Data Quality Issues Identified

### 1. Country Name Inconsistencies
- **UNICEF file:** 222 geographic areas (includes regions)
- **Mortality file:** 200 countries
- **Exact name matches:** 153 countries
- **Issue:** Regional aggregates vs individual countries need separation

### 2. Missing Data
- UNICEF file has significant missing values in confidence intervals and sample sizes
- WPP2022 file has structural missing values due to different data availability by country/year

### 3. File Structure Issues
- WPP2022 file requires special parsing due to metadata in header rows
- Column names in WPP2022 are complex and need cleaning

## Key Indicators for Analysis

### ANC4 (Antenatal Care 4+ Visits)
- **Total records:** 512
- **2022 data available:** 82 countries
- **Indicator definition:** Percentage of women (aged 15-49) who attended at least four antenatal care visits during pregnancy

### SBA (Skilled Birth Attendance)
- **Total records:** 812
- **2022 data available:** 110 countries
- **Indicator definition:** Percentage of deliveries attended by skilled health personnel

### Birth/Population Data (2022)
- Available in WPP2022 file
- Includes births, deaths, population by age/sex
- Can be used for calculating rates and denominators

### Under-5 Mortality Status
- Classification system for SDG progress
- 200 countries classified into 3 categories
- Links to mortality reduction targets

## Data Cleaning Priorities

### 1. Country Name Standardization
- Create mapping between different country naming conventions
- Separate individual countries from regional aggregates
- Handle special cases (e.g., territories, disputed areas)

### 2. WPP2022 File Processing
- Implement proper header parsing (skip first 16 rows)
- Extract relevant demographic indicators for 2022
- Focus on birth-related data for rate calculations

### 3. Indicator Extraction
- Clean and standardize ANC4 and SBA data from UNICEF file
- Filter for 2022 data specifically
- Handle missing values appropriately

### 4. Data Integration
- Create common country identifier across all datasets
- Map mortality status to health indicators
- Prepare merged dataset for analysis

## Recommendations for Next Steps

1. **Create data cleaning script** that addresses the structural issues identified
2. **Develop country name mapping** to standardize geographic identifiers
3. **Extract 2022 baseline data** for ANC4, SBA, and population indicators
4. **Prepare analysis-ready dataset** with all required variables
5. **Document data quality issues** and assumptions made during cleaning

## Files Created
- `03_scripts/data_preparation/01_explore_data.py`: Comprehensive exploration script
- `03_scripts/data_preparation/01_explore_data_focused.py`: Focused exploration with WPP2022 handling
- `04_documentation/data_exploration_findings.md`: This documentation file
