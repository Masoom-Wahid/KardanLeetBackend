.PHONY: create-venv activate-venv install-requirements default

PYTHON := python3
VENV := venv
REQUIREMENTS := requirments.txt
OS := $(shell uname -s)

create-venv:
	$(PYTHON) -m venv $(VENV)
su:
	$(PYTHON) manage.py createsuperuser
ifeq ($(OS),Linux)
activate-venv:
	source ./$(VENV)/bin/activate 
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

install-requirements:
	pip install -r $(REQUIREMENTS)

makemigrations:
	$(PYTHON) manage.py makemigrations

migrate:
	$(PYTHON) manage.py migrate


default:
	create-venv
	activate-venv
	install-requirements
	makemigrations
	migrate

req:
	pip freeze > requirments.txt

