#!/bin/bash

SPARK_WORKLOAD=$1

echo "SPARK_WORKLOAD: $SPARK_WORKLOAD"

if [ "$SPARK_WORKLOAD" == "master" ]; then
  start-master.sh -h spark-master -p 7077
elif [ "$SPARK_WORKLOAD" == "worker" ]; then
  start-worker.sh spark://spark-master:7077
else
  start-history-server.sh
fi