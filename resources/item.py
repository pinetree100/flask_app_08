from multiprocessing import connection
from unittest import result
from flask_restful import Resource, reqparse
#from flask_jwt import jwt_required
from models.item import ItemModel
from sqlalchemy import desc,asc


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Price field cannot be left blank!"
    )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Store Id field cannot be left blank!"
    )

    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message':"An error occurred getting the item"}, 500      

        if item:
            return item.json()
        else:
            return{'message':'Item not found.'}, 404


    def post(self, name):
        data = Item.parser.parse_args()

        if ItemModel.find_by_name(name):
            return {'message':"An item with name '{}' already exists.".format(name)}, 400
        
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message':"An error occurred inserting the item"}, 500
        
        return item.json(), 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return{'message': 'Item deleted'}, 200
        else:
            return{'message': 'Item not found'}, 404
       
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except:
            return {'message':"An error occurred saving the item"}, 500 

        return item.json() 
        

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.order_by(asc(ItemModel.store_id)).all()]}