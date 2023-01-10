import os
import shutil
from zipfile import ZipFile, BadZipFile, LargeZipFile


def run(SourcePath, DestinationPath, env={}):
    """
    Create a zip of a given path and save to a destination
    If the source is a zip then just copy it
    """

    if os.path.isfile(SourcePath):
        create_zip = False
        try:
            source_zip = ZipFile(SourcePath, "r")
            source_zip.testzip()
        except (BadZipFile, LargeZipFile):
            create_zip = True

        if create_zip:
            with ZipFile(DestinationPath, "w") as zip:
                zip.write(SourcePath, os.path.basename(SourcePath))

        else:
            shutil.copyfile(SourcePath, DestinationPath)

    if os.path.isdir(SourcePath):
        shutil.make_archive(os.path.splitext(DestinationPath)[0], "zip", SourcePath)

    return {
        "Properties": {"source_path": SourcePath, "destination_path": DestinationPath}
    }
