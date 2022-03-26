![Build Status](https://github.com/mantidproject/errorreports/actions/workflows/ci.yml/badge.svg)

When developing, to send errorreports to your localhost server, edit `mantid_build_dir/bin/Mantid.properties`, change these lines:
```
usagereports.enabled = 1
errorreports.rooturl = http://localhost:8082
```

Working with docker
-------------------

After [installing docker](https://docs.docker.com/engine/installation/), verify the "hello world" image. [On fedora](https://docs.docker.com/engine/installation/linux/docker-ce/fedora/), the instructions are simply

```
$ sudo systemctl start docker
$ sudo docker run hello-world
```

To do build things with docker you will need to add yourself to the `docker` group
```
sudo usermod -aG docker $USER
```
You can try one of the variety of [quickstart
guides](https://docs.docker.com/get-started/part2/) to make sure that
your setup is otherwise working.

This configuration uses [`docker-compose`](https://github.com/docker/compose) and requires at least version `1.13`. If the version in your OS repo is too old then the latest binaries can be found at https://github.com/docker/compose/releases.

Much of the following is heavily adapted from the [docker django instructions](https://docs.docker.com/compose/django/) and
https://realpython.com/blog/python/django-development-with-docker-compose-and-machine/, which uses an example repo at
https://github.com/realpython/dockerizing-django.

To start the services locally you will first need to create a `.env` file next to `docker-compose.yml` containing, for example:


        DB_NAME=Test
        DB_USER=YourName
        DB_PASS=APassWord
        HOST_PORT=8082
        EMAIL_HOST=smtp.sparkpostmail.com
        EMAIL_HOST_USER=SMTP_Injection
        EMAIL_PORT=587
        EMAIL_HOST_PASSWORD=<Api password need to retrieve from sparkpost>
        EMAIL_TO_ADDRESS=<email to recieve reports>
        EMAIL_FROM_ADDRESS=error-reports@mantidproject.org
        SLACK_WEBHOOK_URL=https://hooks.slack.com/services/.......

The values of each key are irrelevant for the test setup. For production they need to be kept secret. The email enviromental variables may be left out if emailing functionality is not required.

Now start the services with:

```
$ bin/boot.sh
```
and the site will be viewable at `http://localhost:8082/admin`.

To stop the services execute:

```
$ bin/shutdown.sh
```
which ensures that the webdata volume is cleaned up.

Working with Django
-------------------

The first time you create a database you will need to create a Django admin account to access the Django admin interface. To do so first get into the docker container by running `docker exec -it <docker-web-container-name> bash` and then run `python manage.py createsuperuser`.

To see current web containers run `docker-compose ps`, for example: `errorreports_web_1`

To remove old error reports a Django command has been added. Running `docker exec <web-container-name> python manage.py removeoldreports` this will remove error reports over 90 days old. Supplying a positional integer argument will change the number of days old a report has to be to be removed. The `--all` option will remove reports!

OSX Setup
---------

On OSX we can use a `VirtualBox` driver to execute the `Dockerfile`

1. Edit the `.env` file to look something like:

        DB_NAME=Test
        DB_USER=YourName
        DB_PASS=APassWord
        HOST_PORT=8082
        EMAIL_HOST=smtp.sparkpostmail.com
        EMAIL_HOST_USER=SMTP_Injection
        EMAIL_PORT=587
        EMAIL_HOST_PASSWORD=<Api password need to retrieve from sparkpost>
        EMAIL_TO_ADDRESS=<email to recieve reports>
        EMAIL_FROM_ADDRESS=error-reports@mantidproject.org
        SLACK_WEBHOOK_URL=https://hooks.slack.com/services/.......

2. Create a virtual machine called `development`

        docker-machine create development --driver virtualbox
        
3. `docker-machine env development`
4. `eval $(docker-machine env development)`
5. `./bin/boot.sh` takes some time to run!
6. Finally, you need to forward the ports from VirtualBox so that they are accessible on your host machine.

        VBoxManage controlvm "development" natpf1 "tcp-port8082,tcp,,8082,,8082";


Migration Files
---------------

When changes have been made to the server, Django will create a migration file on docker in `web/services/migrations` reflecting these changes. When editing this repo, look for a docker migration file, copy to your local system and include in your PR.

1. run `docker-compse ps` and check for the relevant web container e.g. `errorreports_web_1`
2. Enter docker and find the migration file: `docker exec -it errorreports_web_1 bash` It should be in services/migrations.
3. Exit docker (Ctrl+D) and copy over the migration file, giving it a better name relevant to the server changes: `docker cp errorreports_web_1:/usr/src/app/services/migrations/0005_auto_20200123_1058.py web/services/migrations/0005_stacktrace_added_recoveryfile_removed.py`
4. Add this to your PR!

Misc Docker Commands
--------------------

The [`docker-compose exec`](https://docs.docker.com/compose/reference/exec/) command can be used to run commands within
the various containers:

* start a shell:
```
$ docker-compose exec web bash
```

* show details of the database volume
```
$ docker volume inspect pgdata
```
* start a shell and then attach the `psql` commandline tool:
```
$ docker-compose exec postgres bash
$ psql
```

* or look at the database directly
```
$ docker-compose exec -u postgres postgres psql
```
Then change to the correct database (defined in the `.env` file as `django`) and see the public tables
```
\c reports
\dt
```

* run commands directly with django's `manage.py`
```
$ docker-compose exec web bash
```
* Remove orphaned containers:
```
docker-compose down --remove-orphans
```
Delete things
=============
remove containers
```
$ docker rm -f $(docker ps -a -q)
```
remove volumes
```
$ docker rm -v $(docker ps -a -q)
```
remove images
```
docker rmi $(docker images -q)
```
[This article](https://discuss.devopscube.com/t/how-to-delete-all-none-untagged-and-dangling-docker-containers-and-images/23) suggests just doing which will delete volumes as well.
```
$ docker system prune --volumes
```


Random things found in my browser and other places
--------------------------------------------------

* [sqlectron](https://sqlectron.github.io/) is a desktop client for attaching to sql databases
* [docker-compose rm](https://docs.docker.com/compose/reference/rm/) removes stopped service containers. To list all volumes `docker volume ls`
* official [phpmyadmin docker](https://github.com/phpmyadmin/docker) image
* [adminer](https://hub.docker.com/_/adminer/) at [github repo](https://github.com/vrana/adminer)
* https://hub.docker.com/_/postgres/ says that you can add `.sql` scripts to `/docker-entrypoint-initdb.d/` of the docker image and they will be run on startup
