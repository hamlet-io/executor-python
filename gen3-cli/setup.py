from setuptools import setup, find_packages

packages = find_packages(exclude=["tests.*", "tests"])

print(packages)

setup(
    name='codeontap-cli',
    version='0.1',
    packages=packages,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'cot=cot:command.root'
        ]
    }
)
