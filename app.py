from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWT(app, authenticate, identity)


@app.before_first_request #Before the first request runs, the function below runs
def create_tables():
  db.create_all()
  db.session.commit()


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    from run import db
    db.init_app(app)
    app.run(port=5000, debug=True)