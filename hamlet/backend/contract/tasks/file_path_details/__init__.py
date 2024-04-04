import pathlib


def run(FilePath, env={}):
    """
    read the content of a given filepath and return it as the result
    """
    file_path = pathlib.Path(FilePath)

    return {
        "Properties": {
            "exists": str(file_path.exists()),
            "directory": str(file_path.is_dir()),
            "file": str(file_path.is_file()),
        }
    }
