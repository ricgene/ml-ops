import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

def load_data():
    """Load all three datasets."""
    data_dir = 'data/raw/synthetic_data'
    
    network_df = pd.read_csv(os.path.join(data_dir, 'network_performance_synthetic.csv'))
    customer_df = pd.read_csv(os.path.join(data_dir, 'customer_experience_synthetic.csv'))
    cdr_df = pd.read_csv(os.path.join(data_dir, 'call_detail_records_synthetic.csv'))
    
    # Convert timestamps
    for df in [network_df, customer_df, cdr_df]:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return network_df, customer_df, cdr_df

def basic_data_quality(df, name):
    """Perform basic data quality checks."""
    print(f"\n{name} Data Quality Assessment:")
    print("-" * 50)
    
    # Basic info
    print(f"Shape: {df.shape}")
    print("\nMissing Values:")
    print(df.isnull().sum())
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    print(f"\nDuplicate rows: {duplicates}")
    
    # Check value ranges for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print("\nValue Ranges:")
    for col in numeric_cols:
        print(f"{col}: [{df[col].min():.2f}, {df[col].max():.2f}]")
    
    # Check for outliers using z-score
    print("\nOutliers (z-score > 3):")
    for col in numeric_cols:
        z_scores = np.abs(stats.zscore(df[col]))
        outliers = (z_scores > 3).sum()
        print(f"{col}: {outliers} outliers")

def analyze_distributions(df, name):
    """Analyze distributions of numeric columns."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x=col)
        plt.title(f'{name} - {col} Distribution')
        plt.savefig(f'data/analysis/plots/{name}_{col}_distribution.png')
        plt.close()

def analyze_correlations(df, name):
    """Analyze correlations between numeric columns."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numeric_cols].corr()
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title(f'{name} - Correlation Matrix')
    plt.tight_layout()
    plt.savefig(f'data/analysis/plots/{name}_correlation_matrix.png')
    plt.close()

def main():
    # Create analysis directory if it doesn't exist
    os.makedirs('data/analysis/plots', exist_ok=True)
    
    # Load data
    network_df, customer_df, cdr_df = load_data()
    
    # Basic data quality checks
    basic_data_quality(network_df, "Network Performance")
    basic_data_quality(customer_df, "Customer Experience")
    basic_data_quality(cdr_df, "Call Detail Records")
    
    # Analyze distributions
    analyze_distributions(network_df, "network")
    analyze_distributions(customer_df, "customer")
    analyze_distributions(cdr_df, "cdr")
    
    # Analyze correlations
    analyze_correlations(network_df, "network")
    analyze_correlations(customer_df, "customer")
    analyze_correlations(cdr_df, "cdr")
    
    print("\nAnalysis complete! Check data/analysis/plots for visualizations.")

if __name__ == "__main__":
    main() 