from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError

from backend.utils.decorators import validate_schema

from backend.managers.auth import AuthManager
from backend.schemas.userSchema import UserSchema, UserBase

from backend.schemas.userSchema import UserAuthResponseSchema

class UserRegisterResource(Resource):
    @validate_schema(UserSchema)
    def post(self):
        data = request.get_json()
        try:
            user = AuthManager.create_user(data)
            token= AuthManager.encode_token(user)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        res = UserAuthResponseSchema().dump({"token": token})
        return res

class UserLoginResource(Resource):
    @validate_schema(UserBase)
    def post(self):
        data = request.get_json()
        user = AuthManager.login_user(data)
        token= AuthManager.encode_token(user)
        return UserAuthResponseSchema().dump({"token": token})