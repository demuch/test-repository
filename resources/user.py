import sqlite3
from flask_restful import Resource, Api, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type = str,
                        required = True,
                        help = "This field cannot be blank!")

    parser.add_argument('password',
                        type = str,
                        required = True,
                        help = "This field cannot be blank!")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return{'massage': "The username is already exists!"}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"massage": "User created successfully!"}, 201 #201 is created
