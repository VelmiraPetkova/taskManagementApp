from marshmallow import Schema, fields, validate, post_load
import uuid
from datetime import datetime

from backend.models.enums import TaskStatus
from backend.schemas.userSchema import UserSchema


class TaskSchema(Schema):
    id = fields.UUID(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = fields.String(validate=validate.Length(max=500))
    updated_on = fields.DateTime(required=False, allow_none=True)
    status = fields.String(
        required=False,
        validate=validate.OneOf(
            [role.value for role in TaskStatus],
            error="Invalid status type"
        )
    )
    user_id = fields.UUID(required=False, allow_none=True)

    @post_load
    def set_defaults(self, data, **kwargs):
        if 'updated_on' not in data or data['updated_on'] is None:
            data['updated_on'] = datetime.now()
        if 'status' not in data or not data['status']:
            data['status'] = TaskStatus.notStarted.name
        if 'user_id' not in data:
            data['user_id'] = None
        return data


