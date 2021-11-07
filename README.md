# hamlet - CLI

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![release workflow](https://github.com/hamlet-io/executor-python/actions/workflows/release.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/hamlet.svg)](https://badge.fury.io/py/hamlet)

hamlet is a tool to manage infrastructure throughout the life of your application. With hamlet you define the functional components of your application along with the context they should be run in. The context includes things like environments, tenants, and policies that can be applied across all of your different applications.
From this information hamlet then creates the infrastructure that will perform the function you have asked for and manages it over the life of your application.

This repository contains the CLI for hamlet which acts as the primary interface for hamlet.

## Support

hamlet is built on a plugin based approach so you can create infrastructure for any provider you want, we provide an API of common processes and tasks for provisioning and describing infrastructure which allows you to build a common language across different infrastructure providers

We also provide official plugins for:

- Amazon Web Services (AWS) based on CloudFormation
- Microsoft Azure based on Azure Resource Manager
- mingrammer Diagrams for generating diagrams of your deployed infrastructure

## Docs

To read more about hamlet and what it can do head to our docs site https://docs.hamlet.io/

## Installation

To run hamlet some extra dependencies are required. Head over to the [hamlet install guide](https://docs.hamlet.io/getting-started/install) for details installing hamlet
