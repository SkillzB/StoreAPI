# safe string comaprison to prevent encoding errors
from werkzeug.security import safe_str_cmp
from resources.user import User


def authenticate(username, password):
    # .get allows for setting a default value
    # username_mapping.get(username, None)
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)  # userid_mapping.get(user_id, None)
