# to do
  - create the venv
  - 

# Data Directory Structure

This directory contains the data used in the ML-ops project. The structure is organized as follows:

## Directory Structure

- `raw/`: Original, immutable data
  - `sample_data/`: Small sample datasets for development and testing
- `processed/`: Cleaned, transformed data
  - `sample_data/`: Processed sample datasets
- `features/`: Feature sets for training
  - `sample_data/`: Sample feature sets

## Sample Data

The `sample_data` directories contain small, representative datasets that can be used for:
- Development and testing
- Documentation of expected data formats
- CI/CD pipeline testing
- Team onboarding

These sample datasets should be:
- Small enough to be version controlled
- Representative of the actual data structure
- Free of sensitive information
- Documented with their schema and expected format

## Data Management

- Actual data files (outside of `sample_data`) are ignored by git
- Data should be stored in a cloud storage solution (e.g., S3, GCS)
- Data access should be configured through environment variables
- Data processing pipelines should be documented in the project documentation 