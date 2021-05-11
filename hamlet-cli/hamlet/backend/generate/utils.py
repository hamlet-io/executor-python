import os
import shutil
import tempfile
import importlib_resources

from cookiecutter.main import cookiecutter as cookiecutter_main
from hamlet.backend.common.exceptions import BackendException


def extract_package_to_temp(package, tmp_dir, root_dir, package_dir):
    for entry in importlib_resources.files(package).joinpath(package_dir).iterdir():
        entry_path = os.path.commonprefix([root_dir, entry])
        entry_path = str(entry).replace(entry_path, '').lstrip('/')

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

        if importlib_resources.is_resource(template_package, 'cookiecutter.json'):
            cookiecutter_path = importlib_resources.path(template_package, 'cookiecutter.json')
            package_root_dir = os.path.dirname(cookiecutter_path)

            extract_package_to_temp(template_package, template_dir, package_root_dir, '')
        else:
            raise BackendException(
                f'Provided template package does not contain cookiecutter.json config: {template_package}'
            )

        replace_parameters_values(
            kwargs,
            [
                [None, ''],
                [True, 'yes'],
                [False, 'no']
            ]
        )
        cookiecutter_main(
            template_dir,
            no_input=True,
            output_dir=output_dir,
            extra_context=kwargs
        )
