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
	@ PYTHONDONTWRITEBYTECODE=1 flake8 --exit-zero --config=.flake8 cot tests setup.py

.PHONY: install
.ONESHELL:
install:
	pip uninstall codeontap-cli -y
	python setup.py bdist_wheel clean --all
	rm -rf codeontap_cli.egg-info
	pip install --no-index --find-links=dist codeontap-cli

.PHONY: uninstall
.ONESHELL:
uninstall:
	pip uninstall codeontap-cli -y
