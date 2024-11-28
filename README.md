# Real-Time Fraud Detection System
This project is a real-time fraud detection system that ingests transaction data, applies a machine learning model for fraud prediction, and provides actionable results for storage and further analysis. It leverages Apache Kafka for data streaming, Random Forest/XGBoost for fraud detection, and MySQL for result storage.

# Overview
The system consists of three key scripts:

train.py: Fetches transaction data from a MySQL database and publishes it to a Kafka topic.
transaction_producer.py: Trains a fraud detection model using historical transaction data and saves the trained model for scoring.
transaction_consumer.py: Consumes real-time transaction data from Kafka, uses the trained model to predict fraud, and outputs predictions for further use.
# Full Dataset
The full `transactions.csv` dataset is too large to include in this repository. You can download it from here(https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)).

Files and Descriptions
1. train.py
This script acts as the Kafka Producer that fetches historical transaction data from MySQL and publishes it to a Kafka topic for real-time processing.

# Key Features:
Connects to a MySQL database using SQLAlchemy.
Fetches transaction data from the ccfd.tx_test table.
Publishes each row as a JSON message to the Kafka topic ccfd_7.
Usage:
Update the database configuration (db_config) and Kafka broker (bootstrap_servers) in the script.
Run the script:
bash
Copy code
python train.py
Verify that the data is being published to Kafka by using Kafka tools:
bash
Copy code
bin/kafka-console-consumer.sh --topic ccfd_7 --from-beginning --bootstrap-server localhost:9092
2. transaction_producer.py
This script trains a machine learning model for fraud detection using historical data and saves the model for real-time scoring.

# Key Features:
Prepares data for training by:
Encoding categorical variables like location.
Extracting features from timestamps (e.g., hour_of_day).
Trains a Random Forest Classifier for fraud detection.
Evaluates the model and saves it as payment_scoring_model.pkl.
Usage:
Place your dataset (transactions.csv) in the same directory as the script.
Run the script:
bash
Copy code
python transaction_producer.py
The script will:
Train the model using the dataset.
Display a classification report showing model performance.
Save the trained model as payment_scoring_model.pkl.
3. transaction_consumer.py
This script acts as the Kafka Consumer that reads real-time transaction data from a Kafka topic, applies the trained fraud detection model, and outputs predictions.

# Key Features:
Connects to the Kafka topic ccfd_11 and consumes messages in real time.
Uses a pre-trained XGBoost model (xgboost_model.pkl) for fraud detection.
Preprocesses data on-the-fly to match the model's requirements.
Outputs predictions for fraud likelihood.
Usage:
Ensure the Kafka topic ccfd_11 contains transaction messages.
Load the trained model (xgboost_model.pkl) into the same directory.
Run the script:
python transaction_consumer.py
The script will:
Listen to the Kafka topic and process incoming messages.
Print fraud predictions for each transaction.
# Task Workflow
Data Ingestion:
Use train.py to fetch data from the MySQL database and publish it to the Kafka topic ccfd_7.
Model Training:
Use transaction_producer.py to train a fraud detection model using historical transaction data.
Save the trained model (payment_scoring_model.pkl) for use in real-time scoring.
Real-Time Processing:
Use transaction_consumer.py to consume real-time transaction data from Kafka (ccfd_11).
Apply the trained model to classify transactions as fraudulent or non-fraudulent.
Output predictions for further storage or action.
Setup Instructions
# Prerequisites
Install Python 3.8+.
Install the required Python libraries:
pip install pandas scikit-learn joblib kafka-python sqlalchemy pymysql xgboost
# Setting Up Kafka
Install and start Kafka on your machine:
Start Zookeeper:
bin/zookeeper-server-start.sh config/zookeeper.properties
Start Kafka broker:
bin/kafka-server-start.sh config/server.properties
Create the Kafka topics ccfd_7 and ccfd_11:
bin/kafka-topics.sh --create --topic ccfd_7 --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
bin/kafka-topics.sh --create --topic ccfd_11 --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
# Setting Up MySQL
Create a MySQL database and table:
sql
Copy code
CREATE DATABASE ccfd;
USE ccfd;

CREATE TABLE tx_test (
    time DATETIME,
    pca_1 FLOAT, pca_2 FLOAT, ..., pca_28 FLOAT,
    amount FLOAT
);
# Directory Structure
project/
├── train.py                   # Kafka producer fetching data from MySQL
├── transaction_producer.py    # Model training script
├── transaction_consumer.py    # Kafka consumer for real-time scoring
├── transactionn.csv           # Sample transaction dataset
├── README.md                  # Documentation

# Future Enhancements
Integrate a database for storing real-time predictions (e.g., MySQL).
Add a dashboard for visualizing real-time fraud detection metrics.
Experiment with more advanced machine learning models for higher accuracy.
Optimize the Kafka pipeline for large-scale deployments.
# License
This project is licensed under the MIT License. See LICENSE for details.

