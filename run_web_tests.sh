cp .test_env .env
./bin/boot.sh
sleep 30
docker exec -t errorreports_web_1 sh -c "python manage.py test"