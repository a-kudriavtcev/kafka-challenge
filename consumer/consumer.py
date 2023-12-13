from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.functions import col, window
from pyspark.sql.types import StringType
from schemas import WIKI_UPDATE_SCHEMA
from pyspark.sql.functions import (
    window,
    count,
    to_timestamp,
    from_unixtime,
    col,
    when,
    sum as agg_sum,
)

# from delta import *

# from delta import *

import sys, os

var = os.path.dirname(sys.executable)
print("PYTHONPATH", var)

spark = (
    SparkSession.builder.appName("Kafka Consumer")
    .master("local[*]")
    # .config("spark.cassandra.connection.host", "172.18.0.5")
    # .config("spark.cassandra.connection.port", "9042")
    # .config("spark.cassandra.auth.username", "cassandra")
    # .config("spark.cassandra.auth.password", "cassandra")
    .config("spark.driver.host", "localhost")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")


input_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "WikiUpdates3")
    .option("startingOffsets", "earliest")
    .load()
)

# input_df.printSchema()

expanded_df = (
    input_df.selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), WIKI_UPDATE_SCHEMA).alias("WikiUpdate"))
    .select("WikiUpdate.*")
)

# expanded_df.printSchema()
expanded_df = expanded_df.select("timestamp", "wiki")

# Define a window specification based on the timestamp column and the desired interval (e.g., 1 minute)
window_spec = window("timestamp", "1 minute")

# Perform aggregation to count the number of events per minute

# total_events_per_min = expanded_df.groupBy(window_spec).count()


transformed_df = expanded_df.groupBy(window('timestamp', '1 minute')).agg(
    (agg_sum(when(col('wiki') == 'dewiki', 1).otherwise(0)).alias('count_germany')),
    count('wiki').alias('worldwide'),
)
# total_events_per_min = total_events_per_min.withColumnRenamed('count', 'count_worldwide')

# events_per_min_germany = (
#     expanded_df.withWatermark('timestamp', '5 seconds')
#     .filter(col("wiki") == "dewiki")
#     .groupBy(window_spec)
#     .count()
# )
# events_per_min_germany = events_per_min_germany.withColumnRenamed('count', 'count_germany')

# joined_dfs = total_events_per_min.join(events_per_min_germany, on='Window', how='full_outer')


# def join_them(expanded_df, epoch_id):
#     total_events_per_min = expanded_df.groupBy(window_spec).count()

#     total_events_per_min = total_events_per_min.withColumnRenamed('count', 'count_worldwide')

#     events_per_min_germany = (
#         expanded_df.filter(col("wiki") == "dewiki").groupBy(window_spec).count()
#     )
#     events_per_min_germany = events_per_min_germany.withColumnRenamed('count', 'count_germany')
#     joined_dfs = total_events_per_min.join(events_per_min_germany, on='Window', how='full_outer')
#     # joined_dfs.printSchema()
#     # return joined_dfs


# query1 = (
#     expanded_df.writeStream.trigger(processingTime="400 seconds")
#     .foreachBatch(join_them)
#     .format("console")
#     .option("truncate", False)
#     .outputMode("update")
#     .start()
#     .awaitTermination()
# )


# union_df = total_events_per_min.union(events_per_min_germany)

# deltaTable = DeltaTable.forPath(spark, "/tmp/wiki-updates")

# data.write.format("delta").save("/tmp/delta-table")


# def aggregate_and_save_to_cassandra(writeDF, epoch_id):
#     print("Printing epoch_id: ")
#     print(epoch_id)

#     writeDF.write.format("org.apache.spark.sql.cassandra").mode('append').options(
#         table="wiki_updates_table", keyspace="wiki_updates_ks"
#     ).save()

#     print(epoch_id, "saved to Cassandra")


# Show the result
streaming_query = (
    transformed_df.writeStream.outputMode("complete")
    .format("console")
    .option("truncate", False)
    .start()
    .awaitTermination()
)

# print("Events per min in Germany")
# streaming_query = (
#     events_per_min_germany.writeStream.outputMode("complete")
#     .format("console")
#     .option("truncate", False)
#     .start()
# )


# uuid_udf = udf(lambda: str(uuid.uuid4()), StringType()).asNondeterministic()
# expanded_df = total_events_per_min.withColumn("uuid", uuid_udf())
# expanded_df.printSchema()


# customers_df = spark.read.csv("customers.csv", header=True, inferSchema=True)
# customers_df.printSchema()

# sales_df = expanded_df.join(
#     customers_df, expanded_df.customer_id == customers_df.customer_id, how="inner"
# )
# sales_df.printSchema()

# final_df = (
#     sales_df.groupBy("source", "state")
#     .agg({"total": "sum"})
#     .select("source", "state", col("sum(total)").alias("total_sum_amount"))
# )
# final_df.printSchema()


# Output to Console
# expanded_df.writeStream \
#   .outputMode("append") \
#   .format("console") \
#   .option("truncate", False) \
#   .start() \
#   .awaitTermination()

# Output to Console
# final_df.writeStream \
#   .trigger(processingTime="15 seconds") \
#   .outputMode("update") \
#   .format("console") \
#   .option("truncate", False) \
#   .start()
