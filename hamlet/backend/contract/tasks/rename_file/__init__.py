import shutil


def run(currentFileName, newFileName, env={}):
    """
    rename a file by moving it between two locations
    """

    shutil.move(currentFileName, newFileName)

    return {"Properties": {}}
