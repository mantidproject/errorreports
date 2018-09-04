mv .test_env .env
./bin/shutdown.sh
./bin/boot.sh
docker exec -it errorreports_web_1 sh -c "python manage.py test"