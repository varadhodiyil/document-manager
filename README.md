# Propylon Document Manager

Propylon Document Management Technical Assessment

## Getting Started
1. [Install Direnv](https://direnv.net/docs/installation.html)
2. [Install Pipenv](https://pipenv.pypa.io/en/latest/installation/)
3. This project requires Python 3.11 so you will need to ensure that this version of Python is installed on your OS before building the virtual environment.
4. `$ cp example.env .envrc`
5. `$ direnv allow .`
6. `$ pipenv install -r requirements/local.txt`

## Events System 
This repository is setup to use the LWB360 Events system.
The events system can be run locally via a checked out version via docker.  Or can be run with the latest published events system docker image. 
See the `example.env` for the environment variables that inform the location of the event system code. 

### Initializing the LWB360 Events System
1. `docker-compose --profile up` will control which events application profile you would like to start in.  `events_app` profile will load the docker from the latest published container image.  `events_dev` will load the docker container using a local copy of the events system source.
2. Navigate to the [admin site](http://localhost:8008/admin/) for the event system.  Have a look at the lwb360-events code for default admin username and password.  Navigate to the tokens area of the panel.
3. Copy the token/key of the initial entry for `lwb360.event_log` into your `.envrc` file, assigning the value to `LWB360_EVENTS_APP_TOKEN`.
### Create Test Events
1. Run the `register_app` management command through either the [launch.json](.vscode/launch.json) file or the [Makefile](Makefile) target.  This will register the bootstrap application with the event system.
2. Run the `create_debug_event` management command through either the [launch.json](.vscode/launch.json) file or the [Makefile](Makefile) target. This will create a demonstration `EventRecord`.  You will see more data now in the events sytem admin including new [EventRecord](http://localhost:8008/admin/lwb360_events/eventrecord/) entries.
### Create and Test Subscription
1. Use the events system Django admin to [create a new subscription](http://localhost:8008/admin/lwb360_events/subscription/add/).  Select the newly registered application as the subscriber, the `lwb360.drafting.drafting_test` as the topic, and `http://host.docker.internal:8001/debug-event/` as the callback url, which is the only endpoint available in the [views.py](src/lwb360_ib/api/views.py) file.
2. Run the `serve` command through either the [launch.json](.vscode/launch.json) file or the [Makefile](Makefile) target.  This will start the bootstrap application.
3. Run the `create_debug_event` management command through either the [launch.json](.vscode/launch.json) file or the [Makefile](Makefile) target. This should result in the event information being echoed in the console log of this application. 

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy propylon_document_manager

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest
