from marshmallow import Schema, fields


class CFNStructure(Schema):
    class Resource(Schema):
        id = fields.Str(required=True)
        type = fields.Str(required=True)

    class Output(Schema):
        id = fields.Str(required=True)

    resource = fields.List(fields.Nested(Resource))
    output = fields.List(fields.Nested(Output))


class JSONStructure(Schema):
    class Match(Schema):
        path = fields.Str(required=True)
        value = fields.Raw(required=True)

    class Exists(Schema):
        path = fields.Str(required=True)

    class Length(Schema):
        path = fields.Str(required=True)
        value = fields.Integer(required=True, strict=True)

    class NotEmpty(Schema):
        path = fields.String(required=True)

    match = fields.List(fields.Nested(Match))
    exists = fields.List(fields.Nested(Exists))
    length = fields.List(fields.Nested(Length))
    not_empty = fields.List(fields.Nested(NotEmpty))


class CheckovStructure(Schema):
    framework = fields.Str()
    skip_checks = fields.List(fields.Str())


class CFNLintStructure(Schema):
    ignore_checks = fields.List(fields.Str())


class Testcase(Schema):
    filename = fields.Str(required=True)
    cfn_lint = fields.Nested(CFNLintStructure)
    checkov = fields.Nested(CheckovStructure)
    cfn_structure = fields.Nested(CFNStructure)
    json_structure = fields.Nested(JSONStructure)
