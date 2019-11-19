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
    name='codeontap-cli',
    version='0.1',
    packages=packages,
    install_requires=[
        'Click',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'cot=cot:command.root'
        ]
    },
    cmdclass={
        'install': InstallCommand
    }
)
