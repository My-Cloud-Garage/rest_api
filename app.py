from flask import Flask
#from flask_restplus import Resource, Api
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
# headers = {'Content-type': 'application/json'}
#from flask_restfulplus import Resource, Api
# headers = {'user-agent': 'my-app/0.0.1'}
# s.headers.update({'x-test': 'true'})
# s.get('http://httpbin.org/headers', headers={'x-test2': 'true', 'Content-Type':'application/json' })
# curl -i -H "Content-Type: application/json" -X POST -d '{"userId":"1", "username": "fizz bizz"}' http://localhost:5000/foo

# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjA2MTM2NDksImlhdCI6MTU2MDYxMzM0OSwibmJmIjoxNTYwNjEzMzQ5LCJpZGVudGl0eSI6IjEifQ.NxoVIuxBvvLyWvUADL0Cm1sF4Q9ucVdcitqRKXJK6HI

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key ='jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, port=5000)
