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

.PHONY: install
.ONESHELL:
install:
	rm -rf dist
	pip uninstall hamlet-cli -y
	python setup.py sdist clean --all
	rm -rf hamlet_cli.egg-info
	pip install --no-index --find-links=dist hamlet-cli

.PHONY: uninstall
.ONESHELL:
uninstall:
	pip uninstall hamlet-cli -y
