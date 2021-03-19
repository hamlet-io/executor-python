# Hamlet Deploy - Executor Python

This is a python-based CLI for the Hamlet Deploy application. It acts as the primary interface to Hamlet Deploy, its Plugins and Extensions.

See https://docs.hamlet.io for more info on Hamlet Deploy

## Installation

```bash
# Clone repository
git clone https://github.com/hamlet-io/executor-python

# install dependencies
cd ./executor-python

# optionally create a venv to isolate the package
python -m venv hamlet-cli/.venv
. hamlet-cli/.venv/bin/activate # If using windows see the venv activation process

pip install -e hamlet-cli
```

Hamlet Deploy CLI is now installed.

```bash
hamlet --help
```

## Update

```bash
# pull down changes
cd ./executor-python
git pull
```

With the latest files, re-run the installation steps to complete the update.

## Configuration

The Hamlet Deploy - Executor Python does not require specific configuration, however as it functions as a wrapper around other Hamlet Deploy parts, those must each be configured before using the CLI.

See the [Hamlet Deploy docs](https://docs.hamlet.io/docs/hamletdeploy/software/cli) site for more information.

## Usage

Usage of this provider requires the other parts of the Hamlet Deploy application.

It is recommended that you use the Hamlet Deploy container for this.

See https://docs.hamlet.io for more

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
    pip install -r requirements/dev.txt -r requirements/prod.txt

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
