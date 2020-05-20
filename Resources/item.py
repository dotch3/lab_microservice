# This  will call the Resource Item
from flask_restful import Resource
from Model.item_model import Item


class Item(Resource):
    @staticmethod
    def get_all():
        item_obj = Item()
        return item_obj.get_all_items()

    @staticmethod
    def create(item):
        data_final = item.get("data_final", None)
        data_inicio = item.get("data_inicio", None)
        descricao = item.get("descricao", None)
        nome = item.get("nome", None)
        status = item.get("status", None)

        item_obj = Item()
        return item_obj.create_item()


class ItemList(Resource):
    @staticmethod
    def get_all_items():
        # Getting all the data from the "items" collection
        return ConexionMongo.get_all_data(collection='items')
