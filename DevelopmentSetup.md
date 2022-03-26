# Setup for Development

Docker is used to isolate all application dependencies from the main (host)
system.
As such, the only requirements for the host system are:

* Docker
* docker-compose

## Installing Docker

[Docker](https://docs.docker.com/get-started/) is a platform for running
applications in isolated environments called containers. See the previous link
for an introductory tutorial.

The installation method for Docker varies depending on your operating system.

### macOS/Windows

We recommend using [Docker Desktop](https://www.docker.com/products/docker-desktop/).
*Please note that Docker Desktop can only be used for free under the conditions listed
by their license agreement: <https://www.docker.com/products/docker-desktop/>.*.

Download the correct package from the
[Desktop section](https://docs.docker.com/engine/install/#desktop) of the Docker installation reference and install it.

**Windows Non-Admin Setup**: For Windows an extra step is necessary to be able to run Docker without administrator privileges:

* In the start menu, type `mmc.` to get the management console. On the right-side click run as administrator, this should prompt you for your administrator credentials.
* Go to `File` -> `Add Snap-In` -> `Add Local Users and Groups`. Ensure Local Computer is ticked and simply click next. It will now appear on the right hand list. Click Ok to close the dialog
* Expand Local Users and Groups then select groups
* Ensure you are connected to the VPN if you're off-site
* Open the `docker-users` group and add your normal ID (i.e. not the administrator account)
* Log off / in with that account

**Windows WSL2**: Docker Desktop will prompt for installation of WSL2. Follow the link and restart your machine to complete installation.

Once installed, start the desktop application from either
Spotlight search (macOS) or Start menu (Windows).
This will take a few moments.

Once started see [verifying installation](#verifying-installation).

### Linux

We recommend installing the appropriate server package for the Linux distribution from the Docker repositories. Please follow the guide in the
[Server section](https://docs.docker.com/engine/install/#server) for your
running distribution.

To run Docker as a non-root user (recommended) add your user to the docker group:

```sh
> sudo usermod -a -G docker $USER
```

You'll need to log out and log back in for this to take effect.

The installation does not come with a GUI and should be started automatically by the installation. Once installed see [verifying installation](#verifying-installation).

### Verifying Installation

Once docker has started, open a terminal or command prompt and type:

```sh
>docker run --rm hello-world
```

You should see something similar to:

```sh
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
2db29710123e: Pull complete
Digest: sha256:bfea6278a0a267fad2634554f4f0c6f31981eea41c553fdf5a83e95a41d40c38
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

Some of the text such as the hash values may vary.

Congratulations your Docker installation is working!

## Installing docker-compose

[Docker Compose](https://docs.docker.com/compose/) is a tool for configuring
and running applications by splitting them into multiple containers.
See the previous link for an introductory tutorial.

### macOS/Windows

`docker-compose` is now included within Docker Desktop so if you have used this
method you have the command already. Verify this by running:

```sh
>docker-compose version
```

that should print the compose version.

### Linux

Compose must be installed separately.
See the [Linux section](https://github.com/docker/compose#where-to-get-docker-compose)
of the compose installation for links to download the executable and place it
in the right location.

## Fetching the Code

Clone this repository locally:

```sh
> git clone https://github.com/mantidproject/reports.git
```

## Creating an Environment (.env) File

The docker-compose configuration requires setting some environment variables
such as

* the port to run on
* the name of the database user
* the database password

in order to function correctly. Docker compose supports the de-facto standard
method for setting initial environment variables: `.env files`.
If a file called `.env` is present in the same directory as `docker-compose.yml`
then this file is sourced and the variables contained within are exported to the
compose environment.

The production instance has a secure copy of `.env` used for itself.
There is no default copy provided for development to ensure this is
not accidentally used by production. It is ignored by `.gitignore`.

A blank template file is provided in [blank.env](blank.env) to aid in creation
of a file for development. To create a local copy run the following from the
root of this repository clone (use Git Bash on Windows):

```sh
cp blank.env .env
```

Open the file and follow the instructions in the comments.

**Do not add this file to the version control system!**.

## Running the Server

To start the server, from the root of your clone run: (use Git Bash on Windows)

```sh
bash bin/boot.sh
```

The server should be accessible via `http://localhost:<HOST_PORT>`,
where `HOST_PORT` is the value defined in the `.env` file.

## Django Admin Account

To access the Django admin interface you will need to create a Django admin account.
This needs to be done whenever a fresh database container is created, mostly when
setting up for the first time.

To create the account run:

```sh
docker-compose exec web python manage.py createsuperuser
```

and enter the requested details. Once the account has been created go to
`http://localhost:<HOST_PORT>/admin` and login with the details you provided.
