#!/bin/bash
#
docker run  \
  --env DB_HOST=$DB_HOST \
  --env DB_NAME=$DB_NAME \
  --env DB_USER=$DB_USER \
  --env DB_PASSWORD=$DB_PASSWORD \
  --env REDIS_HOST=$REDIS_HOST \
  --env REDIS_PASSWORD=$REDIS_PASSWORD \
  graph-worker
