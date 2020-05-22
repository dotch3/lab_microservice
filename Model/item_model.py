from flask import jsonify, make_response, abort
from Model.mongo_conexion import ConexionMongo


class ItemModel:
    collection = "items"
    db_inst = "local"
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
        """
        This will get an item from an collection
        :param nome: The nome of the item to find
        :return: a dictionary
        """
        # Getting all the data from the "usuarios" collection
        print(f"looking for {nome}")
        # Will get an object BSON if item is found

        # Using the jsonify thing:
        data_found = ConexionMongo.get_dict_from_mongodb(db_inst=ItemModel.db_inst,
                                                         collection=ItemModel.collection, mode="get_one", nome=nome)
        print(data_found)
        # Verifying if the _id obtained is an ObjectId valid
        if data_found:
            print("eureka! {}".format(data_found["_id"]))
            return data_found  # return a dict
        else:
            print("Oops, the aliens again!")
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
