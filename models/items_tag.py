# from db import db

# class itemsTagModel(db.Model):
#     __tablename__ = "items_tags"

#     id=db.Column(db.Integer, primary_key=True)
#     item_id = db.Column(db.Integer, db.ForeignKey("items.id"), primary_key=True)
#     tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
    
#     item = db.relationship("ItemModel", backref="items_tags")
#     tag = db.relationship("tagModel", backref="items_tags")
    