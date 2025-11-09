import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from db import db
from sqlalchemy.exc import SQLAlchemyError

from schema import storeSchema, TagSchema
from models.stores import StoreModel
from models.tag import tagModel
from models.tag import tagModel

blp = Blueprint("Tags", __name__, description="Operations on Tags")

@blp.route("/store/<int:store_id>/tag")
class TagInStore(MethodView):
    @blp.response(200, storeSchema(many=True))
    def get(self, store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self,tag_data, store_id):
        tag =tagModel(**tag_data,store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the tag.")
        return tag, 201
    
@blp.route("/tag/<int:tag_id>/store/<string:store_id>")
class LinkTagToStore(MethodView):
    @blp.response(200, TagSchema)
    def post(self, tag_id, store_id):
        tag=tagModel.query.get_or_404(tag_id)
        store=StoreModel.query.get_or_404(store_id)
        tag.store=store
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while linking the tag to the store.")
        return tag