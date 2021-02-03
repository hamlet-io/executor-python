from marshmallow import Schema, fields


class Entities(Schema):
    entityID = fields.String(required=True)
    groupID = fields.String(required=True)
    type = fields.String(required=True)
    entityName = fields.String(required=True)


class Relationships(Schema):
    startEntityID = fields.String(required=True)
    endEntityID = fields.String(required=True)
    direction = fields.String(required=True)


class Groups(Schema):
    groupID = fields.String(required=True)
    parentID = fields.String(required=True)


class Diagram(Schema):
    Metadata = fields.Raw()
    diagramName = fields.String(required=True)
    entities = fields.Nested(Entities(many=True))
    relationships = fields.Nested(Relationships(many=True))
    groups = fields.Nested(Groups(many=True))
