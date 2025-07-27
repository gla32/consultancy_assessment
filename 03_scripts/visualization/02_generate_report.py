"""
HTML Report Generation Script for Maternal Health Coverage Analysis
==================================================================

Purpose: Create comprehensive HTML report with findings and interpretation
of maternal health coverage gaps between on-track and off-track countries.

This script generates a professional HTML report including:
- Executive summary
- Methodology description
- Results table and visualization
- Key findings and interpretation
- Policy implications
- Limitations and assumptions

Author: Data Analysis Team
Date: 2025
"""

import pandas as pd
import base64
from pathlib import Path
from datetime import datetime
import numpy as np

def load_analysis_data():
    """
    Load all necessary data for the report.
    
    Returns:
    --------
    dict : Dictionary containing all loaded datasets
    """
    data = {}
    
    # Load summary statistics
    summary_path = Path("05_output/reports/coverage_analysis_summary.csv")
    if summary_path.exists():
        data['summary'] = pd.read_csv(summary_path)
    else:
        raise FileNotFoundError(f"Summary data not found: {summary_path}")
    
    # Load detailed country data
    detailed_path = Path("05_output/reports/coverage_analysis_detailed.csv")
    if detailed_path.exists():
        data['detailed'] = pd.read_csv(detailed_path)
    else:
        raise FileNotFoundError(f"Detailed data not found: {detailed_path}")
    
    # Load chart image
    chart_path = Path("05_output/figures/maternal_health_coverage_comparison.png")
    if chart_path.exists():
        with open(chart_path, "rb") as img_file:
            data['chart_base64'] = base64.b64encode(img_file.read()).decode('utf-8')
    else:
        print(f"Warning: Chart image not found: {chart_path}")
        data['chart_base64'] = None
    
    print(f"Loaded data: Summary ({len(data['summary'])} rows), Detailed ({len(data['detailed'])} rows)")
    return data

def calculate_summary_statistics(data):
    """
    Calculate key summary statistics for the report.
    
    Parameters:
    -----------
    data : dict
        Dictionary containing loaded datasets
    
    Returns:
    --------
    dict : Dictionary containing calculated statistics
    """
    summary_df = data['summary']
    detailed_df = data['detailed']
    
    stats = {}
    
    # Basic counts
    stats['total_countries'] = len(detailed_df)
    stats['on_track_countries'] = len(detailed_df[detailed_df['Mortality_Status_Binary'] == 'on-track'])
    stats['off_track_countries'] = len(detailed_df[detailed_df['Mortality_Status_Binary'] == 'off-track'])
    
    # Coverage statistics for each indicator
    for indicator in ['ANC4', 'SBA']:
        indicator_data = summary_df[summary_df['Indicator'] == indicator]
        
        on_track_row = indicator_data[indicator_data['Track_Status'] == 'on-track']
        off_track_row = indicator_data[indicator_data['Track_Status'] == 'off-track']
        gap_row = indicator_data[indicator_data['Track_Status'] == 'gap_analysis']
        
        if len(on_track_row) > 0 and len(off_track_row) > 0:
            stats[f'{indicator.lower()}_on_track'] = on_track_row['Weighted_Coverage_Percent'].iloc[0]
            stats[f'{indicator.lower()}_off_track'] = off_track_row['Weighted_Coverage_Percent'].iloc[0]
            stats[f'{indicator.lower()}_gap'] = gap_row['Weighted_Coverage_Percent'].iloc[0] if len(gap_row) > 0 else (
                stats[f'{indicator.lower()}_on_track'] - stats[f'{indicator.lower()}_off_track']
            )
            stats[f'{indicator.lower()}_on_track_countries'] = int(on_track_row['N_Countries'].iloc[0])
            stats[f'{indicator.lower()}_off_track_countries'] = int(off_track_row['N_Countries'].iloc[0])
    
    # Calculate total births by track status
    on_track_births = detailed_df[detailed_df['Mortality_Status_Binary'] == 'on-track']['Births_2022'].sum()
    off_track_births = detailed_df[detailed_df['Mortality_Status_Binary'] == 'off-track']['Births_2022'].sum()
    
    stats['on_track_births_millions'] = on_track_births / 1000
    stats['off_track_births_millions'] = off_track_births / 1000
    stats['total_births_millions'] = (on_track_births + off_track_births) / 1000
    
    return stats

def generate_executive_summary(stats):
    """Generate executive summary HTML content."""
    return f"""
    <div class="section">
        <h2>Executive Summary</h2>
        <div class="summary-box">
            <p><strong>Key Finding:</strong> Significant maternal health coverage gaps exist between countries on-track and off-track to meet SDG 3.1 targets, with population-weighted coverage differences of <strong>{stats['anc4_gap']:.1f} percentage points</strong> for antenatal care and <strong>{stats['sba_gap']:.1f} percentage points</strong> for skilled birth attendance.</p>
        </div>
        
        <div class="key-metrics">
            <div class="metric-card">
                <h3>Countries Analyzed</h3>
                <div class="metric-value">{stats['total_countries']}</div>
                <div class="metric-detail">{stats['on_track_countries']} on-track, {stats['off_track_countries']} off-track</div>
            </div>
            <div class="metric-card">
                <h3>Total Births (2022)</h3>
                <div class="metric-value">{stats['total_births_millions']:.1f}M</div>
                <div class="metric-detail">{stats['on_track_births_millions']:.1f}M on-track, {stats['off_track_births_millions']:.1f}M off-track</div>
            </div>
            <div class="metric-card">
                <h3>ANC4+ Coverage Gap</h3>
                <div class="metric-value">{stats['anc4_gap']:.1f}pp</div>
                <div class="metric-detail">{stats['anc4_on_track']:.1f}% vs {stats['anc4_off_track']:.1f}%</div>
            </div>
            <div class="metric-card">
                <h3>SBA Coverage Gap</h3>
                <div class="metric-value">{stats['sba_gap']:.1f}pp</div>
                <div class="metric-detail">{stats['sba_on_track']:.1f}% vs {stats['sba_off_track']:.1f}%</div>
            </div>
        </div>
        
        <p><strong>Critical Implications:</strong> The coverage gaps represent millions of women and newborns lacking access to essential maternal health services. Off-track countries, which account for {stats['off_track_births_millions']:.1f} million births annually ({(stats['off_track_births_millions']/stats['total_births_millions']*100):.1f}% of global births), require immediate, targeted interventions to achieve universal health coverage and reduce maternal mortality.</p>
    </div>
    """

def generate_methodology_section():
    """Generate methodology description HTML content."""
    return """
    <div class="section">
        <h2>Methodology</h2>
        
        <h3>Data Sources</h3>
        <ul>
            <li><strong>Health Coverage Data:</strong> WHO Global Health Observatory (GHO) database, 2018-2022</li>
            <li><strong>Demographic Data:</strong> UN World Population Prospects 2022 Revision</li>
            <li><strong>SDG Progress Classification:</strong> WHO/UNICEF/UNFPA/World Bank/UNDESA maternal mortality tracking</li>
        </ul>
        
        <h3>Indicators Analyzed</h3>
        <div class="indicator-definitions">
            <div class="indicator-def">
                <h4>Antenatal Care Coverage (ANC4+)</h4>
                <p>Percentage of women aged 15-49 years with a live birth who received antenatal care four or more times during pregnancy, as recommended by WHO guidelines.</p>
            </div>
            <div class="indicator-def">
                <h4>Skilled Birth Attendance (SBA)</h4>
                <p>Percentage of births attended by skilled health personnel (doctors, nurses, or midwives) trained in providing lifesaving obstetric care.</p>
            </div>
        </div>
        
        <h3>Analysis Approach</h3>
        <ol>
            <li><strong>Country Classification:</strong> Countries categorized as "on-track" or "off-track" based on progress toward SDG 3.1 target (reducing maternal mortality ratio to less than 70 per 100,000 live births by 2030)</li>
            <li><strong>Population Weighting:</strong> Coverage percentages weighted by annual births (2022) to reflect population-level impact</li>
            <li><strong>Gap Analysis:</strong> Calculated absolute differences in coverage between on-track and off-track countries</li>
            <li><strong>Data Quality:</strong> Analysis limited to countries with available data for each indicator</li>
        </ol>
        
        <h3>Statistical Methods</h3>
        <p>Population-weighted coverage calculated as:</p>
        <div class="formula">
            Weighted Coverage = Σ(Coverage<sub>i</sub> × Births<sub>i</sub>) / Σ(Births<sub>i</sub>)
        </div>
        <p>where i represents individual countries within each track status group.</p>
    </div>
    """

def generate_results_section(data, stats):
    """Generate results section with table and visualization."""
    summary_df = data['summary']
    chart_html = ""
    
    if data['chart_base64']:
        chart_html = f"""
        <div class="chart-container">
            <img src="data:image/png;base64,{data['chart_base64']}" alt="Maternal Health Coverage Comparison Chart" class="chart-image">
            <p class="chart-caption">Figure 1: Population-weighted maternal health coverage by SDG 3.1 track status. Error bars show coverage gaps between on-track and off-track countries.</p>
        </div>
        """
    
    # Create summary table
    table_rows = ""
    for _, row in summary_df[summary_df['Track_Status'].isin(['on-track', 'off-track'])].iterrows():
        indicator_name = "Antenatal Care (ANC4+)" if row['Indicator'] == 'ANC4' else "Skilled Birth Attendance (SBA)"
        table_rows += f"""
        <tr>
            <td>{indicator_name}</td>
            <td>{row['Track_Status'].title()}</td>
            <td>{int(row['N_Countries'])}</td>
            <td>{row['Total_Births']/1000:.1f}M</td>
            <td>{row['Weighted_Coverage_Percent']:.1f}%</td>
            <td>{row['Min_Coverage_Percent']:.1f}%</td>
            <td>{row['Max_Coverage_Percent']:.1f}%</td>
            <td>{row['Median_Coverage_Percent']:.1f}%</td>
        </tr>
        """
    
    return f"""
    <div class="section">
        <h2>Results</h2>
        
        <h3>Coverage Comparison Visualization</h3>
        {chart_html}
        
        <h3>Summary Statistics Table</h3>
        <div class="table-container">
            <table class="results-table">
                <thead>
                    <tr>
                        <th>Indicator</th>
                        <th>Track Status</th>
                        <th>Countries (n)</th>
                        <th>Total Births</th>
                        <th>Weighted Coverage</th>
                        <th>Min Coverage</th>
                        <th>Max Coverage</th>
                        <th>Median Coverage</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
        
        <h3>Coverage Gap Analysis</h3>
        <div class="gap-analysis">
            <div class="gap-item">
                <h4>Antenatal Care (ANC4+)</h4>
                <p><strong>Coverage Gap:</strong> {stats['anc4_gap']:.1f} percentage points</p>
                <p><strong>Relative Difference:</strong> {(stats['anc4_gap']/stats['anc4_off_track']*100):.1f}% higher coverage in on-track countries</p>
                <p><strong>Affected Population:</strong> Approximately {(stats['anc4_gap']/100 * stats['off_track_births_millions']):.1f} million additional women could receive adequate antenatal care if off-track countries achieved on-track coverage levels</p>
            </div>
            <div class="gap-item">
                <h4>Skilled Birth Attendance (SBA)</h4>
                <p><strong>Coverage Gap:</strong> {stats['sba_gap']:.1f} percentage points</p>
                <p><strong>Relative Difference:</strong> {(stats['sba_gap']/stats['sba_off_track']*100):.1f}% higher coverage in on-track countries</p>
                <p><strong>Affected Population:</strong> Approximately {(stats['sba_gap']/100 * stats['off_track_births_millions']):.1f} million additional births could be attended by skilled personnel if off-track countries achieved on-track coverage levels</p>
            </div>
        </div>
    </div>
    """

def generate_findings_section(stats, data):
    """Generate key findings and interpretation section."""
    detailed_df = data['detailed']
    
    # Find countries with largest gaps
    anc4_data = detailed_df[detailed_df['ANC4'].notna()].copy()
    sba_data = detailed_df[detailed_df['SBA'].notna()].copy()
    
    # Countries with lowest coverage in off-track group
    off_track_anc4 = anc4_data[anc4_data['Mortality_Status_Binary'] == 'off-track'].nsmallest(3, 'ANC4')
    off_track_sba = sba_data[sba_data['Mortality_Status_Binary'] == 'off-track'].nsmallest(3, 'SBA')
    
    lowest_anc4 = ", ".join([f"{row['Country']} ({row['ANC4']:.1f}%)" for _, row in off_track_anc4.iterrows()])
    lowest_sba = ", ".join([f"{row['Country']} ({row['SBA']:.1f}%)" for _, row in off_track_sba.iterrows()])
    
    return f"""
    <div class="section">
        <h2>Key Findings and Interpretation</h2>
        
        <h3>Primary Findings</h3>
        <div class="findings-list">
            <div class="finding-item">
                <h4>1. Substantial Coverage Disparities</h4>
                <p>Off-track countries demonstrate significantly lower maternal health service coverage across both indicators. The {stats['anc4_gap']:.1f} percentage point gap in ANC4+ coverage and {stats['sba_gap']:.1f} percentage point gap in SBA coverage represent substantial disparities that directly impact maternal and newborn health outcomes.</p>
            </div>
            
            <div class="finding-item">
                <h4>2. Population-Level Impact</h4>
                <p>Off-track countries account for {stats['off_track_births_millions']:.1f} million births annually ({(stats['off_track_births_millions']/stats['total_births_millions']*100):.1f}% of the global total), meaning coverage gaps affect a substantial portion of the world's pregnant women and newborns. This represents approximately {(stats['anc4_gap']/100 * stats['off_track_births_millions']):.1f} million women lacking adequate antenatal care and {(stats['sba_gap']/100 * stats['off_track_births_millions']):.1f} million births without skilled attendance.</p>
            </div>
            
            <div class="finding-item">
                <h4>3. Service-Specific Patterns</h4>
                <p><strong>Antenatal Care:</strong> Shows the larger coverage gap ({stats['anc4_gap']:.1f}pp), with on-track countries achieving {stats['anc4_on_track']:.1f}% coverage compared to {stats['anc4_off_track']:.1f}% in off-track countries. This suggests particular challenges in establishing comprehensive prenatal care systems.</p>
                <p><strong>Skilled Birth Attendance:</strong> Demonstrates a {stats['sba_gap']:.1f}pp gap, with generally higher overall coverage levels ({stats['sba_on_track']:.1f}% vs {stats['sba_off_track']:.1f}%), indicating that delivery care may be more prioritized than comprehensive antenatal services.</p>
            </div>
            
            <div class="finding-item">
                <h4>4. Countries Requiring Urgent Attention</h4>
                <p><strong>Lowest ANC4+ Coverage:</strong> {lowest_anc4}</p>
                <p><strong>Lowest SBA Coverage:</strong> {lowest_sba}</p>
                <p>These countries represent priority targets for immediate intervention and support.</p>
            </div>
        </div>
        
        <h3>Interpretation in Context</h3>
        <p>The observed coverage gaps align with broader patterns of health system capacity and maternal mortality outcomes. Countries off-track for SDG 3.1 face multiple, interconnected challenges including:</p>
        <ul>
            <li><strong>Health System Capacity:</strong> Limited infrastructure, workforce shortages, and inadequate supply chains</li>
            <li><strong>Geographic Barriers:</strong> Rural populations with limited access to health facilities</li>
            <li><strong>Economic Constraints:</strong> Both at health system and household levels</li>
            <li><strong>Social Determinants:</strong> Gender inequality, education levels, and cultural factors affecting care-seeking</li>
        </ul>
        
        <p>The larger gap in antenatal care compared to skilled birth attendance suggests that while emergency delivery care receives priority attention, comprehensive prenatal care systems require additional focus and investment.</p>
    </div>
    """

def generate_policy_implications():
    """Generate policy implications section."""
    return """
    <div class="section">
        <h2>Policy Implications</h2>
        
        <h3>Immediate Priorities</h3>
        <div class="policy-recommendations">
            <div class="recommendation">
                <h4>1. Targeted Investment in Off-Track Countries</h4>
                <p>Prioritize resource allocation and technical assistance to the 48 countries off-track for SDG 3.1, focusing on those with the lowest coverage levels. This includes both financial support and capacity-building initiatives.</p>
            </div>
            
            <div class="recommendation">
                <h4>2. Strengthen Antenatal Care Systems</h4>
                <p>Given the larger coverage gap in ANC4+, specific attention should be paid to establishing comprehensive antenatal care programs that ensure women receive the recommended minimum of four visits with quality care.</p>
            </div>
            
            <div class="recommendation">
                <h4>3. Integrated Service Delivery</h4>
                <p>Develop integrated maternal health service delivery models that combine antenatal care, skilled birth attendance, and postnatal care to maximize efficiency and coverage.</p>
            </div>
        </div>
        
        <h3>Strategic Approaches</h3>
        <div class="strategic-approaches">
            <h4>Health System Strengthening</h4>
            <ul>
                <li>Expand health workforce training and deployment, particularly in rural areas</li>
                <li>Improve health facility infrastructure and equipment</li>
                <li>Strengthen supply chain management for essential medicines and supplies</li>
                <li>Implement quality improvement programs for maternal health services</li>
            </ul>
            
            <h4>Financial Protection and Access</h4>
            <ul>
                <li>Remove financial barriers through universal health coverage mechanisms</li>
                <li>Implement targeted subsidies or voucher programs for maternal health services</li>
                <li>Address transportation and geographic barriers to care</li>
                <li>Develop community-based service delivery models</li>
            </ul>
            
            <h4>Data and Monitoring Systems</h4>
            <ul>
                <li>Strengthen health information systems for real-time monitoring</li>
                <li>Improve data quality and coverage for maternal health indicators</li>
                <li>Establish accountability mechanisms for coverage targets</li>
                <li>Support evidence-based decision making at all levels</li>
            </ul>
        </div>
        
        <h3>Global and Regional Coordination</h3>
        <p>The scale of the coverage gaps requires coordinated international action:</p>
        <ul>
            <li><strong>Multilateral Support:</strong> Increased funding through global health initiatives and development banks</li>
            <li><strong>Technical Assistance:</strong> Knowledge sharing and capacity building between countries</li>
            <li><strong>Regional Platforms:</strong> Leverage regional health organizations for peer learning and coordination</li>
            <li><strong>Private Sector Engagement:</strong> Innovative partnerships to expand service delivery and financing</li>
        </ul>
        
        <div class="urgency-note">
            <h4>Urgency of Action</h4>
            <p>With only 5 years remaining to achieve SDG 3.1 by 2030, immediate and sustained action is required. The current coverage gaps, if left unaddressed, will result in preventable maternal and newborn deaths and perpetuate health inequities globally.</p>
        </div>
    </div>
    """

def generate_limitations_section():
    """Generate limitations and assumptions section."""
    return """
    <div class="section">
        <h2>Limitations and Assumptions</h2>
        
        <h3>Data Limitations</h3>
        <div class="limitations-list">
            <div class="limitation-item">
                <h4>Data Availability and Coverage</h4>
                <ul>
                    <li>ANC4+ data available for 86 countries (40 on-track, 46 off-track)</li>
                    <li>SBA data available for 149 countries (101 on-track, 48 off-track)</li>
                    <li>Missing data may bias results if non-reporting countries have systematically different coverage patterns</li>
                    <li>Some countries have data from different years within the 2018-2022 period</li>
                </ul>
            </div>
            
            <div class="limitation-item">
                <h4>Indicator Definitions and Measurement</h4>
                <ul>
                    <li>Coverage indicators reflect service utilization but not necessarily quality of care</li>
                    <li>Skilled birth attendance definition may vary across countries in terms of training standards</li>
                    <li>Self-reported data in household surveys may be subject to recall bias</li>
                    <li>Administrative data may have completeness and accuracy issues</li>
                </ul>
            </div>
            
            <div class="limitation-item">
                <h4>Population Weighting Methodology</h4>
                <ul>
                    <li>Birth data from UN World Population Prospects may not perfectly align with health survey periods</li>
                    <li>Population weighting assumes uniform coverage within countries, which may not reflect subnational variations</li>
                    <li>Negative birth values in some developed countries (indicating population decline) handled as absolute values for weighting</li>
                </ul>
            </div>
        </div>
        
        <h3>Methodological Assumptions</h3>
        <div class="assumptions-list">
            <div class="assumption-item">
                <h4>Country Classification</h4>
                <p>Countries classified as "on-track" or "off-track" based on maternal mortality trends and projections. This classification may not capture recent changes in trajectory or account for data quality issues in mortality estimates.</p>
            </div>
            
            <div class="assumption-item">
                <h4>Causal Relationships</h4>
                <p>Analysis identifies associations between track status and coverage but does not establish causal relationships. Multiple factors contribute to both maternal mortality outcomes and service coverage levels.</p>
            </div>
            
            <div class="assumption-item">
                <h4>Temporal Alignment</h4>
                <p>Assumes that coverage data from 2018-2022 period reflects current service delivery capacity and is representative of recent performance.</p>
            </div>
        </div>
        
        <h3>Interpretation Considerations</h3>
        <div class="considerations">
            <h4>Context-Specific Factors</h4>
            <p>Coverage gaps reflect complex interactions of health system capacity, socioeconomic factors, geographic challenges, and policy environments. Simple comparisons may not capture the full complexity of country-specific contexts.</p>
            
            <h4>Quality vs. Quantity</h4>
            <p>Higher coverage does not automatically translate to better health outcomes if service quality is poor. Quality of care indicators would provide additional insights but are not included in this analysis.</p>
            
            <h4>Equity Considerations</h4>
            <p>National-level coverage figures may mask significant within-country inequities by wealth, education, geographic location, and other social determinants of health.</p>
        </div>
        
        <div class="recommendation-box">
            <h4>Recommendations for Future Analysis</h4>
            <ul>
                <li>Include service quality indicators alongside coverage measures</li>
                <li>Conduct subnational analysis to identify within-country disparities</li>
                <li>Incorporate trend analysis to assess progress over time</li>
                <li>Add cost-effectiveness analysis of different intervention approaches</li>
                <li>Include additional maternal health indicators (e.g., postnatal care, family planning)</li>
            </ul>
        </div>
    </div>
    """

def generate_css_styles():
    """Generate CSS styles for the HTML report."""
    return """
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        
        .header .subtitle {
            font-size: 1.2em;
            margin-top: 10px;
            opacity: 0.9;
        }
        
        .header .date {
            font-size: 1em;
            margin-top: 15px;
            opacity: 0.8;
        }
        
        .section {
            background: white;
            margin-bottom: 30px;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .section h2 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 25px;
            font-size: 1.8em;
        }
        
        .section h3 {
            color: #34495e;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .section h4 {
            color: #2c3e50;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        
        .summary-box {
            background: #e8f4fd;
            border-left: 5px solid #3498db;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        
        .key-metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }
        
        .metric-card {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            transition: transform 0.2s;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .metric-card h3 {
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 1em;
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #3498db;
            margin: 10px 0;
        }
        
        .metric-detail {
            font-size: 0.9em;
            color: #6c757d;
        }
        
        .chart-container {
            text-align: center;
            margin: 30px 0;
        }
        
        .chart-image {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .chart-caption {
            font-style: italic;
            color: #6c757d;
            margin-top: 10px;
            font-size: 0.9em;
        }
        
        .table-container {
            overflow-x: auto;
            margin: 20px 0;
        }
        
        .results-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .results-table th {
            background: #3498db;
            color: white;
            padding: 15px 10px;
            text-align: left;
            font-weight: 600;
        }
        
        .results-table td {
            padding: 12px 10px;
            border-bottom: 1px solid #e9ecef;
        }
        
        .results-table tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        .gap-analysis {
            margin: 25px 0;
        }
        
        .gap-item {
            background: #f8f9fa;
            border-left: 4px solid #e74c3c;
            padding: 20px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .gap-item h4 {
            color: #e74c3c;
            margin-top: 0;
        }
        
        .findings-list {
            margin: 20px 0;
        }
        
        .finding-item {
            background: #f8f9fa;
            border-left: 4px solid #27ae60;
            padding: 20px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .finding-item h4 {
            color: #27ae60;
            margin-top: 0;
        }
        
        .policy-recommendations {
            margin: 20px 0;
        }
        
        .recommendation {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 20px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .recommendation h4 {
            color: #856404;
            margin-top: 0;
        }
        
        .strategic-approaches {
            margin: 20px 0;
        }
        
        .strategic-approaches h4 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
        }
        
        .urgency-note {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .urgency-note h4 {
            color: #721c24;
            margin-top: 0;
        }
        
        .limitations-list, .assumptions-list {
            margin: 20px 0;
        }
        
        .limitation-item, .assumption-item {
            background: #f8f9fa;
            border-left: 4px solid #6c757d;
            padding: 20px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .limitation-item h4, .assumption-item h4 {
            color: #495057;
            margin-top: 0;
        }
        
        .considerations {
            background: #e2e3e5;
            border-radius: 5px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .considerations h4 {
            color: #383d41;
            margin-top: 0;
        }
        
        .recommendation-box {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 5px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .recommendation-box h4 {
            color: #0c5460;
            margin-top: 0;
        }
        
        .indicator-definitions {
            margin: 20px 0;
        }
        
        .indicator-def {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
        }
        
        .indicator-def h4 {
            color: #2c3e50;
            margin-top: 0;
            margin-bottom: 10px;
        }
        
        .formula {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            text-align: center;
            font-size: 1.1em;
        }
        
        ul, ol {
            padding-left: 25px;
        }
        
        li {
            margin: 8px 0;
        }
        
        p {
            margin: 15px 0;
            text-align: justify;
        }
        
        strong {
            color: #2c3e50;
        }
        
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .section {
                padding: 20px;
            }
            
            .key-metrics {
                grid-template-columns: 1fr;
            }
            
            .metric-value {
                font-size: 2em;
            }
            
            .results-table {
                font-size: 0.9em;
            }
            
            .results-table th,
            .results-table td {
                padding: 8px 5px;
            }
        }
    </style>
    """

def generate_html_report(data, stats):
    """Generate the complete HTML report."""
    current_date = datetime.now().strftime("%B %d, %Y")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Maternal Health Coverage Analysis Report</title>
        {generate_css_styles()}
    </head>
    <body>
        <div class="header">
            <h1>Maternal Health Coverage Analysis</h1>
            <div class="subtitle">Coverage Gaps Between On-Track and Off-Track Countries for SDG 3.1</div>
            <div class="date">Report Generated: {current_date}</div>
        </div>
        
        {generate_executive_summary(stats)}
        {generate_methodology_section()}
        {generate_results_section(data, stats)}
        {generate_findings_section(stats, data)}
        {generate_policy_implications()}
        {generate_limitations_section()}
        
        <div class="section">
            <h2>About This Report</h2>
            <p>This report was generated as part of a comprehensive analysis of maternal health coverage gaps between countries on-track and off-track to meet Sustainable Development Goal 3.1. The analysis combines data from WHO Global Health Observatory, UN World Population Prospects, and maternal mortality tracking systems to provide evidence-based insights for policy and program development.</p>
            
            <p><strong>For more information or technical details about this analysis, please contact the Data Analysis Team.</strong></p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #e9ecef; text-align: center; color: #6c757d; font-size: 0.9em;">
                <p>© 2025 Maternal Health Coverage Analysis Project | Generated on {current_date}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def save_html_report(html_content, filename='maternal_health_coverage_report.html'):
    """
    Save the HTML report to file.
    
    Parameters:
    -----------
    html_content : str
        The complete HTML content
    filename : str
        The filename for the saved report
    
    Returns:
    --------
    Path : Path to the saved report
    """
    # Create output directory if it doesn't exist
    output_dir = Path("05_output/reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the HTML file
    output_path = output_dir / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML report saved as: {output_path}")
    return output_path

def print_report_summary(stats, output_path):
    """Print a summary of the generated report."""
    print("\n" + "="*70)
    print("HTML REPORT GENERATION COMPLETED")
    print("="*70)
    
    print(f"\nReport saved to: {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")
    
    print("\nReport Contents:")
    print("• Executive Summary with key metrics")
    print("• Comprehensive methodology description")
    print("• Results with embedded visualization and summary table")
    print("• Detailed findings and interpretation")
    print("• Policy implications and recommendations")
    print("• Limitations and methodological assumptions")
    print("• Professional HTML formatting with responsive design")
    
    print(f"\nKey Statistics Included:")
    print(f"• {stats['total_countries']} countries analyzed")
    print(f"• {stats['anc4_gap']:.1f}pp ANC4+ coverage gap")
    print(f"• {stats['sba_gap']:.1f}pp SBA coverage gap")
    print(f"• {stats['total_births_millions']:.1f}M total births (2022)")
    
    print(f"\n{'='*70}")
    print("REPORT READY FOR DISTRIBUTION")
    print(f"{'='*70}")

def main():
    """Main function to generate the HTML report."""
    print("MATERNAL HEALTH COVERAGE REPORT GENERATION")
    print("=" * 50)
    
    try:
        # Load all necessary data
        print("Loading analysis data...")
        data = load_analysis_data()
        
        # Calculate summary statistics
        print("Calculating summary statistics...")
        stats = calculate_summary_statistics(data)
        
        # Generate HTML report
        print("Generating HTML report...")
        html_content = generate_html_report(data, stats)
        
        # Save the report
        print("Saving HTML report...")
        output_path = save_html_report(html_content)
        
        # Print summary
        print_report_summary(stats, output_path)
        
        return output_path
        
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        raise

if __name__ == "__main__":
    main()
