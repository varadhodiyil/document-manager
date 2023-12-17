SERVICE_NAME=backend_service
PROJECT_NAME=propylon_document_manager
TIME=60

# colors
GREEN = $(shell tput -Txterm setaf 2)
YELLOW = $(shell tput -Txterm setaf 3)
WHITE = $(shell tput -Txterm setaf 7)
RESET = $(shell tput -Txterm sgr0)
GRAY = $(shell tput -Txterm setaf 6)
TARGET_MAX_CHAR_NUM = 20


build:
	@docker-compose build $(SERVICE_NAME)


run:
	docker-compose up $(SERVICE_NAME)

#Stop all service
stop:
	@docker-compose stop

clean:
	@docker-compose down

bash:
	@docker exec -it $(SERVICE_NAME) bash


black:
	@docker-compose run --rm $(SERVICE_NAME) black $(PROJECT_NAME) --exclude $(PROJECT_NAME)/migrations -l 79

## Checks types with `mypy`.
mypy:
	@docker-compose run --rm $(SERVICE_NAME) mypy $(PROJECT_NAME)

# isort & format code 
formatter:
	@docker-compose run --rm $(SERVICE_NAME) isort $(PROJECT_NAME)
	@docker-compose run --rm $(SERVICE_NAME) black $(PROJECT_NAME)

lint:
	@docker-compose run --rm $(SERVICE_NAME) pylint $(PROJECT_NAME)
## Runs tests. | Tests
test:
	@docker-compose run --rm $(SERVICE_NAME) pytest $(PROJECT_NAME)

# Django migrate
migrate:
	@docker-compose run --rm $(SERVICE_NAME) python manage.py migrate

# Django make migration
makemigrations:
	@docker-compose run --rm $(SERVICE_NAME) python manage.py makemigrations

# db Viewer
phpmyadmin:
	@docker-compose up phpmyadmin

#load file Fixtures
load_file_fixtures:
	@docker-compose run --rm $(SERVICE_NAME) python manage.py load_file_fixtures

start-db:
	@docker-compose up -d dB 

init_db:
	@docker exec -it dB mysql -u root --password="propylon@test123" mysql < datasource/propylon.sql

db_shell:
	@docker exec -it dB mysql -u root --password="propylon@test123"

createsuperuser:
	@docker-compose run --rm $(SERVICE_NAME) python manage.py createsuperuser