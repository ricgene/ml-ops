"""
Data validation module for telecommunications data.

This module provides functions for validating data against schema
and performing data quality checks.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_schema(df: pd.DataFrame, schema: Dict) -> Tuple[bool, List[Dict]]:
    """
    Validate a DataFrame against a schema.
    
    Args:
        df: DataFrame to validate
        schema: Schema dictionary with column names, types, and constraints
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    # Check for required columns
    required_columns = [col for col, props in schema.items() 
                        if props.get("required", False)]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        issues.append({
            "type": "missing_required_columns",
            "columns": missing_columns
        })
    
    # Check data types and constraints for each column
    for column, properties in schema.items():
        # Skip if column is not in DataFrame
        if column not in df.columns:
            if properties.get("required", False):
                # Already reported in missing_columns
                continue
            else:
                issues.append({
                    "type": "missing_optional_column",
                    "column": column
                })
                continue
        
        # Check data type
        expected_type = properties.get("type")
        if expected_type:
            # Map pandas dtypes to more general types
            type_mapping = {
                "numeric": ["int64", "float64", "int32", "float32"],
                "string": ["object", "string"],
                "datetime": ["datetime64", "datetime64[ns]"],
                "boolean": ["bool"],
                "category": ["category"]
            }
            
            actual_dtype = str(df[column].dtype)
            expected_dtypes = type_mapping.get(expected_type, [expected_type])
            
            if actual_dtype not in expected_dtypes:
                issues.append({
                    "type": "wrong_data_type",
                    "column": column,
                    "expected": expected_type,
                    "actual": actual_dtype
                })
        
        # Check range constraints for numeric columns
        if properties.get("type") == "numeric":
            min_value = properties.get("min")
            max_value = properties.get("max")
            
            if min_value is not None and df[column].min() < min_value:
                issues.append({
                    "type": "out_of_range",
                    "column": column,
                    "constraint": f">= {min_value}",
                    "violation": f"min value is {df[column].min()}"
                })
            
            if max_value is not None and df[column].max() > max_value:
                issues.append({
                    "type": "out_of_range",
                    "column": column,
                    "constraint": f"<= {max_value}",
                    "violation": f"max value is {df[column].max()}"
                })
        
        # Check categorical constraints
        if properties.get("type") in ["string", "category"] and "allowed_values" in properties:
            allowed_values = set(properties["allowed_values"])
            actual_values = set(df[column].dropna().unique())
            invalid_values = actual_values - allowed_values
            
            if invalid_values:
                issues.append({
                    "type": "invalid_categorical_values",
                    "column": column,
                    "invalid_values": list(invalid_values)
                })
        
        # Check uniqueness constraint
        if properties.get("unique", False):
            if not df[column].is_unique:
                issues.append({
                    "type": "uniqueness_violation",
                    "column": column
                })
    
    # Determine overall validity
    is_valid = len(issues) == 0
    
    if is_valid:
        logger.info("Schema validation passed")
    else:
        logger.warning(f"Schema validation failed with {len(issues)} issues")
    
    return is_valid, issues


def validate_data_quality(df: pd.DataFrame) -> Dict:
    """
    Validate overall data quality.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Dictionary with data quality metrics
    """
    # Get missing value stats
    missing_values = check_missing_values(df)
    
    # Get duplicate stats
    duplicates = check_duplicates(df)
    
    # Get outlier stats
    outliers = check_outliers(df)
    
    # Overall quality score (simple implementation)
    # Score from 0 to 100, where 100 is perfect quality
    quality_score = 100
    
    # Penalize for missing values
    quality_score -= min(30, missing_values["total_missing_percentage"] * 100)
    
    # Penalize for duplicates
    if duplicates["has_duplicates"]:
        quality_score -= min(20, duplicates["duplicate_percentage"] * 100)
    
    # Penalize for outliers
    if outliers["total_outliers"] > 0:
        quality_score -= min(20, outliers["outlier_percentage"] * 10)
    
    quality_results = {
        "quality_score": quality_score,
        "missing_values": missing_values,
        "duplicates": duplicates,
        "outliers": outliers
    }
    
    logger.info(f"Data quality score: {quality_score:.2f}/100")
    
    return quality_results


def check_missing_values(df: pd.DataFrame) -> Dict:
    """
    Check for missing values in the DataFrame.
    
    Args:
        df: DataFrame to check
        
    Returns:
        Dictionary with missing value statistics
    """
    # Calculate missing values per column
    missing_counts = df.isna().sum()
    missing_percentages = (missing_counts / len(df)) * 100
    
    # Create results dictionary
    missing_columns = {}
    for column in df.columns:
        count = missing_counts[column]
        percentage = missing_percentages[column]
        
        if count > 0:
            missing_columns[column] = {
                "count": int(count),
                "percentage": float(percentage)
            }
    
    # Calculate total missing values
    total_missing = missing_counts.sum()
    total_cells = df.size
    total_missing_percentage = total_missing / total_cells
    
    # Determine if there are critical missing values
    # (arbitrary threshold of 20% for any column)
    critical_threshold = 0.2
    has_critical_missing = any(p > critical_threshold for p in missing_percentages)
    
    results = {
        "total_missing": int(total_missing),
        "total_cells": int(total_cells),
        "total_missing_percentage": float(total_missing_percentage),
        "has_critical_missing": has_critical_missing,
        "missing_columns": missing_columns
    }
    
    logger.info(f"Missing values check: {total_missing}/{total_cells} cells missing ({total_missing_percentage:.2%})")
    
    return results


def check_duplicates(df: pd.DataFrame) -> Dict:
    """
    Check for duplicate rows in the DataFrame.
    
    Args:
        df: DataFrame to check
        
    Returns:
        Dictionary with duplicate statistics
    """
    # Find duplicate rows
    duplicates = df.duplicated()
    duplicate_count = duplicates.sum()
    duplicate_percentage = duplicate_count / len(df)
    
    # Get indexes of duplicate rows
    duplicate_indexes = df.index[duplicates].tolist()
    
    results = {
        "has_duplicates": duplicate_count > 0,
        "duplicate_count": int(duplicate_count),
        "duplicate_percentage": float(duplicate_percentage),
        "duplicate_indexes": duplicate_indexes
    }
    
    logger.info(f"Duplicate check: {duplicate_count} duplicate rows ({duplicate_percentage:.2%})")
    
    return results


def check_outliers(df: pd.DataFrame) -> Dict:
    """
    Check for outliers in numeric columns using IQR method.
    
    Args:
        df: DataFrame to check
        
    Returns:
        Dictionary with outlier statistics
    """
    outlier_columns = {}
    total_outliers = 0
    
    # Only check numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns
    
    for column in numeric_columns:
        # Calculate IQR
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        
        # Define outlier bounds
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        # Find outliers
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        outlier_count = len(outliers)
        
        if outlier_count > 0:
            outlier_percentage = outlier_count / len(df)
            outlier_indexes = outliers.index.tolist()
            
            outlier_columns[column] = {
                "count": outlier_count,
                "percentage": float(outlier_percentage),
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound),
                "min_value": float(df[column].min()),
                "max_value": float(df[column].max())
            }
            
            total_outliers += outlier_count
    
    # Calculate overall percentage
    outlier_percentage = total_outliers / (len(df) * len(numeric_columns)) if len(numeric_columns) > 0 else 0
    
    results = {
        "total_outliers": total_outliers,
        "outlier_percentage": float(outlier_percentage),
        "outlier_columns": outlier_columns
    }
    
    logger.info(f"Outlier check: {total_outliers} outliers detected across {len(outlier_columns)} columns")
    
    return results