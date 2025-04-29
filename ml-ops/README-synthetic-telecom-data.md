# Synthetic Telecom Data Generation

This document describes the synthetic datasets generated for the telecom ML project. The data is generated using the `util-generate-data.py` script and consists of three main datasets that simulate different aspects of a telecommunications network.

## Dataset Overview

### 1. Network Performance Data
Located at: `data/raw/synthetic_data/network_performance_synthetic.csv`

Infrastructure-level metrics capturing network health and performance:
- `timestamp`: 5-minute interval timestamps
- `cell_id`: Unique identifier for cell towers (CELL_001 to CELL_020)
- `latency_ms`: Network latency in milliseconds (10-200ms range)
- `packet_loss`: Packet loss ratio (0-0.2 range)
- `throughput_mbps`: Network throughput in Mbps (1-100 range)
- `signal_strength_dbm`: Signal strength in dBm (-100 to -40 range)
- `connection_type`: Network technology ('4G', '5G', 'LTE')

### 2. Customer Experience Data
Located at: `data/raw/synthetic_data/customer_experience_synthetic.csv`

User-centric metrics and satisfaction data:
- `timestamp`: 5-minute interval timestamps
- `customer_id`: Unique customer identifier (CUST_0001 to CUST_0100)
- `customer_satisfaction_score`: Rating on 1-5 scale
- `data_usage_mb`: Data consumption in MB (0-1000 range)
- `voice_minutes`: Voice call duration in minutes (0-100 range)
- `sms_count`: Number of SMS messages sent (0-50 range)
- `device_type`: Type of device ('Smartphone', 'Tablet', 'IoT')
- `plan_type`: Service plan category ('Basic', 'Standard', 'Premium')

### 3. Call Detail Records (CDR)
Located at: `data/raw/synthetic_data/call_detail_records_synthetic.csv`

Detailed communication event logs:
- `timestamp`: 5-minute interval timestamps
- `caller_id`: Customer identifier making the call (CUST_XXXX format)
- `call_duration_seconds`: Duration of calls (0-3600 seconds)
- `data_used_mb`: Data consumption per call (0-100 MB)
- `call_type`: Type of communication ('Voice', 'Video', 'Data')
- `call_quality_score`: Quality rating on 1-5 scale
- `network_type`: Network technology used ('4G', '5G', 'LTE')
- `location`: Location identifier (LOC_XXX format)
- `roaming`: Boolean indicating if the call was in roaming

## Data Generation Details

- All datasets are generated with 1000 samples each
- Timestamps are synchronized across datasets starting from 2024-01-01
- Data is generated with realistic distributions and constraints:
  - Normal distribution for latency and signal strength
  - Gamma distribution for throughput and call durations
  - Beta distribution for packet loss
  - Poisson distribution for SMS counts
  - Categorical distributions for device types, plan types, and network types

## Usage

To generate fresh synthetic data:

1. Ensure required Python packages are installed (pandas, numpy)
2. Run the generation script:
   ```bash
   python util-generate-data.py
   ```

The script will create or overwrite the CSV files in the specified locations under the `data/raw/synthetic_data/` directory. 