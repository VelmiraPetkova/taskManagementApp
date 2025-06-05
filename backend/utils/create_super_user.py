from werkzeug.security import generate_password_hash

from backend.models.enums import UserRole
from backend.models.user import UserModel
from db import db



def create_super_user(name, email, password):
    password = generate_password_hash(password)
    user = UserModel(name=name,
                     email=email,
                     password= password,
                     role= UserRole.superUser
                     )
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    #TODO: add values to be fetched from terminal
    create_super_user()