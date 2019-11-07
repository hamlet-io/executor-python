.PHONY: test
.ONESHELL:
test:
	@ pytest tests -vv -x

.PHONY: coverage
.ONESHELL:
coverage:
		coverage run -m tests
		coverage report -m
		coverage html

.PHONY: lint
.ONESHELL:
lint:
	PYTHONDONTWRITEBYTECODE=1 flake8 src tests setup.py

.PHONY: install
.ONESHELL:
install:
	pip uninstall codeontap-cli -y
	python setup.py bdist_wheel clean --all
	rm -rf codeontap_cli.egg-info
	pip install --no-index --find-links=dist codeontap-cli
