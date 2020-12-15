from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema


class ServiceSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    pet = fields.String(validate=[validate.Length(max=200)])
    service = fields.String(validate=[validate.Length(max=200)])
    is_publish = fields.Boolean(dump_only=True)

    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data
