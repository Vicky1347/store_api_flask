import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort,Blueprint 
from flask_jwt_extended import jwt_required
from schema import ItemUpdateSchema, ItemSchema

from models.item import ItemModel
from db import db

from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Items",__name__,description="Operations on items")

@blp.route("/item" )
class Item(MethodView):
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema) #not nesecerray but good to have
    def post(self,item_data):
        item=ItemModel(**item_data)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the item.")
        return item, 201
    


@blp.route("/item/<int:item_id>" )
class ItemDetail(MethodView):
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        item=ItemModel.query.get_or_404(item_id)
        return item
    
    def delete(self,item_id):
        item=ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"item deleted"}
        
        
    @blp.arguments(ItemUpdateSchema)
    def put(self,item_data,item_id):
        item=ItemModel.query.put(item_id)
        if item:
            item.price=item_data["price"]
            item.name=item_data["name"]
        else:
            item=ItemModel(id=item_id,**item_data)
        db.session.add(item)
        db.session.commit()
        return item
        
        
         