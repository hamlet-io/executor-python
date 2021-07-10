.PHONY: tests
.ONESHELL:
tests:
	@ pytest tests -vv -x -c pytest.ini

.PHONY: coverage
.ONESHELL:
coverage:
		coverage run -m tests
		coverage report -m
		coverage html

.PHONY: lint
.ONESHELL:
lint:
	@ PYTHONDONTWRITEBYTECODE=1 flake8 --exit-zero --config=.flake8 hamlet tests setup.py

.PHONY: format
.ONESHELL:
format:
	@ PYTHONDONTWRITEBYTECODE=1 black hamlet tests setup.py

.PHONY: install
.ONESHELL:
install:
	pip uninstall hamlet -y
	pip install -e /hamlet

.PHONY: uninstall
.ONESHELL:
uninstall:
	pip uninstall hamlet -y
