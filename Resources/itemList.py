# This  will call the Resource Item
import json
from flask_restx import Resource, Api
from Model.item_model import ItemModel


class ItemList(Resource):
    # Getting all the data from the "items" collection
    def get(self):
        items = ItemModel.get_all_items()
        print("items")
        return items
