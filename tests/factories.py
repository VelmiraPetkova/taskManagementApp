import factory
from werkzeug.security import generate_password_hash

from backend.models.user import UserModel
from backend.models.enums import UserRole
from db import db



class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.commit()
        return object


class UserFactory(BaseFactory):
    class Meta:
        model = UserModel

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.LazyFunction(lambda: generate_password_hash("correctpass"))
    role = UserRole.employee

def get_user_id():
    return UserFactory.id
