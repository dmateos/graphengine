#!/bin/bash
#
docker run  \
  --env MYSQL_HOST=$MYSQL_HOST \
  --env MYSQL_NAME=$MYSQL_NAME \
  --env MYSQL_USER=$MYSQL_USER \
  --env MYSQL_PASSWORD=$MYSQL_PASSWORD \
  --env REDIS_HOST=$REDIS_HOST \
  --env REDIS_PASSWORD=$REDIS_PASSWORD \
  graph-worker
