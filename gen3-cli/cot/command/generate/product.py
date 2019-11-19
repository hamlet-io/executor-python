import os
from cookiecutter.main import cookiecutter
import click
from cot import conf


TEMPLATES_DIR = os.path.join(conf.COOKIECUTTER_TEMPLATES_BASE_DIR, 'products')


@click.group('product')
def group():
    pass


@group.command('base')
def generate_base():
    """
    This template is for the creation of a codeontap product.
    This creates a base product with no deployed components.
    This template should be run from the root of an empty product directory.
    """
    template_path = os.path.join(TEMPLATES_DIR, 'base')
    cookiecutter(template_path)


@group.command('app-lifecycle-mgmt')
def generate_app_lifecycle_mgmt():
    """
    This template is for the creation of a codeontap product.
    This product provisions a container based application lifecycle management service used
    to build and deploy codeontap managed applications.
    """
    template_path = os.path.join(TEMPLATES_DIR, 'app-lifecycle-mgmt')
    cookiecutter(template_path)


@group.command('django')
def generate_django():
    """
    This template is for the creation of an AWS based Django deployment. It includes all of the components
    required for a produciton level deployment of Django:

    - Web ECS Service for front end
    - Worker ECS Service for celery processing
    - Task ECS Task Definition for Django management
    - Postgres based RDS instance
    - Cloudfront S3 distribution for static content
    - Redis for queue management between web and worker
    - HTTPS offloading load balancer for web

    The template will create a single environment. If you want more you will need too add them manually.
    """
    template_path = os.path.join(TEMPLATES_DIR, 'django-cookiecutter')
    cookiecutter(template_path)
