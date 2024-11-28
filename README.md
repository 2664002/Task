# Real-Time Payment Scoring System
This project implements a real-time payment scoring system that detects potentially fraudulent transactions. It leverages Apache Kafka for real-time data ingestion, a pre-trained machine learning model for transaction scoring, and MySQL for storing results.
# Features
Real-Time Data Ingestion:
Reads payment transactions from an Apache Kafka topic (payment_transactions).
Fraud Detection Model:
A pre-trained machine learning model (Random Forest) is used to score transactions based on features such as amount, transaction time, and location.
Database Integration:
Scoring results are stored in a MySQL database for further analysis and reporting.
Scalable and Robust:
Designed to handle high-throughput real-time transaction streams.
# Components
Kafka Producer:
Simulates or ingests live transaction data into the Kafka topic.
Kafka Consumer:
Reads the transaction data from Kafka, preprocesses it, and uses the machine learning model to predict fraud.
Machine Learning Model:
A Random Forest model trained on historical transaction data to detect patterns indicative of fraud.
MySQL Database:
Stores the results of the fraud detection model for reporting and monitoring.
# Setup Instructions
Install the following:
Python 3.8+
Apache Kafka
MySQL Server
Required Python libraries (listed in requirements.txt)
