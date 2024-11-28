#!/bin/python3

import pandas as pd
from kafka import KafkaProducer
import sqlalchemy as sqa
import json

# Kafka Producer Configuration
topic_name = 'ccfd_7'
bootstrap_servers = ['192.168.1.130:9092']

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print(f"Connected to Kafka topic: {topic_name}")

# MySQL Database Configuration
db_config = "mysql+pymysql://ccfd:ccfd@192.168.1.130:3306/ccfd"

# Create a SQLAlchemy engine
engine = sqa.create_engine(db_config)

# SQL query to fetch the data
query = """
SELECT 
    time, 
    pca_1, pca_2, pca_3, pca_4, pca_5, 
    pca_6, pca_7, pca_8, pca_9, pca_10, 
    pca_11, pca_12, pca_13, pca_14, pca_15, 
    pca_16, pca_17, pca_18, pca_19, pca_20, 
    pca_21, pca_22, pca_23, pca_24, pca_25, 
    pca_26, pca_27, pca_28, amount
FROM ccfd.tx_test
"""

# Load the data into a Pandas DataFrame
try:
    # Fetch data from MySQL and load into a DataFrame
    df = pd.read_sql(query, engine)
    print(f"Fetched {len(df)} rows from the database.")
    
    # Publish each row to Kafka
    for _, row in df.iterrows():
        # Convert the row to a dictionary and send to Kafka
        producer.send(topic_name, value=row.to_dict())
        print(f"Published row: {row.to_dict()}")
    
    producer.flush()  # Ensure all messages are sent
    print("All messages published successfully.")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the producer
    producer.close()