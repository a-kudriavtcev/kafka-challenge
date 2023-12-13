#!/bin/bash
set -e

exec docker compose --project-name kafka-challenge up --build --remove-orphans --renew-anon-volumes --force-recreate ${*}