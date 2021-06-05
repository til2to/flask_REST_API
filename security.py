from models.user import UserModel


def authenticate(username, password): 
    _user = UserModel.find_by_username(username)
    if _user and _user.password == password:
        return _user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)