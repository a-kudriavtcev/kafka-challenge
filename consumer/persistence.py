def ingest_into_cassandra(writeDF, epoch_id):
    writeDF = writeDF.select(
        writeDF.window.cast("string").alias("time_window"),
        writeDF.window.start.cast("string").alias("start_time"),
        writeDF.window.end.cast("string").alias("end_time"),
        "updates_germany",
        "updates_worldwide",
    )

    writeDF.write.format("org.apache.spark.sql.cassandra").mode('append').options(
        table="wiki_updates_table", keyspace="wiki_updates_ks"
    ).save()

    print(f"Batch No. {epoch_id} with updated count ingested into Cassandra")
