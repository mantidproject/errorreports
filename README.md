![Build Status](https://github.com/mantidproject/errorreports/actions/workflows/ci.yml/badge.svg)

# Error Reporter Server

This repository holds the configuration for setting up a Django-based server to
capture error reports sent by [Mantid](https://github.com/mantidproject/mantid).

## Mantid Configuration

### Production

The production server runs at <https://errorreports.mantidproject.org> and
Mantid is configured by default to send to this server.

### Development

While developing this server Mantid can be configured to send to the instance
started locally by editing `mantid_build_dir/bin/Mantid.properties` and changing

```sh
errorreports.rooturl = http://localhost:8083
```

This will require a restart of Mantid.
Note that the port number depends on the value specified of `HOST_PORT`
specified in the environment file but defaults to the above value.
See [DevelopmentSetup](DevelopmentSetup.md) for how to setup and environment file.

## Getting Started

To get started for development please follow the instructions in [DevelopmentSetup](DevelopmentSetup.md).

## Maintenance

Old error reports can be removed with the following docker command:

```sh
docker-compose exec web python manage.py removeoldreports [ndays] [--all]
```

where reports older than `ndays` are removed (default=90).
Passing `--all` removes all reports.
