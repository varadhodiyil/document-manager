PROJECT_NAME=propylon_document_manager
TIME=60

# colors
GREEN = $(shell tput -Txterm setaf 2)
YELLOW = $(shell tput -Txterm setaf 3)
WHITE = $(shell tput -Txterm setaf 7)
RESET = $(shell tput -Txterm sgr0)
GRAY = $(shell tput -Txterm setaf 6)
TARGET_MAX_CHAR_NUM = 20


test:
	pipenv run pytest -s

start:
	pipenv run python manage.py runserver 8001