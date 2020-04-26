import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install


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


print(packages)

setup(
    name='hamlet-cli',
    version='0.1.0',
    packages=packages,
    install_requires=[
        'click>=7.0.0,<8.0.0',
        'pytest>=5.0.0,<6.0.0',
        'cookiecutter>=1.6.0,<2.0.0',
        'tabulate>=0.8.0,<1.0.0',
        'Jinja2>=2.10.0,<3.0.0',
        'cfn-lint>=0.25.0,<1.0.0',
        'cfn-flip>=1.2.0,<2.0.0',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'hamlet=hamlet:command.root'
        ]
    },
    cmdclass={
        'install': InstallCommand
    }
)
