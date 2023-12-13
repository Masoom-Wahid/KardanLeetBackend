.PHONY: default create-venv activate-venv install-requirements makemigrations migrate su runserver check-compilers

PYTHON := python3
VENV := venv
REQUIREMENTS := requirments.txt
OS := $(shell uname -s)

default: install-requirements makemigrations migrate su runserver
check-compilers:
	@command -v python3 >/dev/null 2>&1 && { echo -e "\033[32mPython found\033[0m"; } || { echo -e "\033[31mPython not found\033[0m"; exit 1; }
	@command -v node >/dev/null 2>&1 && { echo -e "\033[32mNode.js found\033[0m"; } || { echo -e "\033[31mNode.js not found\033[0m"; exit 1; }
	@command -v tsc >/dev/null 2>&1 && { echo -e "\033[32mTSC Compiler Found\033[0m"; } || { echo -e "\033[31mTSC Compiler not found\033[0m"; exit 1; }
	@command -v g++ >/dev/null 2>&1 && { echo -e "\033[32mg++ found\033[0m"; } || { echo -e "\033[31mg++ not found\033[0m"; exit 1; }
	@command -v rustc >/dev/null 2>&1 && { echo -e "\033[32mRust found\033[0m"; } || { echo -e "\033[31mRust not found\033[0m"; exit 1; }
	@command -v mcs >/dev/null 2>&1 && { echo -e "\033[32mMono C# compiler found\033[0m"; } || { echo -e "\033[31mMono C# compiler not found\033[0m"; exit 1; }
	@command -v php >/dev/null 2>&1 && { echo -e "\033[32mPHP found\033[0m"; } || { echo -e "\033[31mPHP not found\033[0m"; exit 1; }
	@command -v javac >/dev/null 2>&1 && { echo -e "\033[32mJavaC compiler found\033[0m"; } || { echo -e "\033[31mJavaC compiler not found\033[0m"; exit 1; }
	@command -v java >/dev/null 2>&1 && { echo -e "\033[32mJava compiler found\033[0m"; } || { echo -e "\033[31mJava compiler not found\033[0m"; exit 1; }
.PHONY: check-compilers






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

