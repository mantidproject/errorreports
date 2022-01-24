#! /bin/bash
# Stops the stack of containers and removes the _webdata container
# as it contains only non-persistent data.

SCRIPTPATH=$(cd "$(dirname "$0")"; pwd -P)
SOURCE_DIR=$(cd "$SCRIPTPATH" && cd .. && pwd -P)
PROJECT_NAME=errorreports

cd ${SOURCE_DIR}
docker-compose down

# the web data volume shouldn't really be persistent as all of the files
# come from an image
echo "Removing webdata volume so it is rebuilt on next startup"
rm -r "${SOURCE_DIR}/webdata"

echo "Removing external network nginx_net"
docker network rm nginx_net
