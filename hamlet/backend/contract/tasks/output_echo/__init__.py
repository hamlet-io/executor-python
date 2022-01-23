import json
import click


def run(Value, Format, OutputStream, env={}):
    """
    echo a given value to an output stream
    """

    err = OutputStream == "stderr"
    if Format == "json":
        Value = json.dumps(json.loads(Value), indent=2)

    click.echo(Value, err=err)
    return {"Properties": {"result": Value}}
