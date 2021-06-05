from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name()
        if store:
            return store.json()
        return {'message':'store name not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name:
            return {'store with {} already exist'.format(name)}, 400
        
        data = request.get_json()
        
        store = StoreModel(name, data['store_id']) # create a new store since it doesnt exist at this stage
        try:
            store.save_to_db()
        except:
            return {'message': 'an error occured'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'store name {} deleted'.format(name) }, 404


class StoreList(Resource):
    def get(self):
        return {'items':[store.json() for store in StoreModel.query.all()]} # Where each store from the stores has to be in it own json