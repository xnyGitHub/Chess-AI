
ifeq ($(shell python3 --version 2> /dev/null),)
    PYTHON = python
else
    PYTHON = python3
endif

lint:
	$(PYTHON) -m black src tests
	$(PYTHON) -m pylint src tests
test:
	$(PYTHON) -m pytest -vv --cov=src --cov-report=term-missing --no-cov-on-fail
