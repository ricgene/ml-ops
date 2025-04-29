import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_network_performance_data(n_samples=1000):
    """Generate synthetic network performance data."""
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate timestamps
    start_time = datetime(2024, 1, 1)
    timestamps = [start_time + timedelta(minutes=i*5) for i in range(n_samples)]
    
    # Generate cell IDs
    cell_ids = [f'CELL_{i:03d}' for i in range(1, 21)]  # 20 cells
    cell_ids = np.random.choice(cell_ids, n_samples)
    
    # Generate network metrics
    data = {
        'timestamp': timestamps,
        'cell_id': cell_ids,
        'latency_ms': np.random.normal(50, 20, n_samples),  # Mean 50ms, std 20ms
        'packet_loss': np.random.beta(2, 10, n_samples),    # Skewed towards 0
        'throughput_mbps': np.random.gamma(2, 5, n_samples), # Skewed towards higher values
        'signal_strength_dbm': np.random.normal(-70, 10, n_samples),  # Mean -70dBm
        'connection_type': np.random.choice(['4G', '5G', 'LTE'], n_samples, p=[0.3, 0.4, 0.3])
    }
    
    # Ensure values are within realistic ranges
    data['latency_ms'] = np.clip(data['latency_ms'], 10, 200)
    data['packet_loss'] = np.clip(data['packet_loss'], 0, 0.2)
    data['throughput_mbps'] = np.clip(data['throughput_mbps'], 1, 100)
    data['signal_strength_dbm'] = np.clip(data['signal_strength_dbm'], -100, -40)
    
    return pd.DataFrame(data)

def generate_customer_experience_data(n_samples=1000):
    """Generate synthetic customer experience data."""
    np.random.seed(42)
    
    # Generate timestamps
    start_time = datetime(2024, 1, 1)
    timestamps = [start_time + timedelta(minutes=i*5) for i in range(n_samples)]
    
    # Generate customer IDs
    customer_ids = [f'CUST_{i:04d}' for i in range(1, 101)]  # 100 customers
    customer_ids = np.random.choice(customer_ids, n_samples)
    
    # Generate customer metrics
    data = {
        'timestamp': timestamps,
        'customer_id': customer_ids,
        'customer_satisfaction_score': np.random.normal(3.5, 1, n_samples),  # 1-5 scale
        'data_usage_mb': np.random.gamma(2, 100, n_samples),  # Skewed towards higher values
        'voice_minutes': np.random.gamma(1.5, 10, n_samples),
        'sms_count': np.random.poisson(5, n_samples),
        'device_type': np.random.choice(['Smartphone', 'Tablet', 'IoT'], n_samples, p=[0.7, 0.2, 0.1]),
        'plan_type': np.random.choice(['Basic', 'Standard', 'Premium'], n_samples, p=[0.3, 0.5, 0.2])
    }
    
    # Ensure values are within realistic ranges
    data['customer_satisfaction_score'] = np.clip(data['customer_satisfaction_score'], 1, 5)
    data['data_usage_mb'] = np.clip(data['data_usage_mb'], 0, 1000)
    data['voice_minutes'] = np.clip(data['voice_minutes'], 0, 100)
    data['sms_count'] = np.clip(data['sms_count'], 0, 50)
    
    return pd.DataFrame(data)

def generate_call_detail_records(n_samples=1000):
    """Generate synthetic call detail records."""
    np.random.seed(42)
    
    # Generate timestamps
    start_time = datetime(2024, 1, 1)
    timestamps = [start_time + timedelta(minutes=i*5) for i in range(n_samples)]
    
    # Generate caller IDs
    caller_ids = [f'CUST_{i:04d}' for i in range(1, 101)]  # 100 customers
    caller_ids = np.random.choice(caller_ids, n_samples)
    
    # Generate call records
    data = {
        'timestamp': timestamps,
        'caller_id': caller_ids,
        'call_duration_seconds': np.random.gamma(2, 30, n_samples),  # Skewed towards longer calls
        'data_used_mb': np.random.gamma(1.5, 10, n_samples),
        'call_type': np.random.choice(['Voice', 'Video', 'Data'], n_samples, p=[0.4, 0.3, 0.3]),
        'call_quality_score': np.random.normal(4, 0.5, n_samples),  # 1-5 scale
        'network_type': np.random.choice(['4G', '5G', 'LTE'], n_samples, p=[0.3, 0.4, 0.3]),
        'location': [f'LOC_{i:03d}' for i in np.random.randint(1, 50, n_samples)],
        'roaming': np.random.choice([True, False], n_samples, p=[0.1, 0.9])
    }
    
    # Ensure values are within realistic ranges
    data['call_duration_seconds'] = np.clip(data['call_duration_seconds'], 0, 3600)
    data['data_used_mb'] = np.clip(data['data_used_mb'], 0, 100)
    data['call_quality_score'] = np.clip(data['call_quality_score'], 1, 5)
    
    return pd.DataFrame(data)

def main():
    # Generate synthetic data
    network_df = generate_network_performance_data(1000)
    customer_df = generate_customer_experience_data(1000)
    cdr_df = generate_call_detail_records(1000)
    
    # Save to CSV files
    network_df.to_csv('data/raw/synthetic_data/network_performance_synthetic.csv', index=False)
    customer_df.to_csv('data/raw/synthetic_data/customer_experience_synthetic.csv', index=False)
    cdr_df.to_csv('data/raw/synthetic_data/call_detail_records_synthetic.csv', index=False)
    
    print("Synthetic data generated successfully!")
    print(f"Network Performance Data: {network_df.shape}")
    print(f"Customer Experience Data: {customer_df.shape}")
    print(f"Call Detail Records: {cdr_df.shape}")

if __name__ == "__main__":
    main() 