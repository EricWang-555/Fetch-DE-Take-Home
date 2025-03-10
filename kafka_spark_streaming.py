from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StringType
from kafka import KafkaProducer
import json
import os
from datetime import datetime

# Kafka Configuration
KAFKA_BROKER = "localhost:29092"
INPUT_TOPIC = "user-login"
OUTPUT_TOPIC = "processed-topic"

# Define local checkpoint directory
CHECKPOINT_DIR = "./local_checkpoint"
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

schema = StructType() \
    .add("user_id", StringType()) \
    .add("device_type", StringType()) \
    .add("ip", StringType()) \
    .add("locale", StringType()) \
    .add("device_id", StringType()) \
    .add("timestamp", StringType())

# UDF to convert timestamp
@udf(StringType())
def convert_timestamp(ts):
    try:
        return datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return None

def main():
    spark = SparkSession.builder \
        .appName("KafkaSparkStreaming") \
        .master("local[*]") \
        .config("spark.sql.streaming.checkpointLocation", CHECKPOINT_DIR) \
        .getOrCreate()

    kafka_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", INPUT_TOPIC) \
        .option("startingOffsets", "earliest") \
        .load()

    parsed_stream = kafka_stream.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # some transformation
    processed_stream = parsed_stream.withColumn("timestamp", convert_timestamp(col("timestamp")))

    query = processed_stream.writeStream \
        .outputMode("append") \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("topic", OUTPUT_TOPIC) \
        .option("checkpointLocation", CHECKPOINT_DIR) \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()