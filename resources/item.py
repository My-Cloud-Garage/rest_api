from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float, required=True, help='Cannot be left blank!')
    parser.add_argument('store_id',type=int, required=True, help='Every item needs a store id')
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'msg': "An item with name '{}' already exists." .format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        # item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured"}, 500
        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'msg': name +' successfully deleted from items list'}, 200
        else:
            return {'msg': name + ' not in items list'}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item == None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        all = [i.json() for i in items]
        return {'items': all}, 200
