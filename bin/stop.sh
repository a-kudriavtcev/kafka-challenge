#!/bin/bash
docker compose \
  --project-name kafka-challenge \
  down ${*}
