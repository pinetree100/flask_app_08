import os

from flask import Flask
from flask_restful import Api
#from db import db

#here should be the imports from JWT but the thing doesn't work...
#from resource.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'pass'
api = Api(app)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

#api.add_resource(UserRegister, '/register')
#to protect from import impositions

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    
    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
            
    app.run(port=5000)
