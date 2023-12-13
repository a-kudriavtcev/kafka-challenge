# kafka-challenge

# Overview
This prototype offers a solution for processing streaming data which is represented by real-time Wikipedia updates. It consists of a Kafka cluster, a producer and a consumer. The producer reads the data from the provided CSV file line by line and emits it onto a Kafka topic every 0 to 1 seconds. The consumer listens to the incoming data and performs aggregations required by the customer.

![kafka-challenge drawio](https://github.com/a-kudriavtcev/kafka-challenge/assets/39767359/884296c0-c563-4b80-8fd1-983b47e36faa)


# Setup
To run the project locally:
- execute `bin/start.sh`. This will spin up the necessary docker containers which will perform their respective tasks. 
- wait until you start seeing the log
- stop the system with with `CMD+C` or `bin/stop.sh`
