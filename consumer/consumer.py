from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.functions import col, window
from pyspark.sql.types import StringType
from schemas import WIKI_UPDATE_SCHEMA
from pyspark.sql.functions import (
    window,
    count,
    col,
    when,
    sum as agg_sum,
)
from persistence import ingest_into_cassandra


spark = (
    SparkSession.builder.appName("Kafka Consumer")
    .master("local[*]")
    .config("spark.cassandra.connection.host", "cassandra")
    .config("spark.cassandra.connection.port", "9042")
    .config("spark.cassandra.auth.username", "cassandra")
    .config("spark.cassandra.auth.password", "cassandra")
    .config("spark.driver.host", "localhost")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

input_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "WikiUpdates")
    .option("startingOffsets", "earliest")
    .load()
)


expanded_df = (
    input_df.selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), WIKI_UPDATE_SCHEMA).alias("WikiUpdate"))
    .select("WikiUpdate.*")
)

expanded_df = expanded_df.select("timestamp", "wiki")

window_spec = window("timestamp", "1 minute")

expanded_df = expanded_df.groupBy(window('timestamp', '1 minute')).agg(
    (agg_sum(when(col('wiki') == 'dewiki', 1).otherwise(0)).alias('updates_germany')),
    count('wiki').alias('updates_worldwide'),
)

query = (
    expanded_df.writeStream.trigger(processingTime="5 seconds")
    .foreachBatch(ingest_into_cassandra)
    .outputMode("update")
    .start()
    .awaitTermination()
)
