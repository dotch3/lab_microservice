# This  will call the Resource Item
import json
from flask_restx import Resource, Api
from Model.item_model import ItemModel


class Item(Resource):
    # Getting an item with the name "nome"
    def get(self, nome):
        items = ItemModel.get_item(nome)
        return items
