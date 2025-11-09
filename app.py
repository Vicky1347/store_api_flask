from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager 
from db import db
from blocklist import Blocklist
import models
import os

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tags import blp as TagBlueprint
from resources.user import blp as UserBlueprint
def create_app(db_url=None):
 
    app = Flask(__name__)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    app.config["PROPAGATE_EXCEPTIONS"]=True
    app.config["API_TITLE"]="Store REST API"
    app.config["API_VERSION"]="v1"
    app.config["OPENAPI_VERSION"]="3.0.3"
    app.config["OPENAPI_URL_PREFIX"]="/"
    app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"]="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"]= db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    db.init_app(app) 
    
    api= Api(app)
    
    app.config["JWT_SECRET_KEY"]=os.getenv("JWT_SECRET_KEY")  #change this in real app
    jwt=JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in Blocklist
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return (
            {"message":"The token has been revoked.","error":"token_revoked"},
            401,
        )
    
    with app.app_context():
        
        db.create_all()


    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    
    return app

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"



# @app.route("/store" ,methods=['POST'])
# def create_store():
#      store_data = request.get_json()
#      if "name" not in store_data:
#         abort(
#            400,
#             message="Bad request. Ensure 'name' is included in the JSON payload.",
#         )
#         for store in stores.values():
#             if store_data["name"] == store["name"]:
#                 abort(400, message=f"Store already exists.")

#      store_id = uuid.uuid4().hex
#      store = {**store_data, "id": store_id}
#      stores[store_id] = store
#      return store, 201
     

# @app.route("/store/<string:store_id>", methods=['GET'])
# def get_store(store_id):
#     try:
#         return stores[store_id]
#     except IndexError:
#         abort (404,message="store not found")
        
# @app.route("/store/<string:store_id>", methods=['DELETE'])
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message":"store deleted"}
#     except IndexError:
#         abort (404,message="store not found")  
        

        
   

# @app.route("/item", methods=['POST'])
# def create_item():
#     item_data = request.get_json()

#     # Validate required fields
#     if (
#         "price" not in item_data
#         or "store_id" not in item_data
#         or "name" not in item_data
#     ):
#         abort(
#             400,
#             description=(
#                 "Bad request. Ensure 'price', 'store_id', and 'name' "
#                 "are included in the JSON payload."
#             ),
#         )

#     # Validate data types
#     if not isinstance(item_data["price"], (int, float)):
#         abort(400, description="'price' must be a number.")

#     if item_data["store_id"] not in stores:
#         abort(404, description="Store not found.")

#     # Check if the item already exists in the same store
#     for item in items.values():
#         if (
#             item_data["name"] == item["name"]
#             and item_data["store_id"] == item["store_id"]
#         ):
#             abort(400, description="Item already exists.")

#     # Create and store the item
#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id": item_id}
#     items[item_id] = item

#     return item, 201




# @app.route("/item/<string:item_id>", methods=['GET'])
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except IndexError:
#         abort (404,message="item not found")
    

# @app.route("/item/<string:item_id>", methods=['DELETE'])
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {"message":"item deleted"}
#     except IndexError:
#         abort (404,message="store not found")         
        

# @app.route("/item/<string:item_id>", methods=['PUT'])
# def update_item(item_id):
#     item_data = request.get_json()
#     if "price" not in item_data or "name" not in item_data:
#         abort(
#             400,
#             message="Bad request. Ensure 'name' and 'price' are included in the JSON payload.",
#         )
#     try:
#         item = items[item_id]
#         item.update(item_data)
#         # item |= item_data
#         return item
        
#     except IndexError:
#         abort (404,message="store not found")         




