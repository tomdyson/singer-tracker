.PHONY: test

test:
	pytest

install:
	pip install -r requirements.txt

lint:
	ruff check .

format:
	ruff format .

all: install lint format test