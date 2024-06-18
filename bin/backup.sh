#!/bin/bash

# Takes a backup of the error reporter DB in the current dir
if [[ -z "$1" ]]; then
    >&2 echo "The name of the file to backup is required"
    exit 1
fi


SCRIPTPATH=$(cd "$(dirname "$0")"; pwd -P)
SOURCE_DIR=$(cd "$SCRIPTPATH" && cd .. && pwd -P)

source ${SOURCE_DIR}/.env

PROJECT_NAME=errorreports
PG_DOCKER_NAME=$PROJECT_NAME"-postgres-1"

docker exec -t $PG_DOCKER_NAME pg_dumpall -c -U ${DB_USER} | gzip > $1
