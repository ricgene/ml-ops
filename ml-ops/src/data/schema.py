"""
Data schema definitions for telecommunications data.

This module defines the expected schema for telecommunications
data, including column types, constraints, and validation rules.
"""

# Schema definition for telecommunications data
# Format:
# {
#     "column_name": {
#         "type": "numeric|string|datetime|boolean|category",
#         "required": True|False,
#         "min": minimum_value,  # for numeric columns
#         "max": maximum_value,  # for numeric columns
#         "allowed_values": [],  # for categorical columns
#         "unique": True|False,  # for unique columns
#         "description": "Column description"
#     }
# }

TELECOM_DATA_SCHEMA = {
    # Customer demographic information
    "customer_id": {
        "type": "string",
        "required": True,
        "unique": True,
        "description": "Unique identifier for the customer"
    },
    "age": {
        "type": "numeric",
        "required": True,
        "min": 18,
        "max": 120,
        "description": "Customer age in years"
    },
    "gender": {
        "type": "category",
        "required": False,
        "allowed_values": ["Male", "Female", "Other", "Prefer not to say"],
        "description": "Customer gender"
    },
    "location": {
        "type": "string",
        "required": True,
        "description": "Customer location (city or region)"
    },
    
    # Service information
    "service_plan": {
        "type": "category",
        "required": True,
        "allowed_values": ["Basic", "Standard", "Premium", "Enterprise"],
        "description": "Customer's service plan"
    },
    "contract_type": {
        "type": "category",
        "required": True,
        "allowed_values": ["Month-to-Month", "One Year", "Two Year"],
        "description": "Type of contract"
    },
    "tenure_months": {
        "type": "numeric",
        "required": True,
        "min": 0,
        "description": "Number of months the customer has been with the provider"
    },
    "monthly_charges": {
        "type": "numeric",
        "required": True,
        "min": 0,
        "description": "Monthly charges in currency units"
    },
    "total_charges": {
        "type": "numeric",
        "required": True,
        "min": 0,
        "description": "Total charges to date in currency units"
    },
    
    # Network usage metrics
    "data_usage_gb": {
        "type": "numeric",
        "required": True,
        "min": 0,
        "description": "Monthly data usage in gigabytes"
    },
    "voice_minutes": {
        "type": "numeric",
        "required": True,
        "min": 0,
        "description": "Monthly voice usage in minutes"
    },
    "sms_count": {
        "type": "numeric",
        "required": True,
        "min": 0,
        "description": "Monthly SMS count"
    },
    "international_calls_minutes": {
        "type": "numeric",
        "required": False,
        "min": 0,
        "description": "Monthly international calls in minutes"
    },
    
    # Network performance metrics
    "download_speed_mbps": {
        "type": "numeric",
        "required": False,
        "min": 0,
        "description": "Average download speed in Mbps"
    },
    "upload_speed_mbps": {
        "type": "numeric",
        "required": False,
        "min": 0,
        "description": "Average upload speed in Mbps"
    },
    "latency_ms": {
        "type": "numeric",
        "required": False,
        "min": 0,
        "description": "Average network latency in milliseconds"
    },
    "packet_loss_percent": {
        "type": "numeric",
        "required": False,
        "min": 0,
        "max": 100,
        "description": "Average packet loss percentage"
    },
    "network_availability_percent": {
        "type": "numeric",
        "required": False,
        "min": 0,
        "max": 100,
        "description": "Network availability percentage"
    },
    
    # Call quality metrics
    "call_drop_count": {
        "type": "numeric",
        "required": False,
        "min": 0,
        "description": "Number of dropped calls"
    },
    "call_setup_success_percent": {
        "type": "numeric",
        "required": False,
        "min": 0,
        "max": 100,
        "description": "Call setup success rate percentage"
    },
    "voice_quality_score": {
        "type": "numeric",
        "required": False,
        "min": 1,
        "max": 10,
        "description": "Voice quality score (1-10)"
    },
    
    # Customer service interactions
    "support_calls_count": {
        "type": "numeric",
        "required": False,
        "min": 0,
        "description": "Number of customer support calls"
    },
    "support_tickets_count": {
        "type": "numeric",
        "required": False,
        "min": 0,
        "description": "Number of support tickets raised"
    },
    "avg_resolution_time_hours": {
        "type": "numeric",
        "required": False,
        "min": 0,
        "description": "Average resolution time for support tickets in hours"
    },
    
    # Target variables
    "churn": {
        "type": "boolean",
        "required": False,
        "description": "Whether the customer churned (target variable for churn prediction)"
    },
    "customer_satisfaction_score": {
        "type": "numeric",
        "required": False,
        "min": 1,
        "max": 10,
        "description": "Customer satisfaction score (1-10)"
    }
}

# Define critical columns that must not have missing values
CRITICAL_COLUMNS = [
    "customer_id",
    "service_plan",
    "contract_type",
    "tenure_months",
    "monthly_charges",
    "data_usage_gb"
]

# Define expected data types for easier validation
EXPECTED_TYPES = {
    "numeric": ["int64", "float64", "int32", "float32"],
    "string": ["object", "string"],
    "datetime": ["datetime64", "datetime64[ns]"],
    "boolean": ["bool"],
    "category": ["category", "object"]
}

# Schema for a simplified version of the data (subset of columns)
SIMPLIFIED_TELECOM_SCHEMA = {
    key: TELECOM_DATA_SCHEMA[key] 
    for key in [
        "customer_id", "age", "gender", "location",
        "service_plan", "contract_type", "tenure_months",
        "monthly_charges", "data_usage_gb", "voice_minutes",
        "sms_count", "churn"
    ]
}