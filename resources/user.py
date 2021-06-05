from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser() 
    parser.add_argument('username',
        type=str,
        required=True, #ensures no request comes through without price
        help="this field cannot be left blank"
    ) # define the argument and add other informaton
    
    parser.add_argument('password',
        type=str,
        required=True, #ensures no request comes through without price
        help="this field cannot be left blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args() 
        try:
            if UserModel.find_by_username(data['username']):
                return {'message':'username {} already exists'.format(data['username'])}, 201

            user = UserModel(**data) #Since the arguments are all dictionaries, can unpack them
            # for each of the keys in data, username=data['username'] and password=data['password]
            try:
                user.save_to_db()
            except:
                return {'message':'item not saved'}
    
            return {'message':'user created successfully.'}, 201
        except Exception as e:
            return str(e), 500 
        