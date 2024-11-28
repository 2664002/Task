#!/bin/python3

from kafka import KafkaProducer
import pymysql
import json

# Kafka Producer Configuration
topic_name = 'ccfd_11'
bootstrap_servers = ['192.168.1.130:9092']

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print(f"Connected to Kafka topic: {topic_name}")

# MySQL Database Configuration
db_config = {
    'host': '192.168.1.130',
    'user': 'ccfd',
    'password': 'ccfd',
    'database': 'ccfd'
}

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

# Fetch data from MySQL and publish to Kafka
try:
    # Connect to MySQL
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    # Execute query
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print(f"Fetched {len(rows)} rows from the database.")
    
    # Publish each row to Kafka
    for row in rows:
        producer.send(topic_name, value=row)
        print(f"Published row: {row}")
    
    producer.flush()  # Ensure all messages are sent
    print("All messages published successfully.")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()