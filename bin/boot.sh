#! /bin/bash -e
# Starts the stack

function create_external_net(){
  network_name=nginx_net
  docker network inspect nginx_net >/dev/null 2>&1 || \
    docker network create --driver bridge nginx_net
}

SCRIPTPATH=$(cd "$(dirname "$0")"; pwd -P)
SOURCE_DIR=$(cd "$SCRIPTPATH" && cd .. && pwd -P)
PROJECT_NAME=errorreports

if [[ ! -f "$SOURCE_DIR/.env" ]]; then
  echo "Please copy and configure the .env file from blank.env"
  exit 1
fi

# Create empty directories, so they are not owned by root
mkdir -p "$SOURCE_DIR/pgdata"
mkdir -p "$SOURCE_DIR/webdata"

# Start external network
create_external_net
# Build services
docker-compose --project-name ${PROJECT_NAME} build
# Bring up the stack and detach
docker-compose --project-name ${PROJECT_NAME} up --detach

# Replace this loop with `--wait-timeout` when it is available
# with 'docker compose' v2
sleep_counter=0
while [ $(docker-compose ps --quiet --filter status=running | wc -l | xargs) -ne 4 ]
do
  sleep 1
  let counter++
  if [[ $counter -eq 30 ]]; then
    echo "Services have not come up to a running state."
    exit 1
  fi
  echo "Waiting for all services to be running."
done


echo "Services up and running."
