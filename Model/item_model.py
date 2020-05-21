from flask import jsonify, make_response, abort
from pymongo import MongoClient
from Model.mongo_conexion import ConexionMongo


class ItemModel:
    def __init__(self, item_id=None, nome=None, descricao=None, data_inicio=None, data_final=None, status=None):
        self.item_id = item_id
        self.nome = nome
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fin = data_final
        self.status = status

    def __repr__(self):
        return f"<Item: ID:{self.item_id}, {self.nome} , status {self.status}. Disponivel  {self.data_inicio} - " \
               f"{self.data_final}>"

    @classmethod
    def get_all_items(cls):
        # Getting all the data from the "items" collection
        return ConexionMongo.get_all_data(collection='items')

    @classmethod
    def get_item(cls, nome):
        # Getting all the data from the "items" collection
        ITEMS = ConexionMongo.get_all_data(collection='items')
        data = ITEMS.get_json()  # to make lists from flask responses
        data_found = None
        for item in data:
            if nome in str(item):
                print("Eureka!")
                data_found = item

        if data_found:
            return data_found
        else:
            abort(
                404, "Item com nome {nome} nao encontrado".format(
                    nome=nome)
            )

    @classmethod
    def create_item(cls, nome, descricao, data_inicio, data_final, status):
        ITEMS = ConexionMongo.get_dict_from_mongodb()
        if lname not in ITEMS and lname is not None:
            item = {
                "address": lname,
                "fname": fname,
                "timestamp": get_timestamp(),
            }
            db.clientes.insert_one(item)
            return make_response(
                "{lname} criado com sucesso".format(lname=lname), 201
            )
        else:
            abort(
                406,
                "Pessoa com sobrenome {lname} ja existe".format(lname=lname),
            )
