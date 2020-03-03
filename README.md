# MUD Backend

Django backend for cspt5 MUD game

## Setting Up Dev Environment

1. Set up virtual environment
2. Set up PostgreSQL database server

### Setting up the virtual environment

Install with conda via:

> conda create --file environment.yml

Insall with pipenv:

> pipenv install

### Docker PostgreSQL Image

Using podman (similar to docker):

> podman run --rm --name postgres-general -p 5432 -e POSTGRES_PASSWORD=cspt5 postgres

> Check the port in use by opening a second terminal and using "podman ps" to list active containers.  Ensure the port listed matches the default in django.