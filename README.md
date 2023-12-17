# Propylon Document Manager Assessment

The Propylon Document Management Technical Assessment is a simple (and incomplete) web application consisting of a basic API backend and a React based client. This API/client can be used as a bootstrap to implement the specific features requested in the assessment description.

# Docs

## Desgin

- Separation of FE/ BE components

- Auth (Sign Up/ Sign In) via FE / API

## Database Design

![schema](docs/schema.png)

- A user Can have multiple files
- A File can have any number of versions
- Content of file version needs to be unique for each file object
- Each file should have atleast file Version attached to it

## Getting Started

1. Install [Docker](https://www.docker.com/products/docker-desktop/)
2. `$ make build`. This will spin up docker image for the Backend Server
3. `$ make start-db` This will spin up mysql db instance

   - This should create propylon db as well.
   - If it didn't

     - Connect to mysql instance and run create schema

       1. `$ make db_shell`
       2. ```sql
          CREATE DATABASE /*!32312 IF NOT EXISTS*/ `propylon` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
          ```

   - Run `$ make init_db` to initialise db.

4. `$ make migrate` to create the tables.

5. `$ make run` to start the development server on port 8001.
6. Navigate to the client/document-manager.
7. `$ npm install` to install the dependencies.
8. `$ ng s` to start the [Angular](https://angular.io/) development server.
9. `$ make clean` To stop all services

10. `$ make load_file_fixtures` to create the fixture file versions.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **superuser account**, use this command:

      $ make createsuperuser

### Type checks

Running type checks with mypy:

    $ make mypy

### Test coverage

#### Running tests with pytest

    $ make test

## Make Commands

#### Start Backend

    $ make start

#### Run Tests with Coverage Report

    $ make test

#### Run formatting (isort and then black)

    $ make formatter

#### Database Administration

    $ make phpmyadmin

This spins up phymyadmin container. We can view , edit, create tables /db . Admin is available at : http://localhost:7700/
