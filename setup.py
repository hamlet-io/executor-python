import subprocess

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

with open("README.md", "r") as fh:
    long_description = fh.read()

about = {}
with open("hamlet/__about__.py", "r") as fp:
    exec(fp.read(), about)

packages = find_packages(exclude=["tests.*", "tests"])


class InstallCommand(install):
    def __post_install(self, dir):
        subprocess.call(["./setup-hamlet.sh"])

    def run(self):
        install.run(self)
        self.execute(
            self.__post_install, (self.install_lib,), msg="Setting up hamlet..."
        )


class DevelopCommand(develop):
    def __post_install(self, dir):
        subprocess.call(["./setup-hamlet.sh"])

    def run(self):
        develop.run(self)
        self.execute(
            self.__post_install, (self.install_lib,), msg="Setting up hamlet..."
        )


setup(
    name=about["__title__"],
    author=about["__author__"],
    url=about["__url__"],
    description=about["__summary__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    project_urls={"Repository": about["__repository_url__"]},
    packages=packages,
    setup_requires=["setuptools_scm>=6.0.1,<7.0.0"],
    use_scm_version={
        "root": "",
        "relative_to": __file__,
        "fallback_version": "_testing_",
        "write_to": "hamlet/__version__.py",
        "local_scheme": "no-local-version",
    },
    install_requires=[
        "click>=8.0.3,<9.0.0",
        "click-configfile>=0.2.3,<1.0.0",
        "cookiecutter>=1.7.0,<2.0.0",
        "tabulate>=0.8.0,<1.0.0",
        "Jinja2>=2.11.0,<3.0.0",
        "jmespath>=0.10.0,<1.0.0",
        "importlib-resources>=5.2.0,<6.0.0",
        "www-authenticate>=0.9.2,<1.0.0",
        "httpx>=0.19.0,<0.20.0",
        "marshmallow>=3.7.0,<4.0.0",
        # Template testing
        "pytest>=6.0.0,<7.0.0",
        # AWS testing dependencies
        "cfn-lint>=0.54.1,<1.0.0",
        # - boto3 locked to support checkov current requirements
        "checkov>=2.0.461,<3.0.0",
        "boto3>=1.17.111,<1.18.0",
        "botocore>=1.20.112,<2.0.0",
        # Diagrams
        "diagrams>=0.18.0,<1.0.0",
    ],
    include_package_data=True,
    python_requires=">=3.6",
    entry_points={"console_scripts": ["hamlet=hamlet:command.root"]},
    cmdclass={
        "install": InstallCommand,
        "develop": DevelopCommand,
    },
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Java",
        "Programming Language :: Python",
    ],
)
