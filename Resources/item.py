# This  will call the Resource Item
import json
from flask_restx import Resource, Api
from Model.item_model import ItemModel


class Item(Resource):
    # Getting an item with the name "nome"
    def get(self, nome):
        res = ItemModel.get_item(nome)
        return res


class ItemList(Resource):
    # Getting all the data from the "items" collection
    def get(self):
        res = ItemModel.get_all_items()
        print("items")
        return res
