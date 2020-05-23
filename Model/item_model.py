from flask import make_response
from Model.mongo_conexion import ConexionMongo
from bson import ObjectId


class ItemModel:
    collection = "items"
    db_inst = "local"

    def __init__(self, item_id=None, nome=None, descricao=None, data_inicio=None, data_final=None, status=None,
                 proprietario=None):
        self.item_id = item_id
        self.nome = nome
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_final = data_final
        self.status = status
        self.proprietario = proprietario

    def __repr__(self):
        return f"<Item: ID:{self.item_id}, {self.nome}  - {self.descricao}, status {self.status}. Disponivel  " \
               f"{self.data_inicio} - " \
               f"{self.data_final}, {self.proprietario}>"

    def get_all_items(self):
        # Getting all the data from the "items" collection
        print("get_all_items")
        return ConexionMongo.get_all_data(collection="items")

    def get_item(self, nome):
        """
        This will get an item from an collection
        :param nome: The nome of the item to find
        :return: a dictionary
        """
        # Getting all the data from the "items" collection
        print(f"looking for {nome}")
        # Will get an object BSON if item is find

        # Using the jsonify thing:
        data_found = ConexionMongo.get_dict_from_mongodb(db_inst=ItemModel.db_inst,
                                                         collection=ItemModel.collection, mode="get_one", nome=nome)
        # Verifying if the _id obtained is an ObjectId valid

        if "dict" in str(type(data_found)) or "ObjectId" in str(type(data_found)):
            return data_found
        else:
            return make_response(
                "item  nao foi encontrado, documento inexistente", 404)

    def novo_item(self, item):
        """
        Will create the new object Item using the data entered through the resource
        :param: dictionary with the item key:values
        :return: an Item object
        """
        print("NOVO ITEM")
        nome = item.get("nome", None)
        descricao = item.get("descricao", None)
        data_inicio = item.get("data_inicio", None)
        data_final = item.get("data_final", None)
        status = item.get("status", None)
        proprietario = item.get("proprietario", None)

        try:
            print("TRY")
            data_found = ConexionMongo.get_dict_from_mongodb(db_inst=ItemModel.db_inst,
                                                             collection=ItemModel.collection, mode="create", nome=nome)
            # When object does not exists in the collection, create it
            # nome=nome)
            if not data_found:  # Data not found
                new_item = ItemModel(
                    nome=nome, descricao=descricao, data_inicio=data_inicio, data_final=data_final, status=status,
                    proprietario=proprietario)
                python_dict_item = {
                    "nome": new_item.nome,
                    "descricao": new_item.descricao,
                    "data_inicio": new_item.data_inicio,
                    "data_final": new_item.data_final,
                    "status": new_item.status,
                    "proprietario": new_item.proprietario
                }

                res_creation = ConexionMongo.add_document(db_inst=ItemModel.db_inst,
                                                          collection=ItemModel.collection,
                                                          python_dict=python_dict_item)
                # @TODO  change the logic to get the object res itself and use them for the JSON response

                if res_creation.acknowledged and ObjectId.is_valid(res_creation.inserted_id):
                    print("Data retrieved of mongo operation:", res_creation.acknowledged, res_creation.inserted_id)
                return res_creation
                # return make_response("Item {nome} criado com sucesso ".format(
                #     nome=nome), 201)

            elif ObjectId.is_valid(data_found["_id"]):
                print("The object exists") # For testing
                return data_found
            return make_response("item ja existe na collection, nao se criara o item", 401)

        except Exception as e:
            print("Error criando o novo item ItemModel: {}".format(e))
        return make_response(
            "item nao foi criado, ja existe", 500
        )

    def update_item(self, nome, item_data):
        """
        Will update the Item object
        :param nome: the name of the object "Item"
        :param data_item: json The values that are being updated
        :return: a dictionary of the  Item object updated
        """
        print("TRY ")
        try:
            query = {"nome": nome}
            item_set_values = {"$set": {
                "nome": nome,
                "descricao": item_data.get("descricao"),
                "data_inicio": item_data.get("data_inicio"),
                "data_final": item_data.get("data_final"),
                "status": item_data.get("status"),
                "proprietario": item_data.get("proprietario"),
                "last_update": item_data.get("last_update")}
            }
            result = ConexionMongo.update_document(db_inst=ItemModel.db_inst,
                                                   collection=ItemModel.collection, query=query,
                                                   values_set=item_set_values)
            return result

        except Exception as e:
            print("Error atualizando o  item: {}".format(e))
            return make_response(
                "item nao foi atualizado", 400
            )

    def delete_item(self, nome=None, _id=None):
        """
        Will delete a document type "Item" if found
        :param nome: str The nome of the item to be removed
        :param _id: ObjectID The id of the item to be removed (not available for MVP)
        :return: a response object
        """
        # Checking if the item exists in the collection
        print(f"looking for {nome}")
        user_deleted = False
        try:
            # Searching by nome
            print("try")
            if nome and not _id:
                query = {"nome": nome}
                result = ConexionMongo.remove_document(db_inst=ItemModel.db_inst, collection=ItemModel.collection,
                                                       query=query)
                return result
        except Exception as e:
            print(f"Delete failed {e}")
            return e
