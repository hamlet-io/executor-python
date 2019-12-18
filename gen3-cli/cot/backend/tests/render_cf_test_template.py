import json
from .templates_loader import loader


def __render_python_dict_path(json_path_str):
    dict_path_str = ""
    for part in json_path_str.split('.'):
        part = part.strip()
        try:
            dict_path_str += "[{}]".format(int(part))
        except ValueError:
            dict_path_str += "['{}']".format(part)
    return dict_path_str


def prepare_template_context(
    filename="",
    exists=None,
    match=None,
    resource=None,
    output=None,
    not_empty=None,
    length=None,
    no_vulnerability_check=False,
    no_lint=False
):
    exists = exists or []
    match = match or []
    resource = resource or []
    output = output or []
    not_empty = not_empty or []
    length = length or []

    context = dict(
        filename=filename,
        exists=[],
        match=[],
        resource=[],
        output=[],
        not_empty=[],
        length=[],
        no_vulnerability_check=no_vulnerability_check,
        no_lint=no_lint
    )

    for path in exists:
        context['exists'].append(
            {
                "path": __render_python_dict_path(path)
            }
        )
    for path, value in match:
        try:
            value = json.loads(value)
        except ValueError:
            value = "\"{}\"".format(value)
        context['match'].append(
            {
                "path": __render_python_dict_path(path),
                "value": value
            }
        )
    for name, type in resource:
        context['resource'].append(
            {
                'name': name,
                'type': type
            }
        )

    for name in output:
        context['output'].append(
            {
                'name': name
            }
        )

    for path in not_empty:
        context['not_empty'].append(
            {
                'path': __render_python_dict_path(path)
            }
        )

    for path, value in length:
        context['length'].append(
            {
                'path': __render_python_dict_path(path),
                'value': int(value)
            }
        )

    return context


def render(**kwargs):
    template = loader.get_template('cf_test.py.tmpl')
    context = prepare_template_context(**kwargs)
    return template.render(**context)
