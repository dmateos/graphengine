#!/bin/bash

cd /app

while true; do
  gunicorn --bind 0.0.0.0:8080 --timeout 7200 --workers 8 l4mbda.wsgi
done
