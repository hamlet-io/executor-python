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


.PHONY: install
.ONESHELL:
install:
	pip uninstall cli -y
	python setup.py bdist_wheel clean --all
	rm -rf cli.egg-info
	pip install --no-index --find-links=dist cli
