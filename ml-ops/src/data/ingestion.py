"""
Data ingestion module for telecommunications data.

This module handles data loading, validation, and preprocessing
for the telecommunications MLOps project.
"""

import os
import logging
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime

# Import validation functions
from .validation import (
    validate_schema,
    validate_data_quality,
    check_missing_values,
    check_duplicates,
    check_outliers
)
from .schema import TELECOM_DATA_SCHEMA

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataIngestion:
    """
    Data ingestion class for telecommunications data.
    
    This class handles loading data from various sources,
    validating the data against a schema, and performing
    data quality checks.
    """
    
    def __init__(
        self,
        data_dir: str = "data",
        raw_dir: str = "raw",
        processed_dir: str = "processed",
        schema: Dict = TELECOM_DATA_SCHEMA
    ):
        """
        Initialize the DataIngestion class.
        
        Args:
            data_dir: Base directory for data
            raw_dir: Directory for raw data
            processed_dir: Directory for processed data
            schema: Data schema for validation
        """
        self.data_dir = data_dir
        self.raw_dir = os.path.join(data_dir, raw_dir)
        self.processed_dir = os.path.join(data_dir, processed_dir)
        self.schema = schema
        
        # Create directories if they don't exist
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        
        logger.info(f"Initialized DataIngestion with data directory: {data_dir}")
    
    def load_csv(
        self, 
        file_path: str, 
        validate: bool = True,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load data from a CSV file with validation.
        
        Args:
            file_path: Path to the CSV file
            validate: Whether to validate the data
            **kwargs: Additional arguments to pass to pd.read_csv
            
        Returns:
            Pandas DataFrame with the loaded data
        """
        logger.info(f"Loading data from {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            # Load the data
            df = pd.read_csv(file_path, **kwargs)
            logger.info(f"Successfully loaded data with shape {df.shape}")
            
            # Validate the data if requested
            if validate:
                self.validate_data(df)
            
            return df
        
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {str(e)}")
            raise
    
    def load_from_database(
        self,
        connection_string: str,
        query: str,
        validate: bool = True,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load data from a database with validation.
        
        Args:
            connection_string: Database connection string
            query: SQL query to execute
            validate: Whether to validate the data
            **kwargs: Additional arguments to pass to pd.read_sql
            
        Returns:
            Pandas DataFrame with the loaded data
        """
        logger.info(f"Loading data from database with query: {query}")
        
        try:
            import sqlalchemy
            engine = sqlalchemy.create_engine(connection_string)
            
            # Load the data
            df = pd.read_sql(query, engine, **kwargs)
            logger.info(f"Successfully loaded data with shape {df.shape}")
            
            # Validate the data if requested
            if validate:
                self.validate_data(df)
            
            return df
        
        except ImportError:
            logger.error("sqlalchemy not installed, cannot load from database")
            raise
        except Exception as e:
            logger.error(f"Error loading data from database: {str(e)}")
            raise
    
    def validate_data(self, df: pd.DataFrame) -> Tuple[bool, Dict]:
        """
        Validate data against schema and perform quality checks.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Tuple of (is_valid, validation_results)
        """
        logger.info("Validating data")
        
        validation_results = {
            "schema_validation": None,
            "missing_values": None,
            "duplicates": None,
            "outliers": None
        }
        
        # Validate schema
        schema_valid, schema_issues = validate_schema(df, self.schema)
        validation_results["schema_validation"] = {
            "valid": schema_valid,
            "issues": schema_issues
        }
        
        # Check for missing values
        missing_check = check_missing_values(df)
        validation_results["missing_values"] = missing_check
        
        # Check for duplicates
        duplicate_check = check_duplicates(df)
        validation_results["duplicates"] = duplicate_check
        
        # Check for outliers
        outlier_check = check_outliers(df)
        validation_results["outliers"] = outlier_check
        
        # Check overall validity
        is_valid = (
            schema_valid and
            not missing_check["has_critical_missing"] and
            not duplicate_check["has_duplicates"]
        )
        
        if is_valid:
            logger.info("Data validation passed")
        else:
            logger.warning("Data validation failed")
            logger.warning(f"Validation results: {validation_results}")
        
        return is_valid, validation_results
    
    def preprocess_data(
        self, 
        df: pd.DataFrame, 
        drop_duplicates: bool = True,
        handle_missing: bool = True,
        handle_outliers: bool = False
    ) -> pd.DataFrame:
        """
        Preprocess data based on validation results.
        
        Args:
            df: DataFrame to preprocess
            drop_duplicates: Whether to drop duplicate rows
            handle_missing: Whether to handle missing values
            handle_outliers: Whether to handle outliers
            
        Returns:
            Preprocessed DataFrame
        """
        logger.info("Preprocessing data")
        
        processed_df = df.copy()
        
        # Drop duplicates if requested
        if drop_duplicates:
            initial_rows = len(processed_df)
            processed_df = processed_df.drop_duplicates()
            dropped_rows = initial_rows - len(processed_df)
            logger.info(f"Dropped {dropped_rows} duplicate rows")
        
        # Handle missing values if requested
        if handle_missing:
            # For numeric columns, fill with median
            numeric_cols = processed_df.select_dtypes(include=['number']).columns
            for col in numeric_cols:
                if processed_df[col].isna().sum() > 0:
                    median_value = processed_df[col].median()
                    processed_df[col] = processed_df[col].fillna(median_value)
                    logger.info(f"Filled missing values in {col} with median: {median_value}")
            
            # For categorical columns, fill with mode
            cat_cols = processed_df.select_dtypes(include=['object', 'category']).columns
            for col in cat_cols:
                if processed_df[col].isna().sum() > 0:
                    mode_value = processed_df[col].mode()[0]
                    processed_df[col] = processed_df[col].fillna(mode_value)
                    logger.info(f"Filled missing values in {col} with mode: {mode_value}")
        
        # Handle outliers if requested
        if handle_outliers:
            numeric_cols = processed_df.select_dtypes(include=['number']).columns
            for col in numeric_cols:
                q1 = processed_df[col].quantile(0.25)
                q3 = processed_df[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                # Cap outliers to the bounds
                processed_df[col] = processed_df[col].clip(lower_bound, upper_bound)
                logger.info(f"Capped outliers in {col} to range [{lower_bound}, {upper_bound}]")
        
        logger.info(f"Preprocessing complete, final shape: {processed_df.shape}")
        return processed_df
    
    def save_processed_data(
        self, 
        df: pd.DataFrame, 
        file_name: str = None
    ) -> str:
        """
        Save processed data to processed directory.
        
        Args:
            df: DataFrame to save
            file_name: Name of the file to save
            
        Returns:
            Path to the saved file
        """
        if file_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"processed_data_{timestamp}.csv"
        
        file_path = os.path.join(self.processed_dir, file_name)
        
        # Save the data
        df.to_csv(file_path, index=False)
        logger.info(f"Saved processed data to {file_path}")
        
        return file_path
    
    def run_ingestion_pipeline(
        self,
        source_path: str,
        source_type: str = "csv",
        output_file: str = None,
        **kwargs
    ) -> Tuple[pd.DataFrame, str]:
        """
        Run the complete ingestion pipeline.
        
        Args:
            source_path: Path to the data source
            source_type: Type of the data source ('csv' or 'database')
            output_file: Name of the output file
            **kwargs: Additional arguments for data loading
            
        Returns:
            Tuple of (processed_dataframe, output_file_path)
        """
        logger.info(f"Running ingestion pipeline for {source_type} data from {source_path}")
        
        # Load data based on source type
        if source_type.lower() == "csv":
            df = self.load_csv(source_path, **kwargs)
        elif source_type.lower() == "database":
            if "query" not in kwargs:
                raise ValueError("Database source requires a 'query' parameter")
            df = self.load_from_database(source_path, kwargs.pop("query"), **kwargs)
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
        
        # Preprocess the data
        processed_df = self.preprocess_data(df)
        
        # Save the processed data
        output_path = self.save_processed_data(processed_df, output_file)
        
        return processed_df, output_path


def main():
    """Example usage of the DataIngestion class."""
    # Create an instance of DataIngestion
    ingestion = DataIngestion()
    
    # Example: Run the ingestion pipeline on a CSV file
    try:
        df, output_path = ingestion.run_ingestion_pipeline(
            source_path="data/raw/telecom_data.csv",
            source_type="csv",
            output_file="clean_telecom_data.csv"
        )
        print(f"Ingestion completed successfully. Output: {output_path}")
    except Exception as e:
        print(f"Ingestion failed: {str(e)}")


if __name__ == "__main__":
    main()