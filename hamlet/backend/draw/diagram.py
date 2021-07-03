import os
import json
from marshmallow import ValidationError
from hamlet.backend.common.exceptions import BackendException
from .render import create_script
from .diagram_schema import Diagram as DiagramSchema


DIAGRAM_OUTPUT_PREFIX = "diagram"
DIAGRAM_CONFIG_OUTPUT_SUFFIX = "-config.json"
DIAGRAM_SCRIPT_OUTPUT_SUFFIX = "-script.py"
DIAGRAM_IMAGE_OUTPUT_SUFFIX = ".png"


def run(
    diagram_id,
    src_dir,
    output_dir,
):
    file_path = ""
    diagram_prefix = f"{DIAGRAM_OUTPUT_PREFIX}-{diagram_id}-"

    for name in os.listdir(src_dir):
        if name.startswith(diagram_prefix) and name.endswith(
            DIAGRAM_CONFIG_OUTPUT_SUFFIX
        ):
            file_path = os.path.join(src_dir, name)

    # if after all no files found raise an error
    if not file_path:
        raise BackendException("No diagram file found")

    diagram = dict()
    with open(file_path, "rt") as f:
        diagram_file_data = json.load(f)
        try:
            DiagramSchema().load(diagram_file_data)
        except ValidationError as e:
            message = json.dumps(e.messages, indent=4)
            raise BackendException(
                f"Invalid diagram schema in {file_path}\n\nErrors: \n{message}"
            ) from e
        diagram.update(**diagram_file_data)

    # if files have no diagrams data
    if not diagram:
        raise BackendException("No diagram found!")

    # Create outputs
    script_file_path = file_path.replace(
        DIAGRAM_CONFIG_OUTPUT_SUFFIX, DIAGRAM_SCRIPT_OUTPUT_SUFFIX
    )
    image_file_path = os.path.join(
        output_dir,
        os.path.basename(file_path).replace(
            DIAGRAM_CONFIG_OUTPUT_SUFFIX, DIAGRAM_IMAGE_OUTPUT_SUFFIX
        ),
    )

    text = create_script(
        diagram=diagram, temp_path=script_file_path, image_filename=image_file_path
    )
    if text is not None:
        with open(script_file_path, "w+t") as f:
            f.write(str(text))
    exec(text)
    return text
