
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#The Api works with resources and every resource has to be a class.

class Item(Resource): #Inherit from the Resource class - a copy of a Resource class(implement some features of a Resource) with our changes.
    parser = reqparse.RequestParser() #new object wich we can use to parse the request
    parser.add_argument('price', # the patser is looking through the JSON payload or HTML form
    type = float,
    required = True, #to make sure that no request can come through with no price
    help = "This field cannot be blank!")

    parser.add_argument('store_id',
    type = int,
    required = True,
    help = "Every item needs id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "The item not found!"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'massage': "An item with name '{}' is already exist.".format(name)}, 400 #If already exist so will return 400 - bad request.
        data = Item.parser.parse_args() #like request.get_json() but takes only the right value - price for this example
        #data = request.get_json() #the request is going to have a json payload a body attached to it. Remember to set up Content-Type and etc in Postman.
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message': "An error occured"}, 500 #Internal server error
        return item.json(), 201 #Just to tell to the client that this happened.

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'massage': 'Item deleted!'}

#Filter returns only those elements for which the function_object returns true.
    def put(self, name): #can create and update
        data = Item.parser.parse_args() #like request.get_json() but takes only the right value - price for this example
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource): #Get all the items in a list of items.
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}apply the func to each element in this list and make into the list
