from flask import request
from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message":"A store with name '{}' already exists.".format(name)}
        store = StoreModel(name)
        try:
            store.save_to_db()
            return store.json(), 201
        except Exception as msg:
            return {"message": "An error occured while creating the store. Error: {}".format(msg)}, 500

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "Store deleted"}, 200


class StoreList(Resource):
    def get(self):
        stores = StoreModel.query.all()
        all = [store.json() for store in stores]
        return {'stores': all}, 200
