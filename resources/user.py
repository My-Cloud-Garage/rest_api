from flask_restful import Resource, reqparse
from models.user import UserModel as User

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Field Cannot be blank")
    parser.add_argument('password', type=str, required=True, help="Field Cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            return {"message": "username already exists!"}, 400

        user = User(**data)
        user.save_to_db()
        return {"message": "User created successfully"}, 201
