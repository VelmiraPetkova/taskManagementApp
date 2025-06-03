from flask import request
from flask_restful import Resource

from backend.utils.decorators import validate_schema
from db import db


from backend.managers.auth import AuthManager
from backend.schemas.userSchema import UserSchema, UserBase

from backend.schemas.userSchema import UserAuthResponseSchema


class UserRegisterResource(Resource):
    @validate_schema(UserSchema)
    def post(self):
        data = request.get_json()
        user = AuthManager.create_user(data)
        token= AuthManager.encode_token(user)
        return UserAuthResponseSchema().dump({"token": token})
        #return UserOutSchema().dump(user), 201


class UserLoginResource(Resource):
    @validate_schema(UserBase)
    def post(self):
        data = request.get_json()
        user = AuthManager.login_user(data)
        token= AuthManager.encode_token(user)
        return UserAuthResponseSchema().dump({"token": token})