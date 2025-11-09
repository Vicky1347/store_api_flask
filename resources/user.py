import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from db import db

from schema import UserSchema
from models import userModel
from blocklist import Blocklist

blp = Blueprint("User", __name__, description="Operations on Users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        if userModel.query.filter_by(username=user_data["username"]).first():
            abort(409,message="A user with that username already exists.")
        
        hashed_password=pbkdf2_sha256.hash(user_data["password"])
        user=userModel(username=user_data["username"],password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        
        return {"message":"User created successfully."},201 
    
@blp.route("/user/<int:user_id>")
class UserDetail(MethodView):
    @blp.response(200,UserSchema)
    def get(self,user_id):
        user=userModel.query.get_or_404(user_id)
        return user
    
    def delete(self,user_id):
        user=userModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"user deleted"}
    
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        user=userModel.query.filter_by(username=user_data["username"]).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token=create_access_token(identity=str(user.id))
            return {"access_token":access_token}
        abort(401,message="Invalid credentials.")
        
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        Blocklist.add(jti) 
        return {"message":"User logged out successfully."}