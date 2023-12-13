.PHONY: default create-venv activate-venv install-requirements makemigrations migrate

PYTHON := python3
VENV := venv
REQUIREMENTS := requirments.txt
OS := $(shell uname -s)

default: install-requirements makemigrations migrate su runserver

create-venv:
	$(PYTHON) -m venv $(VENV)

su:
	$(PYTHON) manage.py createsuperuser

runserver:
	$(PYTHON) manage.py runserver


ifeq ($(OS),Linux)
activate-venv:
	source $(VENV)/bin/activate
else ifeq ($(OS),Darwin)
activate-venv:
	source $(VENV)/bin/activate
else ifeq ($(OS),Windows_NT)
activate-venv:
	$(VENV)\Scripts\activate
else
activate-venv:
	@echo "Unsupported operating system: $(OS)"
	exit 1
endif

install-requirements: activate-venv
	pip install -r $(REQUIREMENTS)

makemigrations: install-requirements
	python manage.py makemigrations

migrate: makemigrations
	python manage.py migrate

req:
	pip freeze > requirments.txt

