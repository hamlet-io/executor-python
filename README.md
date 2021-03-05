# Hamlet Deploy - Executor Python

This is a python-based CLI for the Hamlet Deploy application. It acts as the primary interface to Hamlet Deploy, its Plugins and Extensions.

See https://docs.hamlet.io for more info on Hamlet Deploy

### Installation

```bash
# Clone repository
git clone https://github.com/hamlet-io/executor-python

# install dependencies
cd ./executor-python/hamlet-cli
pip install -r ./requirements/prod.txt -r ./requirements/dev.txt

# install
make install
```

Hamlet Deploy CLI is now installed.

```bash
hamlet --help
```

### Configuration

The Hamlet Deploy - Executor Python does not require specific configuration, however as it functions as a wrapper around other Hamlet Deploy parts, those must each be configured before using the CLI.

See the [Hamlet Deploy docs](https://docs.hamlet.io/docs/hamletdeploy/software/cli) site for more information.

### Update

```bash
# pull down changes
cd ./executor-python
git pull
```

With the latest files, re-run the installation steps to complete the update.
### Usage

Usage of this provider requires the other parts of the Hamlet Deploy application. 

It is recommended that you use the Hamlet Deploy container for this.

See https://docs.hamlet.io for more

---

## Development

The follow sections outline how to create a local development environment for the Executor Python.
### Requirements
You just need to install requirements:
- ```docker```
- ```docker-compose```
- ```make```

### Build

Build the Python Executor into a docker container

```bash
make build
```
### Run

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

### Develop

Inside of the container, the following commands are available to help development

```bash
# install common tooling & Hamlet Deploy
make install

# create test coverage report
make coverage

# test the project (no coverage report)
make tests

# python linter
make link
```

### Clean Up

Clear the local development environment build data

```bash
make clean
```
