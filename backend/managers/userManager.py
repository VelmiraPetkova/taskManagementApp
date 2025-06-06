from werkzeug.exceptions import BadRequest, NotFound

from backend.models.user import UserModel


class UserManager:
    """It is used to check the user from the request if it exists"""
    @staticmethod
    def _verify_user(user_id):
        try:
            user = UserModel.query.get(user_id)
        except (BadRequest, NotFound):
            raise BadRequest('No such user found')

        return user


    @staticmethod
    def get_users():
        return UserModel.query.all()