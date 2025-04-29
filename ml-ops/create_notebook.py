import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Telecom Data Analysis\n",
                "\n",
                "This notebook analyzes network performance, customer experience, and call detail records to identify patterns and insights for improving network performance and customer satisfaction."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Setup and Data Loading\n",
                "\n",
                "### 1.1 Import Libraries"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "import plotly.express as px\n",
                "import plotly.graph_objects as go\n",
                "from datetime import datetime\n",
                "\n",
                "# Set plot style\n",
                "plt.style.use(\"default\")\n",
                "sns.set_palette(\"husl\")\n",
                "\n",
                "# Display settings\n",
                "pd.set_option(\"display.max_columns\", None)\n",
                "pd.set_option(\"display.max_rows\", 100)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 1.2 Load Data"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Load network performance data\n",
                "network_df = pd.read_csv(\"../../data/raw/sample_data/network_performance_sample.csv\")\n",
                "network_df[\"timestamp\"] = pd.to_datetime(network_df[\"timestamp\"])\n",
                "\n",
                "# Load customer experience data\n",
                "customer_df = pd.read_csv(\"../../data/raw/sample_data/customer_experience_sample.csv\")\n",
                "customer_df[\"timestamp\"] = pd.to_datetime(customer_df[\"timestamp\"])\n",
                "\n",
                "# Load call detail records\n",
                "cdr_df = pd.read_csv(\"../../data/raw/sample_data/call_detail_records_sample.csv\")\n",
                "cdr_df[\"timestamp\"] = pd.to_datetime(cdr_df[\"timestamp\"])"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 1.3 Explore Network Performance Data"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Display basic information about the network performance dataset\n",
                "print(\"Network Performance Dataset Info:\")\n",
                "print(\"-\" * 50)\n",
                "print(f\"Number of records: {len(network_df)}\")\n",
                "print(f\"Columns: {', '.join(network_df.columns)}\")\n",
                "print(\"First few records:\")\n",
                "display(network_df.head())\n",
                "\n",
                "print(\"Basic statistics:\")\n",
                "display(network_df.describe())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Data Analysis\n",
                "\n",
                "### 2.1 Network Performance Analysis"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Calculate correlation between network performance metrics\n",
                "network_corr = network_df[['latency_ms', 'packet_loss', 'throughput_mbps', 'signal_strength']].corr()\n",
                "\n",
                "# Plot correlation heatmap\n",
                "plt.figure(figsize=(10, 8))\n",
                "sns.heatmap(network_corr, annot=True, cmap='coolwarm', center=0)\n",
                "plt.title('Correlation between Network Performance Metrics')\n",
                "plt.show()\n",
                "\n",
                "# Analyze signal strength by connection type\n",
                "plt.figure(figsize=(12, 6))\n",
                "sns.boxplot(x='connection_type', y='signal_strength', data=network_df)\n",
                "plt.title('Signal Strength Distribution by Connection Type')\n",
                "plt.xticks(rotation=45)\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 2.2 Customer Experience Analysis"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Analyze customer satisfaction by service type\n",
                "plt.figure(figsize=(10, 6))\n",
                "sns.boxplot(x='service_type', y='customer_satisfaction_score', data=customer_df)\n",
                "plt.title('Customer Satisfaction by Service Type')\n",
                "plt.show()\n",
                "\n",
                "# Plot data usage patterns\n",
                "plt.figure(figsize=(12, 6))\n",
                "sns.histplot(data=customer_df, x='data_usage_mb', hue='service_type', multiple='stack')\n",
                "plt.title('Data Usage Distribution by Service Type')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 2.3 Call Detail Records Analysis"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Analyze call duration patterns\n",
                "plt.figure(figsize=(10, 6))\n",
                "sns.histplot(data=cdr_df, x='call_duration_seconds', hue='call_type', multiple='stack')\n",
                "plt.title('Call Duration Distribution by Call Type')\n",
                "plt.show()\n",
                "\n",
                "# Plot data usage by call type\n",
                "plt.figure(figsize=(10, 6))\n",
                "sns.boxplot(x='call_type', y='data_used_mb', data=cdr_df)\n",
                "plt.title('Data Usage by Call Type')\n",
                "plt.show()"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.11.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('notebooks/analysis/telecom_data_analysis.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1) 