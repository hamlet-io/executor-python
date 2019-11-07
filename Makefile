.PHONY: clean
.ONESHELL:
clean:
	@ docker-compose down --rmi all --volumes

.PHONY: run
.ONESHELL:
run:
	@ docker-compose up --build --remove-orphans -d

.PHONY: run-fg
.ONESHELL:
run-fg:
	@ docker-compose up --build --remove-orphans

.PHONY: build
.ONESHELL:
build:
	@ docker-compose build --no-cache

.PHONY: ssh-gen3-cli
.ONESHELL:
ssh-gen3-cli:
	@ docker-compose exec gen3-cli /bin/bash
