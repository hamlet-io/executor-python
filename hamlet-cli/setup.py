import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = find_packages(exclude=["tests.*", "tests"])


class InstallCommand(install):

    def __post_install(self, dir):
        subprocess.call(['./setup-autocomplete.sh'])

    def run(self):
        install.run(self)
        self.execute(
            self.__post_install,
            (self.install_lib,),
            msg='Setting up autocomplete...'
        )


setup(
    name='hamlet-cli',
    version='8.2.0-dev9',
    author='Hamlet',
    url="https://github.com/hamlet-io/executor-python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=packages,
    install_requires=[
        'click>=7.0.0,<8.0.0',
        'click-configfile>=0.2.3,<1.0.0',
        'pytest>=6.0.0,<7.0.0',
        'cookiecutter>=1.7.0,<2.0.0',
        'tabulate>=0.8.0,<1.0.0',
        'Jinja2>=2.11.0,<3.0.0',
        'cfn-lint>=0.25.0,<1.0.0',
        'cfn-flip>=1.2.0,<2.0.0',
        'diagrams>=0.18.0,<1.0.0',
        'marshmallow>=3.7.0,<4.0.0',
        'jmespath>=0.10.0<1.0.0',
        'importlib-resources>=5.1.2<6.0.0',
        'www-authenticate>=0.9.2<1.0.0',
        'requests>=2.25.1<3.0.0',

        # cfn-lint has issues with the latest networkx
        # Their requirements are installing the latest one
        'networkx==2.4;python_version>="3.5"',
    ],
    include_package_data=True,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'hamlet=hamlet:command.root'
        ]
    },
    cmdclass={
        'install': InstallCommand
    },
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Java',
        'Programming Language :: Python',
    ],
)
