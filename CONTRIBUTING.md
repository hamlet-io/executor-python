# Development

You will need an existing hamlet workspace with `python` and `make` available ( the hamletio/hamlet docker container comes with these )

1. Clone this repo into your workspace ( feel free to change the directory to what you need )

    ```bash
    git clone https://github.com/hamlet-io/executor-python hamlet/executor/python
    ```

2. Hop into the executor clone location and setup a python venv

    ```bash
    cd hamlet/executor/python/hamlet
    python -m venv .venv
    . .venv/bin/activate

    # install requirements
    pip install -r requirements/dev.txt

    # Install the hamlet into the venv in edit mode
    pip install -e hamlet
    ```

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
