# Hamlet Deploy - CLI

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![release workflow](https://github.com/hamlet-io/executor-python/actions/workflows/release.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/hamlet.svg)](https://badge.fury.io/py/hamlet)

Hamlet deploy is a tool to manage infrastructure throughout the life of your application. With hamlet you define the functional components of your application along with the context they should be run in. The context includes things like environments, tenants, and policies that can be applied across all of your different applications.
From this information hamlet then creates the infrastructure that will perform the function you have asked for and manages it over the life of your application.

## Support

Hamlet deploy is built on a plugin based approach so you can create infrastructure for any provider you want, we provide an API of common processes and tasks for provisioning and describing infrastructure which allows you to build a common language across different infrastructure providers

We also provide official plugins for:

- Amazon Web Services (AWS) based on CloudFormation
- Microsoft Azure based on Azure Resource Manager
- mingrammer Diagrams for generating diagrams of your deployed infrastructure

## Docs

To read more about hamlet and what it can do head to our docs site https://docs.hamlet.io/

## Installation

Hamlet Deploy is made up of a couple of parts:

- engine - The engine is the core of hamlet and defines how infrastructure is deployed along with understanding the context of your application defined in a CMDB. The engine creates contracts and supporting documents which describes a task to complete. The engine is a java based app using the freemarker template engine.
- executor - The executor providers the user interface to hamlet along with executing the contracts provided by the engine. This is a mix of bash scripts and python code ( this cli )

### Docker Image

This guide takes you through installing the cli on your own machine and includes the OS packages that are required. We also offer a docker image which includes the hamelt cli along with a suite of tools to use the image as a general purpose CI/CD environment

The image is available on Dockerhub - https://hub.docker.com/r/hamletio/hamlet

### Prerequisites

Before using the cli a few OS level requirements need to be installed. This process differs from OS to OS so we are just including the packages and the websites if they are available. The packages need to be available on the PATH of your cli

#### Minimum

These packages will give you base access to start using hamlet

| Name     | Install Link                                 | Version           |
|----------|----------------------------------------------|-------------------|
| Java     | https://openjdk.java.net/install/            | 8 (1.8) required  |
| Jq       | https://stedolan.github.io/jq/               | 1.6 and above     |
| dos2unix | http://dos2unix.sourceforge.net/             | Any version       |
| Bash     | https://www.gnu.org/software/bash/           | 4.0 and above     |
| Python   | https://www.python.org/about/gettingstarted/ | 3.6 and above     |

All of these packages should be available through linux OS based package managers ( apt-get, yum etc ) and would be the recommended install approach

#### Optional Packages

The optional packages depend on what you want to do with hamlet

| Name     | Install Link                                 | Version                  | Purpose                  |
|----------|----------------------------------------------|--------------------------|--------------------------|
| Docker   | https://www.docker.com/get-started           | No specific requirements | Container deployments    |
| AWS Cli  | https://aws.amazon.com/cli/                  | v1 Currently Supported   | AWS deployments          |
| Az       | https://docs.microsoft.com/en-us/cli/azure/  | No specific requirements | Azure deployments        |
| Graphviz | https://graphviz.org/                        | No specific requirements | Diagram generation       |

See the websites for each package for these ones, but they should also be available through OS package manages or language specific managers ( aws cli and az are both available through pypi)

### Cli Install

Once you've got the prereqs installed the rest of hamlet is installed through the cli

To install the hamlet cli/executor use the python package manager pip

```bash
pip install hamlet
```

If you want the latest changes that are in development we publish all commits as pre-releases

```bash
pip install --pre hamlet
```

**Note** These builds can be unstable and aren't recommended for production usage

To confirm the install has worked

```bash
hamlet --help
```

Should return something like this

```bash
hamlet --help
Usage: hamlet [OPTIONS] COMMAND [ARGS]...

  hamlet deploy
```

And that's it, to see what you can do head to our docs https://docs.hamlet.io
