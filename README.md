# Fetch-DE-Take-Home

## Overview
This project sets up a **real-time data processing pipeline** using **Apache Kafka** and **Apache Spark Streaming**. The pipeline consumes streaming user login data, processes it using **PySpark**, and publishes the transformed data to another Kafka topic.

## Prerequisites
Ensure you have the following installed before running the project:
- **Docker & Docker Compose** (for running Kafka & Zookeeper)
- **Python 3.8+**
- **Apache Spark (with PySpark)**
- **Kafka-Python & PySpark libraries**

Install the required Python packages:
```sh
pip install pyspark kafka-python
```

## Project Structure
```
├── docker-compose.yml      # Kafka & Zookeeper setup
├── kafka_spark_streaming.py # Spark Streaming consumer
├── readme.txt              # Instructions
├── local_checkpoint/       # Checkpoint directory for Spark Streaming
```

## Step 1: Set Up Kafka Using Docker
Run the following command to start Kafka and Zookeeper:
```sh
docker-compose up -d
```
This will start:
- **Zookeeper** (Port: 22181)
- **Kafka Broker** (Port: 29092)

Verify Kafka is running:
```sh
docker ps
```

## Step 2: Create Kafka Topics
To create the required topics manually (if needed):
```sh
docker exec -it <kafka-container-id> kafka-topics --create --topic user-login --bootstrap-server localhost:29092 --partitions 1 --replication-factor 1

docker exec -it <kafka-container-id> kafka-topics --create --topic processed-topic --bootstrap-server localhost:29092 --partitions 1 --replication-factor 1
```

## Step 3: Run the Spark Streaming Consumer
Execute the Spark Streaming application:
```sh
python kafka_spark_streaming.py
```

This will:
1. Consume data from the **`user-login`** Kafka topic.
2. Transform timestamps into a human-readable format.
3. Publish the processed data into the **`processed-topic`** Kafka topic.
4. Ensure fault tolerance using **checkpointing**.

## Cleanup
To stop all running services:
```sh
docker-compose down
```
