#! /bin/bash
# Stops the stack of containers and removes the _webdata container
# as it contains only non-persistent data.

SCRIPTPATH=$(cd "$(dirname "$0")"; pwd -P)
SOURCE_DIR=$(cd "$SCRIPTPATH" && cd .. && pwd -P)
PROJECT_NAME=errorreports

cd ${SOURCE_DIR}
docker-compose down
docker volume rm ${PROJECT_NAME}_webdata
