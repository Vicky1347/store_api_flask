from marshmallow import Schema, fields #marshmallow is used for validation and serialization

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True) #dump only means we are genrating it ourself hence no need to provide it while creating item
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    
class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
   
    
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()
    
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True)
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()),dump_only=True)
    
class storeSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()),dump_only=True)
    
class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    
class TagAndItemSchema(Schema):
    message=fields.Str()
    item=fields.Nested(ItemSchema)
    tag=fields.Nested(TagSchema)
    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True) #load only means api never returns the password