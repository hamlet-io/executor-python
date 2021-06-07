# Hamlet Deploy - Executor Python

This is a CLI interface for [Hamlet Deploy](https://docs.hamlet.io). Using the cli you can manage your hamlet deployments including creating CMDBs, managing deployments and finding out about what you have deployed.

## Using the Cli

This README outlines how you can develop the cli. If you would like to just get in and start using hamlet head to the [CLI Readme](./hamlet-cli/README.md).

---

## Development

There are two development approaches for working in this repo

- Isolated: creates a complete isolated dev environment using a local docker image
- Integrated: uses an existing hamlet workspace ( this is useful for working on your own CMDBS )

### Isolated Process

#### Requirements

You just need to install requirements:

- ```docker```
- ```docker-compose```
- ```make```

#### Build

Build the Python Executor into a docker container

```bash
make build
```

#### Run

Build and then run the Executor Python in a docker container

The container image built will be tagged as `hamlet-cli`

```bash
# in the background
make run

# in the foreground
make run-fg

# start a terminal session inside a running container
make shell
```

#### Install

Once you are inside the built container

```bash
# install common tooling & Hamlet Deploy
make install
```

#### Clean Up

Clear the local development environment build data

```bash
make clean
```

### Integrated Process

You will need an existing hamlet workspace with `python` and `make` available ( the hamletio/hamlet docker container comes with these )

1. Clone this repo into your workspace ( feel free to change the directory to what you need )

    ```bash
    git clone https://github.com/hamlet-io/executor-python hamlet/executor/python
    ```

2. Hop into the executor clone location and setup a python venv

    ```bash
    cd hamlet/executor/python/hamlet-cli
    python -m venv .venv
    . .venv/bin/activate

    # install requirements
    pip install -r requirements/dev.txt

    # Install the hamlet-cli into the venv in edit mode
    pip install -e hamlet-cli
    ```

When calling hamlet from within the venv the development installation will be used instead of the workspace installation

To use the workspace installation again deactivate the venv

```bash
deactivate
```

### Development tasks

Once you have setup the hamlet-cli the following make commands are available from the hamlet-cli directory in this repo

```bash
# create test coverage report
make coverage

# test the project (no coverage report)
make tests

# python linter
make link
```
