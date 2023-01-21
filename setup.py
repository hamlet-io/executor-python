from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

about = {}
with open("hamlet/__about__.py", "r") as fp:
    exec(fp.read(), about)

packages = find_packages(exclude=["tests.*", "tests"])

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
    setup_requires=["setuptools_scm>=7.1.0,<8.0.0"],
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
        "cookiecutter>=2.1.1,<3.0.0",
        "tabulate>=0.8.0,<1.0.0",
        "Jinja2>=3.0.3,<4.0.0",
        "jmespath>=0.10.0,<1.0.0",
        "www-authenticate>=0.9.2,<1.0.0",
        "httpx>=0.21.2,<1.0.0",
        "marshmallow>=3.7.0,<4.0.0",
        "dulwich>=0.20.45,<1.0.0",
        "semver>=2.13.0,<3.0.0",
        "importlib_resources>=5.10.2,<6.0.0",
        # contract execution
        "boto3>=1.20.0,<2.0.0",
        "botocore>=1.20.0,<2.0.0",
        "fabric>=2.6.0,<3.0.0",
        "simple-term-menu>=1.4.1,<2.0.0",
        "docker>=5.0.3,<6.0.0",
        # Template testing
        "pytest>=6.0.0,<7.0.0",
    ],
    extras_require={
        "dev": [
            "coverage",
            "freezegun",
            "setuptools",
            # formatting
            "flake8",
            "black",
            # packaging
            "build",
            "wheel",
            "twine",
            # Docs
            "Sphinx",
            "sphinx-markdown-builder",
            "sphinx-click",
        ],
    },
    include_package_data=True,
    python_requires=">=3.7",
    entry_points={"console_scripts": ["hamlet=hamlet:command.root"]},
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Java",
        "Programming Language :: Python",
    ],
)
