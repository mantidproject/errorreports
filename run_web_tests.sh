cp .test_env .env
./bin/boot.sh
sleep 30
docker exec -it errorreports_web_1 sh -c "python manage.py test"