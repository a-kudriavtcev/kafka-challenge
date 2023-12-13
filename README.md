# kafka-challenge

# Overview
This prototype offers a solution for processing streaming data which is represented by real-time Wikipedia updates. It consists of a Kafka cluster, a producer and a consumer. The producer reads the data from the provided CSV file line by line and emits it onto a Kafka topic every 0 to 1 seconds. The consumer listens to the incoming data and performs aggregations required by the customer.

# Setup
To run the project locally:
- execute `bin/start.sh`. This will spin up the necessary docker containers which will perform their respective tasks. 
- wait until you see the aggregated Wikipedia updates logged by the consumer:
  
<img width="616" alt="Bildschirmfoto 2023-12-13 um 18 57 02" src="https://github.com/a-kudriavtcev/kafka-challenge/assets/39767359/8c761f88-4c2a-4f66-9ead-34a2cfc4226d">

- stop the system with with `CMD+C` or `bin/stop.sh`
