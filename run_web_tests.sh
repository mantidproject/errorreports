ENV_FILE=.env
DB_DIR=pgdata
DJANGO_SERVICE_NAME=web
CLEAN_ENV=false
CLEAN_SERVICES=false

if [[ ! -f "$ENV_FILE" ]]; then
  if [[ -d ${DB_DIR} ]]; then
    echo "A $ENV_FILE file could not be found yet a '${DB_DIR}' directory exists."
    echo "This implies a database has been created but the credentials are missing."
    echo "Tests will fail as they won't be able to access the database."
    echo "IF IN A DEVELOPMENT ENVIRONMENT remove ${DB_DIR} and re-run this script."
    exit 1
  fi

  echo "No $ENV_FILE file and no DB found. Generating .env file for tests."
  echo "Both .env file and DB will be cleaned "
  cat blank.env |\
  sed -e "s@DEBUG=false@DEBUG=true@" |\
  sed -e "s@SECRET_KEY=<Not Set>@SECRET_KEY=123456789abcdefghijkl@" |\
  sed -e 's@DB_USER=<Not Set>@DB_USER=testuser@' |\
  sed -e 's@DB_PASS=<Not Set>@DB_PASS=testuserpasswd@' |\
  sed -e 's@SLACK_WEBHOOK_URL=<Not Set>@SLACK_WEBHOOK_URL=@' |\
  sed -e 's@DJANGO_CSRF_TRUSTED_ORIGINS=<Not Set>@DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8083@' > ${ENV_FILE}
  CLEAN_ENV=true
else
  echo "Running tests using an existing environment file..."
fi

if [[ -z $(docker compose ps --quiet --filter status=running $DJANGO_SERVICE_NAME) ]]; then
  echo "Booting services."
  ./bin/boot.sh
  CLEAN_SERVICES=true
else
   echo "Services already running.."
fi

echo "Executing web tests..."
docker compose exec $DJANGO_SERVICE_NAME sh -c "python manage.py test $@"

# Clean up
if [[ $CLEAN_SERVICES == true ]]; then
  echo "Shutting down services that were auto started."
  ./bin/shutdown.sh
fi
if [[ $CLEAN_ENV == true ]]; then
  echo "Cleaning auto-generated .env file"
  rm -f $ENV_FILE
fi
