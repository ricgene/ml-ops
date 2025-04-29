# Model Training Pipeline

This component implements the model training pipeline for two main tasks:
1. Predicting network issues using network performance data
2. Predicting customer churn using customer experience data

## Overview

The model training pipeline uses various baseline models and evaluates their performance using multiple metrics. The implementation is contained in the `model_training.ipynb` notebook.

## Features

### Network Issue Prediction
- Uses network performance metrics to predict issues
- Implements multiple baseline models:
  - Logistic Regression
  - Random Forest
  - SVM
  - XGBoost
- Evaluates models using various metrics:
  - Accuracy
  - Precision
  - Recall
  - F1 Score
  - ROC AUC

### Customer Churn Prediction
- Combines customer experience data with network performance
- Uses the same set of baseline models
- Includes visualization of model performance
- Features used for prediction:
  - Customer satisfaction score
  - Data usage
  - Voice minutes
  - SMS count
  - Network performance metrics

## Implementation Details

### Network Issue Definition
Network issues are defined based on the following thresholds:
- High latency (> 100ms)
- High packet loss (> 5%)
- Low throughput (< 5 Mbps)

### Customer Churn Definition
Customer churn is defined based on:
- Low customer satisfaction score (< 3)
- Significant drop in data usage (< 50% of mean)

### Model Training Process
1. Data preprocessing and feature engineering
2. Train-test split (80-20)
3. Feature scaling using StandardScaler
4. Model training and evaluation
5. Performance comparison and visualization

## Usage

1. Ensure you have all required dependencies installed in your virtual environment
2. Open the `model_training.ipynb` notebook
3. Run the cells in sequence to:
   - Load and preprocess the data
   - Train the models
   - Evaluate performance
   - Visualize results

## Dependencies

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- xgboost

## Next Steps

- Hyperparameter tuning for better performance
- Feature importance analysis
- Model deployment pipeline
- Real-time prediction implementation 