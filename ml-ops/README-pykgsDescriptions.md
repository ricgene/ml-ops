# Essential Python Packages for ML-Ops Project

This document describes the essential Python packages used in this project and their purposes.

## Core ML Packages

### MLflow
- **Purpose**: Machine Learning Lifecycle Management
- **Key Features**:
  - Experiment tracking
  - Model versioning
  - Model deployment
  - Model registry
- **Use Case**: Track experiments, manage model versions, and deploy models in production

### scikit-learn
- **Purpose**: Machine Learning Library
- **Key Features**:
  - Classification algorithms
  - Regression algorithms
  - Clustering algorithms
  - Model evaluation tools
  - Feature selection
- **Use Case**: Implement and evaluate machine learning models for network performance prediction

### pandas
- **Purpose**: Data Manipulation and Analysis
- **Key Features**:
  - Data structures for efficient data manipulation
  - Data cleaning and preprocessing
  - Time series analysis
  - Data aggregation and transformation
- **Use Case**: Process and analyze network performance data, customer experience metrics, and call detail records

## Installation

To install these packages, activate the virtual environment and run:

```bash
pip install mlflow scikit-learn pandas
```

## Additional Recommended Packages

### Data Processing & Analysis
- `numpy`: Numerical computations
- `pydantic`: Data validation
- `great-expectations`: Data quality checks

### Azure Integration
- `azure-storage-blob`: Azure Blob Storage access
- `azure-identity`: Azure authentication

### Testing & Development
- `pytest`: Testing framework
- `black`: Code formatting
- `flake8`: Linting
- `mypy`: Type checking

### Visualization
- `matplotlib`: Basic plotting
- `seaborn`: Statistical visualizations
- `plotly`: Interactive visualizations

### Jupyter Support
- `jupyter`: Notebook support
- `ipykernel`: Jupyter kernel support

## Package Management

All package dependencies should be managed through `requirements.txt`. To update the requirements file after installing new packages:

```bash
pip freeze > requirements.txt
```

## Version Control

It's recommended to pin specific versions of packages in `requirements.txt` to ensure reproducibility. For example:

```
mlflow==2.22.0
scikit-learn==1.6.1
pandas==2.2.3
``` 