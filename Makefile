PROJECT = 'rubik'

.PHONY: build format run test

build:
	@poetry export -o requirements.txt --without-hashes

format:
	@poetry run black $(PROJECT) tests

run:
	@poetry run python microservice.py

test:
	@poetry run pytest tests
