# Kafka Challenge: Solution Prototype

## Overview
This prototype offers a solution for processing streaming data (real-time Wikipedia updates). The system consists of a Kafka cluster, a producer, a consumer and Cassandra database instance. The producer reads the data from the provided CSV file line by line and emits it onto a Kafka topic every 0 to 1 seconds. The consumer listens to the incoming data, performs required aggregations and ingests the data into the database.

![kafka-challenge drawio (1)](https://github.com/a-kudriavtcev/kafka-challenge/assets/39767359/c2d41fc9-7d3e-4937-807e-ea3e8ffcf4c8)


## Run and check the data 
To run the project locally, execute `bin/start.sh`. This will spin up the docker containers. 

To see the aggregated data:
- wait until you start getting logs like `Batch No. 0 with updated count ingested into Cassandra`, emitted by the `spark-consumer` service
- use a DB Client, for example [DbVisualizer](https://www.dbvis.com/), to access Cassandra DB
- navigate to the keyspace `wiki_updates_ks` and go to the table `wiki_updates_table`. Note that [DbVisualizer](https://www.dbvis.com/) is sometimes *buggy* and won't display the table columns properly! In this case just *restart* it. You should see something like this:

<img width="915" alt="Bildschirmfoto 2023-12-13 um 23 57 50" src="https://github.com/a-kudriavtcev/kafka-challenge/assets/39767359/a505a5dc-f4a5-4def-bcaf-04d052689d29">

The final result should look like this:

<img width="934" alt="Bildschirmfoto 2023-12-14 um 00 08 18" src="https://github.com/a-kudriavtcev/kafka-challenge/assets/39767359/4a0c51ca-85a3-4a74-b14d-34967fd39a55">

## Motivation behind Cassandra DB

The reasons to use Cassandra DB in the current scenario are the following:

- capable to handle large volumes of data in real time
- very good scalability
- high availability
- low ingestion latency and high throughput
- flexible data model
- we do not need to maintain data consistency

There are, however, also some disadvantages:
- advanced queries may be hard or even impossible to implement
- database may be complex to configure
- CQL (Cassandra Query Language) may present a steep learning curve for developers

