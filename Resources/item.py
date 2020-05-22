# This  will call the Resource Item
from flask_restx import Resource, Api
from Model.item_model import ItemModel
from bson import ObjectId
from flask import make_response


class Item(Resource):
    # Getting an item with the name "nome"
    def get(self, nome):
        """
        Function to get an item of type Item
        :param nome: The name of the Item to find if exists in the mongodb collection
        :return: Flask responses
        """
        print("GET")
        itemmodel_obj = ItemModel()
        res_docu = itemmodel_obj.get_item(nome=nome)
        # Checking the response from the Model
        if "ObjectId" in str(type(res_docu)) or "dict" in str(type(res_docu)):
            print("The object is a BSON")
            return make_response(
                "item encontrado com sucesso", 200
            )
        else:
            return make_response("item no existe na collection", 404)
