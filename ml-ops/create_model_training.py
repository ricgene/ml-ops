import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Model Training Pipeline\n",
                "\n",
                "This notebook implements the model training pipeline for two main tasks:\n",
                "1. Predicting network issues using network performance data\n",
                "2. Predicting customer churn using customer experience data\n",
                "\n",
                "We'll use various baseline models and evaluate their performance."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Setup and Data Loading"
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
                "from sklearn.model_selection import train_test_split, cross_val_score\n",
                "from sklearn.preprocessing import StandardScaler\n",
                "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score\n",
                "from sklearn.linear_model import LogisticRegression\n",
                "from sklearn.ensemble import RandomForestClassifier\n",
                "from sklearn.svm import SVC\n",
                "from xgboost import XGBClassifier\n",
                "\n",
                "# Set display options\n",
                "pd.set_option('display.max_columns', None)\n",
                "pd.set_option('display.max_rows', 100)\n",
                "\n",
                "# Set plot style\n",
                "plt.style.use('seaborn')\n",
                "sns.set_palette('husl')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Load the datasets\n",
                "network_df = pd.read_csv(\"../../data/raw/sample_data/network_performance_sample.csv\")\n",
                "customer_df = pd.read_csv(\"../../data/raw/sample_data/customer_experience_sample.csv\")\n",
                "cdr_df = pd.read_csv(\"../../data/raw/sample_data/call_detail_records_sample.csv\")\n",
                "\n",
                "# Convert timestamps to datetime\n",
                "network_df[\"timestamp\"] = pd.to_datetime(network_df[\"timestamp\"])\n",
                "customer_df[\"timestamp\"] = pd.to_datetime(customer_df[\"timestamp\"])\n",
                "cdr_df[\"timestamp\"] = pd.to_datetime(cdr_df[\"timestamp\"])"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Network Issue Prediction"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Define network issues based on performance metrics\n",
                "def identify_network_issues(df):\n",
                "    df = df.copy()\n",
                "    # Define thresholds for network issues\n",
                "    df['is_issue'] = (\n",
                "        (df['latency_ms'] > 100) |  # High latency\n",
                "        (df['packet_loss'] > 0.05) |  # High packet loss\n",
                "        (df['throughput_mbps'] < 5)  # Low throughput\n",
                "    ).astype(int)\n",
                "    return df\n",
                "\n",
                "# Prepare network data for modeling\n",
                "network_issues_df = identify_network_issues(network_df)\n",
                "\n",
                "# Select features for network issue prediction\n",
                "network_features = ['latency_ms', 'packet_loss', 'throughput_mbps', 'signal_strength_dbm']\n",
                "X_network = network_issues_df[network_features]\n",
                "y_network = network_issues_df['is_issue']\n",
                "\n",
                "# Split the data\n",
                "X_train_net, X_test_net, y_train_net, y_test_net = train_test_split(\n",
                "    X_network, y_network, test_size=0.2, random_state=42\n",
                ")\n",
                "\n",
                "# Scale the features\n",
                "scaler = StandardScaler()\n",
                "X_train_net_scaled = scaler.fit_transform(X_train_net)\n",
                "X_test_net_scaled = scaler.transform(X_test_net)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Train and evaluate network issue prediction models\n",
                "def train_and_evaluate_models(X_train, X_test, y_train, y_test):\n",
                "    models = {\n",
                "        'Logistic Regression': LogisticRegression(),\n",
                "        'Random Forest': RandomForestClassifier(),\n",
                "        'SVM': SVC(probability=True),\n",
                "        'XGBoost': XGBClassifier()\n",
                "    }\n",
                "    \n",
                "    results = {}\n",
                "    for name, model in models.items():\n",
                "        # Train the model\n",
                "        model.fit(X_train, y_train)\n",
                "        \n",
                "        # Make predictions\n",
                "        y_pred = model.predict(X_test)\n",
                "        y_pred_proba = model.predict_proba(X_test)[:, 1]\n",
                "        \n",
                "        # Calculate metrics\n",
                "        results[name] = {\n",
                "            'Accuracy': accuracy_score(y_test, y_pred),\n",
                "            'Precision': precision_score(y_test, y_pred),\n",
                "            'Recall': recall_score(y_test, y_pred),\n",
                "            'F1 Score': f1_score(y_test, y_pred),\n",
                "            'ROC AUC': roc_auc_score(y_test, y_pred_proba)\n",
                "        }\n",
                "    \n",
                "    return pd.DataFrame(results).T\n",
                "\n",
                "# Train and evaluate network issue models\n",
                "network_results = train_and_evaluate_models(\n",
                "    X_train_net_scaled, X_test_net_scaled, y_train_net, y_test_net\n",
                ")\n",
                "print(\"\\nNetwork Issue Prediction Results:\")\n",
                "print(network_results)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Customer Churn Prediction"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Prepare customer data for modeling\n",
                "def prepare_customer_data(customer_df, network_df, cdr_df):\n",
                "    # Merge customer data with network performance\n",
                "    merged_df = pd.merge_asof(\n",
                "        customer_df.sort_values('timestamp'),\n",
                "        network_df.sort_values('timestamp'),\n",
                "        on='timestamp',\n",
                "        direction='nearest'\n",
                "    )\n",
                "    \n",
                "    # Add CDR data\n",
                "    merged_df = pd.merge_asof(\n",
                "        merged_df.sort_values('timestamp'),\n",
                "        cdr_df.sort_values('timestamp'),\n",
                "        on='timestamp',\n",
                "        direction='nearest'\n",
                "    )\n",
                "    \n",
                "    # Define churn based on customer satisfaction and usage patterns\n",
                "    merged_df['is_churn'] = (\n",
                "        (merged_df['customer_satisfaction_score'] < 3) |\n",
                "        (merged_df['data_usage_mb'] < merged_df['data_usage_mb'].mean() * 0.5)\n",
                "    ).astype(int)\n",
                "    \n",
                "    return merged_df\n",
                "\n",
                "# Prepare the data\n",
                "customer_churn_df = prepare_customer_data(customer_df, network_df, cdr_df)\n",
                "\n",
                "# Select features for churn prediction\n",
                "churn_features = [\n",
                "    'customer_satisfaction_score', 'data_usage_mb', 'voice_minutes',\n",
                "    'sms_count', 'latency_ms', 'packet_loss', 'throughput_mbps'\n",
                "]\n",
                "X_churn = customer_churn_df[churn_features]\n",
                "y_churn = customer_churn_df['is_churn']\n",
                "\n",
                "# Split the data\n",
                "X_train_churn, X_test_churn, y_train_churn, y_test_churn = train_test_split(\n",
                "    X_churn, y_churn, test_size=0.2, random_state=42\n",
                ")\n",
                "\n",
                "# Scale the features\n",
                "X_train_churn_scaled = scaler.fit_transform(X_train_churn)\n",
                "X_test_churn_scaled = scaler.transform(X_test_churn)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Train and evaluate churn prediction models\n",
                "churn_results = train_and_evaluate_models(\n",
                "    X_train_churn_scaled, X_test_churn_scaled, y_train_churn, y_test_churn\n",
                ")\n",
                "print(\"\\nCustomer Churn Prediction Results:\")\n",
                "print(churn_results)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Model Comparison and Visualization"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Compare model performance\n",
                "def plot_model_comparison(network_results, churn_results):\n",
                "    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))\n",
                "    \n",
                "    # Plot network issue prediction results\n",
                "    network_results['F1 Score'].plot(kind='bar', ax=ax1)\n",
                "    ax1.set_title('Network Issue Prediction - F1 Scores')\n",
                "    ax1.set_ylabel('F1 Score')\n",
                "    ax1.tick_params(axis='x', rotation=45)\n",
                "    \n",
                "    # Plot churn prediction results\n",
                "    churn_results['F1 Score'].plot(kind='bar', ax=ax2)\n",
                "    ax2.set_title('Customer Churn Prediction - F1 Scores')\n",
                "    ax2.set_ylabel('F1 Score')\n",
                "    ax2.tick_params(axis='x', rotation=45)\n",
                "    \n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "\n",
                "# Plot the results\n",
                "plot_model_comparison(network_results, churn_results)"
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

with open('notebooks/analysis/model_training.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1) 