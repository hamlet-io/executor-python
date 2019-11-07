from setuptools import setup


setup(
    name='cli',
    version='0.1',
    packages=['src'],
    package_dir={
        'src': 'src'
    },
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'cli=src.cli:root'
        ]
    }
)
