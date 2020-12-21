#!/bin/bash

# Restores a backup of the error reporter DB in the current dir
if [[ -z "$1" ]]; then
    >&2 echo "The name of the file to restore is required"
    exit 1
fi

SCRIPTPATH=$(cd "$(dirname "$0")"; pwd -P)
SOURCE_DIR=$(cd "$SCRIPTPATH" && cd .. && pwd -P)

source ${SOURCE_DIR}/.env

PROJECT_NAME=errorreports
PG_DOCKER_NAME=$PROJECT_NAME"_postgres_1"

# sed - Removes an in-line comment to drop and restore the current user, which won't work as we are using that login to actually restore

# Use template1 (which will also exist for a new db) as the target, as psql needs a target DB even for a full restore
gunzip -c $1 | sed "/^DROP ROLE.*${DB_USER}/d;/^CREATE ROLE.*${DB_USER}/d" | docker exec -i $PG_DOCKER_NAME psql -U ${DB_USER} template1

echo "Please restart the stack to ensure ORM picks up changes"
