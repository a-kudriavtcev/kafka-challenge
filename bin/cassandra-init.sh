#!/usr/bin/env bash

until printf "" 2>>/dev/null >>/dev/tcp/cassandra/9042; do
    sleep 5;
    echo "Waiting for cassandra...";
done

echo "Creating keyspace and table..."
cqlsh cassandra -u cassandra -p cassandra -e "CREATE KEYSPACE IF NOT EXISTS wiki_updates_ks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE TABLE IF NOT EXISTS wiki_updates_ks.wiki_updates_table(start_time text primary key, end_time text, count_germany int, worldwide int);"