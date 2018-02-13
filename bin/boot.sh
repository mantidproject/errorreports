#! /bin/bash
# Starts the stack

function mk_django_secret() {
  python -c "import random,string;print '%s'%''.join([random.SystemRandom().choice(\"{}{}{}\".format(string.ascii_letters, string.digits, string.punctuation)) for i in range(63)])";
}

SCRIPTPATH=$(cd "$(dirname "$0")"; pwd -P)
SOURCE_DIR=$(cd "$SCRIPTPATH" && cd .. && pwd -P)
PROJECT_NAME=reports
DB_VOLUME_NAME=pgdata

# Required by django settings
DB_SERVICE=postgres
DB_PORT=5432
# Create a secret key
SECRET_KEY=$(mk_django_secret)
export DB_SERVICE DB_PORT SECRET_KEY

# Does the database volume already exist
_volume=$(docker volume ls | grep $DB_VOLUME_NAME)
if [ $# -eq 1 ]; then
  if [ -n "${_volume}" ]; then
    echo "Initial database dump supplied but database volume already exists. Please remove the volume to continue."
    exit 1
  fi
  if [ ! -f "$1" ]; then
    echo "SQL dump \"$1\" does not exist"
    exit 1
  fi
  DB_DUMP=$1
  if [ "${DB_DUMP:0:1}" != "/" ]; then
      DB_DUMP=$PWD/$DB_DUMP
  fi
  export DB_DUMP
  COMPOSE_FILES="--file ${SOURCE_DIR}/docker-compose.yml --file ${SOURCE_DIR}/docker-compose-db-import.yml"
  echo "Using provided database dump to populate database."
elif [ $# -eq 0 ]; then
  if [ -n "${_volume}" ]; then
    echo "Using existing database volume."
  else
    echo "Starting with clean database."
  fi
  COMPOSE_FILES="--file ${SOURCE_DIR}/docker-compose.yml"
else
  echo "Usage: $0 [path-postrges-sql-dump]"
  exit 1
fi

if [ ! -f ${SOURCE_DIR}/.env ]; then
  echo "Unable to find environment file ${SOURCE_DIR}/.env. It must contain the following variables:"
  echo "  DB_NAME, DB_USER, DB_PASS"
  exit 1
fi

# Build services
docker-compose ${COMPOSE_FILES} --project-name ${PROJECT_NAME} build
# Bring up the stack and detach
docker-compose ${COMPOSE_FILES} --project-name ${PROJECT_NAME} up -d
