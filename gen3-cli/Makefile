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
