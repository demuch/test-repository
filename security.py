from resources.user import UserRegister
from models.user import UserModel


def authentictate(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user

#The identity function is used when we receive a JWT
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
