# Development

You will need an existing hamlet workspace with Python (3.6 or higher) and make available

1. Clone this repo into your workspace ( feel free to change the directory to what you need )

    ```bash
    git clone https://github.com/hamlet-io/executor-python hamlet/executor/python
    ```

2. Hop into the executor clone location and setup a python venv

    ```bash
    cd hamlet/executor/python
    python -m venv .venv
    . .venv/bin/activate

    # Install the hamlet into the venv in edit mode
    pip install -e .

    # Add the dev packages
    pip install hamlet[dev]
    ```

3. To confirm that the local installation is being used

    ```bash
    hamlet --version
    hamlet, version 9.14.2.dev0
    ```

    If the version ends in dev0, the local installation is active

:::Note
If a new version of the engine is released and you install it using pip install hamlet into the current venv. You need to rerun the local installation.
The local version will have a lower version number than the published version
:::

When calling hamlet from within the venv the development installation will be used instead of the workspace installation

To use the workspace installation again deactivate the venv

```bash
deactivate
```

## Development tasks

Once you have setup the hamlet the following make commands are available from the hamlet directory in this repo

```bash
# create test coverage report
make coverage

# test the project (no coverage report)
make tests

# python linter
make lint

# code formatting
make format
```
