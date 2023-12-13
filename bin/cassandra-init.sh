#!/usr/bin/env bash

until printf "" 2>>/dev/null >>/dev/tcp/cassandra/9042; do
    sleep 5;
    echo "Waiting for cassandra...";
done

echo "Creating keyspace and table..."
cqlsh cassandra -u cassandra -p cassandra -e "CREATE KEYSPACE IF NOT EXISTS wiki_updates_ks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE TABLE IF NOT EXISTS wiki_updates_ks.wiki_updates_table(uuid uuid primary key, updates_per_min int, updates_per_min_germany int);"


[11:56] Fehemi Lecini
command: >
      /bin/sh -c "
        echo Waiting for rabbitmq service start...;
        while ! nc -z kafka-init 9092;
        do
          sleep 1;
        done;
        echo Connected!;
      "