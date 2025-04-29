# Telecom ML Project - Checkpoint 1

## Project Structure
- Data generation script: `util-generate-data.py`
- Data analysis script: `scripts/analyze_telecom_data.py`
- Data documentation: `README-synthetic-telecom-data.md`
- Data location: `data/raw/synthetic_data/`

## Dataset Overview

### 1. Network Performance Data
- Location: `data/raw/synthetic_data/network_performance_synthetic.csv`
- Key metrics:
  - `timestamp`: 5-minute intervals
  - `cell_id`: CELL_001 to CELL_020
  - `latency_ms`: 10-200ms range
  - `packet_loss`: 0-0.2 range
  - `throughput_mbps`: 1-100 range
  - `signal_strength_dbm`: -100 to -40 range
  - `connection_type`: '4G', '5G', 'LTE'

### 2. Customer Experience Data
- Location: `data/raw/synthetic_data/customer_experience_synthetic.csv`
- Key metrics:
  - `timestamp`: 5-minute intervals
  - `customer_id`: CUST_0001 to CUST_0100
  - `customer_satisfaction_score`: 1-5 scale
  - `data_usage_mb`: 0-1000 range
  - `voice_minutes`: 0-100 range
  - `sms_count`: 0-50 range
  - `device_type`: 'Smartphone', 'Tablet', 'IoT'
  - `plan_type`: 'Basic', 'Standard', 'Premium'

### 3. Call Detail Records (CDR)
- Location: `data/raw/synthetic_data/call_detail_records_synthetic.csv`
- Key metrics:
  - `timestamp`: 5-minute intervals
  - `caller_id`: CUST_XXXX format
  - `call_duration_seconds`: 0-3600 seconds
  - `data_used_mb`: 0-100 MB
  - `call_type`: 'Voice', 'Video', 'Data'
  - `call_quality_score`: 1-5 scale
  - `network_type`: '4G', '5G', 'LTE'
  - `location`: LOC_XXX format
  - `roaming`: Boolean

## Data Quality Assessment
- Sample size: 1000 records per dataset
- No missing values
- No duplicate rows
- Some outliers detected:
  - Network Performance: 1 latency outlier, 11 throughput outliers
  - Customer Experience: 7 data usage outliers, 17 voice minutes outliers, 5 SMS count outliers
  - Call Detail Records: 11 duration outliers, 13 data usage outliers, 2 quality score outliers

## Data Generation Details
- All datasets use synchronized timestamps starting from 2024-01-01
- Data distributions:
  - Normal distribution: latency, signal strength
  - Gamma distribution: throughput, call durations
  - Beta distribution: packet loss
  - Poisson distribution: SMS counts
  - Categorical distributions: device types, plan types, network types

## Next Steps
1. Feature Engineering:
   - Create time-based features (hour of day, day of week)
   - Aggregate metrics by customer and cell
   - Create interaction features between datasets

2. Model Development:
   - Define target variables (e.g., customer satisfaction, network quality)
   - Split data into training and testing sets
   - Develop baseline models
   - Evaluate model performance

3. Data Validation:
   - Cross-validate relationships between datasets
   - Verify temporal patterns
   - Check for data leakage

## Environment Setup
- Python virtual environment: `.venv`
- Required packages:
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - scipy
  - jupyter

## Notes
- Data is synthetic but follows realistic patterns
- All datasets are temporally aligned
- Customer IDs are consistent across datasets
- Metrics follow industry-standard ranges

## Known Issues and Solutions

### Jupyter Notebook Setup Issues
1. **Notebook Trust Issues**
   - Error: "Notebook is not trusted"
   - Solution: Trust the notebook in Jupyter interface or use `jupyter trust notebook.ipynb`

2. **Port Conflicts**
   - Error: "The port 8888 is already in use, trying another port"
   - Solution: 
     - Kill existing Jupyter processes: `pkill -f jupyter`
     - Or specify a different port: `jupyter notebook --port=8889`

3. **Notebook JSON Errors**
   - Error: "Notebook does not appear to be JSON: ' '"
   - Solution:
     - Ensure notebook file is properly formatted JSON
     - Create new notebook if file is corrupted
     - Use `jupyter notebook --generate-config` to reset configuration

4. **Kernel Connection Issues**
   - Error: "Connecting to kernel" messages with repeated attempts
   - Solution:
     - Restart the kernel
     - Clear all outputs and restart
     - Check for memory issues

5. **File System Permissions**
   - Error: "Failed to find default application for content type 'text/html'"
   - Solution:
     - Ensure proper file permissions
     - Check browser configuration
     - Use `chmod` to set appropriate permissions

### Best Practices for Jupyter Setup
1. Always activate virtual environment before starting Jupyter
2. Use `jupyter notebook --generate-config` for fresh configuration
3. Trust notebooks before running them
4. Monitor system resources (memory, CPU) during long-running notebooks
5. Save work frequently and maintain backup copies of important notebooks 

### Matplotlib Style Issues
1. **Seaborn Style Not Found**
   - Error: "OSError: 'seaborn' is not a valid package style"
   - Solution: 
     - Use simpler style settings: `plt.style.use('default')`
     - Or remove style settings entirely
     - Or use built-in styles: `plt.style.use('ggplot')` or `plt.style.use('bmh')`
   - Note: This is a common issue when seaborn is not installed or when using older versions of matplotlib 