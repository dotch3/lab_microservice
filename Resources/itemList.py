# This  will call the Resource Item
import json
from flask_restx import Resource
from Model.item_model import ItemModel


class ItemList(Resource):
    # Getting all the data from the "items" collection
    def get(self):
        """
        Function to get  all the documents of type 'Item' from the mongoDB
        :return: list of documents <Item>
        """
        items = ItemModel.get_all_items()
        print("items")
        return items
