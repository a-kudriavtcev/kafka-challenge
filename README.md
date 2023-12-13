# kafka-challenge

## Overview
This prototype offers a solution for processing streaming data (real-time Wikipedia updates). The system consists of a Kafka cluster, a producer, a consumer and Cassandra database instance. The producer reads the data from the provided CSV file line by line and emits it onto a Kafka topic every 0 to 1 seconds. The consumer listens to the incoming data, performs required aggregations and ingests the data into the database.

![kafka-challenge drawio](https://github.com/a-kudriavtcev/kafka-challenge/assets/39767359/884296c0-c563-4b80-8fd1-983b47e36faa)

## Run and see the data 
To run the project locally, execute `bin/start.sh`. This will spin up the docker containers. 

To see the aggregated data:
- wait until you start getting logs like `Batch No. 0 with updated count ingested into Cassandra`, emitted by the `spark-consumer` service
- use a DB Client, for example [DbVisualizer](https://www.dbvis.com/), to access Cassandra DB and check that the data is being properly updated
- navigate to the keyspace `wiki_updates_ks` and go to the table `wiki_updates_table`. You should see something like this:
