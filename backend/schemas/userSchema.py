from marshmallow import Schema, fields, validate

from backend.models.enums import UserRole


class UserBase(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=100))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))


class UserSchema(UserBase):
    id = fields.Method("get_id", dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=255))
    role = fields.String(
        required=False,
        validate=validate.OneOf([role.value for role in UserRole], error="Invalid user role")
    )

    def get_id(self, obj):
        return str(obj.id)

class UserAuthResponseSchema(Schema):
    token = fields.Str(required=True)


