
ifeq ($(shell python3 --version 2> /dev/null),)
    PYTHON = python
else
    PYTHON = python3
endif

lint:
	$(PYTHON) -m black src
	$(PYTHON) -m black tests
	$(PYTHON) -m pylint src
	$(PYTHON) -m pylint test
test:
	$(PYTHON) -m pytest tests -v
