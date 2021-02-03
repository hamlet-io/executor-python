import os
import json
from marshmallow import ValidationError
from hamlet.backend.common.exceptions import UserFriendlyBackendException
from .render import create_script
from .diagram_schema import Diagram as DiagramSchema


DIAGRAM_OUTPUT_PREFIX = 'diagram'
DIAGRAM_CONFIG_OUTPUT_SUFFIX = '-config.json'
DIAGRAM_SCRIPT_OUTPUT_SUFFIX = '-script.py'
DIAGRAM_IMAGE_OUTPUT_SUFFIX = '-digaram.png'


def run(
    filename=None,
    directory=None,
    output_dir=None,
    type=None
):
    filename = ''
    diagram_prefix = f'{DIAGRAM_OUTPUT_PREFIX}-{type}-'

    # searching testcase files in given directory if no files provided
    if not filename and directory:
        if not type:
            raise UserFriendlyBackendException('Diagram type required if using directory search')

        for name in os.listdir(directory):
            if name.startswith(diagram_prefix) and name.endswith(DIAGRAM_CONFIG_OUTPUT_SUFFIX):
                filename = os.path.join(directory, name)
    # if after all no files found raise an error
    if not filename:
        raise UserFriendlyBackendException('No diagram file found')

    diagram = dict()
    with open(filename, 'rt') as f:
        diagram_file_data = json.load(f)
        try:
            DiagramSchema().load(diagram_file_data)
        except ValidationError as e:
            message = json.dumps(e.messages, indent=4)
            raise UserFriendlyBackendException(
                f"Invalid diagram schema in {filename}\n\nErrors: \n{message}"
            ) from e
        diagram.update(**diagram_file_data)

    # if files have no diagrams data
    if not diagram:
        raise UserFriendlyBackendException('No diagram found!')

    # Create outputs
    script_file_path = os.path.join(output_dir, filename.replace(DIAGRAM_CONFIG_OUTPUT_SUFFIX, DIAGRAM_SCRIPT_OUTPUT_SUFFIX))
    image_file_path = os.path.join(output_dir, filename.replace(DIAGRAM_CONFIG_OUTPUT_SUFFIX, DIAGRAM_IMAGE_OUTPUT_SUFFIX))

    text = create_script(diagram, image_file_path, script_file_path)
    if text is not None:
        with open(script_file_path, 'w+t') as f:
            f.write(str(text))
    exec(text)
    return text
