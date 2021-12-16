
ifeq ($(shell python3 --version 2> /dev/null),)
    PYTHON = python
else
    PYTHON = python3
endif

lint:
	python -m black src
	python -m black tests
	python -m pylint src
	python -m pylint test
test:
	python -m pytest tests -v