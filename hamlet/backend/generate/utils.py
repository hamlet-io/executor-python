import os
import shutil
import tempfile

from cookiecutter.main import cookiecutter as cookiecutter_main
from hamlet.backend.common.exceptions import BackendException

try:
    from importlib.resources import files, as_file
except (ImportError, ModuleNotFoundError):
    from importlib_resources import files, as_file


def extract_package_to_temp(package, tmp_dir, root_dir, package_dir):
    for entry in files(package).joinpath(package_dir).iterdir():
        entry_path = os.path.commonprefix([root_dir, entry])
        entry_path = str(entry).replace(entry_path, "").lstrip("/")

        if entry.is_dir():
            os.makedirs(os.path.join(tmp_dir, entry_path))
            extract_package_to_temp(package, tmp_dir, root_dir, entry_path)
        else:
            tmp_file = os.path.join(tmp_dir, entry_path)
            shutil.copyfile(entry, tmp_file)


def replace_parameters_values(kwargs, replacers=None):
    for key, value in kwargs.items():
        for target, replacer in replacers:
            if value is target or value == target:
                kwargs[key] = replacer
                break


def cookiecutter(template_package, output_dir, **kwargs):
    with tempfile.TemporaryDirectory() as template_dir:
        if files(template_package).joinpath("cookiecutter.json").is_file():
            with as_file(
                files(template_package).joinpath("cookiecutter.json")
            ) as package_path:
                extract_package_to_temp(
                    template_package, template_dir, os.path.dirname(package_path), ""
                )
        else:
            raise BackendException(
                f"Provided template package does not contain cookiecutter.json config: {template_package}"
            )

        replace_parameters_values(kwargs, [[None, ""], [True, "yes"], [False, "no"]])
        cookiecutter_main(
            template_dir, no_input=True, output_dir=output_dir, extra_context=kwargs
        )
