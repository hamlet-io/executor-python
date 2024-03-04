import pathlib


def run(FilePath, env={}):
    """
    remove a file if it is a file and exists
    """
    file_path = pathlib.Path(FilePath)

    if file_path.is_file() and file_path.exists():
        file_path.unlink()

    return {
        "Properties": {
        }
    }
