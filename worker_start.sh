#!/bin/bash

cd /app

celery -A l4mbda.tasks worker -c 4 --max-tasks-per-child 100

while true; do
  sleep 10
done
