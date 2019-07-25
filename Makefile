install:
	pip install poetry
	poetry install

build:
	poetry run python -m saltdocker
	poetry run python -m saltdocker --push --dryrun
	pytest

push:
	docker login --username $(HUB_USERNAME) --password $(HUB_PASSWORD)
	poetry run python -m saltdocker --push
