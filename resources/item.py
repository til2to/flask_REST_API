from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser() #only initializes a new object
    #can also use this request parser for forms in html 

    parser.add_argument('price',
    type=float,
    required=True,
    help='this field cannot be left blank'
     )

    parser.add_argument('store_id',
    type=int,
    required=True,
    help='every item needs a store id to belong ro a particular store'
     )

    @jwt_required()
    def get(self, name): 
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'item is not found'}, 404

    def post(self, name):
        try:
            if ItemModel.find_by_name(name): 
                return {'message':'item {} already exists'.format(name)}, 400

            data = Item.parser.parse_args()
            #data = request.get_json()

            item = ItemModel(name, data['price'], data['store_id'])

            try:
                item.save_to_db() #insert()
            except:
                return {'message':'item failed to insert'}, 500 

            return item.json(), 201
        except Exception as e:
            return str(e), 500 

    def delete(self, name): 

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
         
        return {'message':'item deleted'}


    def put(self, name):
       
        data = Item.parser.parse_args()  # is gonna parse the arguments that comes through the json payload
        #data = request.get_json()

        item = ItemModel.find_by_name(name)
       
        if item is None:              
            item = ItemModel(name, data['price'], data['store_id']), 400 #we create a new one since the item by name is not found
  
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
           
        return item.json()


class ItemList(Resource):
    def get(self): #get all the items available
        #return {'items': ItemModel.query.All()} # Returns all the objects in the DB
        return {'items':[item.json() for item in ItemModel.query.all()]}
        