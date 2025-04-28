# Sample Data for Telecom ML Project

This directory contains sample datasets that represent the structure and format of data that would be stored in Azure Blob Storage. These samples are used for development, testing, and documentation purposes.

## Dataset Descriptions

### 1. Network Performance Data (`network_performance_sample.csv`)
- Contains key network performance metrics
- Fields:
  - `timestamp`: Time of measurement
  - `cell_id`: Unique identifier for network cell
  - `latency_ms`: Network latency in milliseconds
  - `packet_loss`: Packet loss rate
  - `throughput_mbps`: Network throughput in Mbps
  - `signal_strength`: Signal strength in dBm
  - `connection_type`: Network type (5G, LTE, etc.)

### 2. Customer Experience Data (`customer_experience_sample.csv`)
- Contains customer usage and satisfaction metrics
- Fields:
  - `customer_id`: Unique customer identifier
  - `timestamp`: Time of measurement
  - `service_type`: Type of service (mobile, business)
  - `data_usage_mb`: Data usage in MB
  - `voice_minutes`: Voice call duration
  - `sms_count`: Number of SMS messages
  - `network_quality_score`: Network quality rating
  - `customer_satisfaction_score`: Customer satisfaction rating

### 3. Call Detail Records (`call_detail_records_sample.csv`)
- Contains detailed call and data usage records
- Fields:
  - `call_id`: Unique call identifier
  - `timestamp`: Time of call/data usage
  - `caller_id`: ID of the calling customer
  - `callee_id`: ID of the called customer
  - `call_duration_seconds`: Duration of call
  - `call_type`: Type of call (voice/data)
  - `cell_id`: Network cell identifier
  - `roaming_status`: Roaming status
  - `data_used_mb`: Data usage in MB

## Azure Blob Storage Integration

In production, these datasets would be stored in Azure Blob Storage with the following structure:

```
container/
├── network_performance/
│   ├── year=2024/
│   │   ├── month=03/
│   │   │   └── day=20/
│   │   │       └── network_performance_*.csv
├── customer_experience/
│   ├── year=2024/
│   │   ├── month=03/
│   │   │   └── day=20/
│   │   │       └── customer_experience_*.csv
└── call_detail_records/
    ├── year=2024/
    │   ├── month=03/
    │   │   └── day=20/
    │   │       └── cdr_*.csv
```

## Usage Notes

1. These sample datasets are small and simplified versions of the actual data
2. They maintain the same schema and data types as the production data
3. They can be used for:
   - Development and testing of data processing pipelines
   - Documentation of expected data formats
   - CI/CD pipeline testing
   - Team onboarding and training

## Data Access

In production, data access will be configured through environment variables:
- `AZURE_STORAGE_CONNECTION_STRING`
- `AZURE_STORAGE_CONTAINER_NAME`
- `AZURE_STORAGE_ACCOUNT_NAME`
- `AZURE_STORAGE_ACCOUNT_KEY` 