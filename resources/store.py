import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from db import db
from sqlalchemy.exc import SQLAlchemyError

from schema import storeSchema
from models.stores import StoreModel

blp = Blueprint("Stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, storeSchema)
    def get(self, store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store

    @blp.response(200, storeSchema)
    def delete(self, store_id):
        store=StoreModel.query.get_or_404(store_id)
        
        db.session.delete(store)
        db.session.commit()
        return {"message":"store deleted"}

@blp.route("/store")
class StoreList(MethodView):
    @blp.arguments(storeSchema)
    @blp.response(201, storeSchema)
    def post(self,store_data):
        store =StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the store.")

        
        return store, 201
    @blp.response(200, storeSchema(many=True))
    def get(self):
        return StoreModel.query.all()
