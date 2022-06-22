import tempfile


def run(env={}):
    """
    Create a temporary directory and return the path to the directory
    """

    return {"Properties": {"path": tempfile.mkdtemp()}}
