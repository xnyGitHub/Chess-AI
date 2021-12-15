lint:
	python -m black src
	python -m black tests
	python -m pylint src
	python -m pylint test
test:
	python -m pytest tests -v