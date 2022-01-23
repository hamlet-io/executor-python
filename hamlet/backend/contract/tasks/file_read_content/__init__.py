from hamlet.backend.common.exceptions import BackendException


def run(FilePath, env={}):
    """
    read the content of a given filepath and return it as the result
    """
    content = ""
    try:
        with open(FilePath, "r") as file:
            content = file.read()

    except FileNotFoundError as e:
        raise BackendException(str(e))

    return {"Properties": {"result": content}}
