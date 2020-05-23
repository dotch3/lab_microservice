# This  will call the Resource Item
from datetime import datetime, timedelta
from flask_restx import Resource
from Model.item_model import ItemModel
from flask import make_response, abort, json


class Item(Resource):
    # Getting an item with the name "nome"
    def get(self, nome):
        """
        Function to get an object of 'Item' type from the items mongoDB collection based on the  keyword 'nome'
         :param nome: The name of the document type 'Item' to find if exists in the mongodb collection
        :return: mongo document of type 'Item'
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
            return make_response("item nao existe na collection", 404)

    def post(self, nome, descricao=None, data_inicio=None, data_final=None, status=None, proprietario=None):
        """
        Function to create a new Item
        :param nome: nome do item, which is unique
        :param descricao: the description of the item
        :param data_inicio: time the initial time that will be available
        :param data_final:time the final time that will be available
        :param status: str status of item
        :return:
        """
        print("POST")
        # For testing using this dict
        item_data = {
            "nome": nome,
            "descricao": "Ferramenta Model:" + str(datetime.now().microsecond),
            "data_inicio": str(datetime.now().microsecond),
            "data_final": str(datetime.now().microsecond),
            "status": "livre"
        }
        # Sending the request for the creation
        res_item_post = ItemModel.novo_item(self, item=item_data)
        # Creation on mongo retuns the id of the object
        # Working on the results obtained by the model

        if res_item_post:
            # When created the return are: res_creation.acknowledged, res_creation.inserted_id
            #  objetcId 5ec98c03683d5e17ad4a668b
            # <class 'pymongo.results.InsertOneResult'>
            # <pymongo.results.InsertOneResult object at 0x1103f4460>
            if "InsertOneResult" in str(type(res_item_post)):
                print("new :", res_item_post.acknowledged, res_item_post.inserted_id)
                return make_response("item  foi criado com sucesso, _id: {_id}".format(_id=res_item_post.inserted_id),
                                     201)
            # When document exists, the return is a dictionary with the document
            # <class 'dict'>
            # {'_id': ObjectId('5ec98ae9765e59b87bd3d571'), 'nome': 'lata', 'descricao': 'Ferramenta Model:173683',
            # 'data_inicio': '173690', 'data_final': '173691', 'status': 'livre', 'proprietario': None}
            elif "dict" in str(type(res_item_post)):
                print(res_item_post.get("_id"))
                # data_json = json.dumps(res_item_post.raw_result)
                # data_encoded = json.loads(data_json)
                return make_response(
                    "item  nao foi criado, documento existente, _id: {_id}".format(_id=res_item_post.get("_id")), 403)

        else:
            make_response("item  {nome} nao foi criado, verifique seus dados", 404)

    def put(self, nome, item=None):
        """
        Function to get update an 'Item', it requires item's nome
         :param nome: The name of the document type 'Item' to update
        :param item: dictionary with the parameters to be used for the update of the document
        :return: dictionary 'Usuario' with new values
        """
        print("PUT")
        # Using mocked data for testing purposes:
        item_data = []
        if not item:
            print("none item retrieved , lets mockup it for tests")
            item_data = {
                "nome": nome,
                "descricao": "Ferramenta Test Model" + str(datetime.now().microsecond),
                "data_inicio": str(datetime.now()),
                "data_final": str(datetime.now() + timedelta(days=10, hours=3)),
                "status": "livre",
                "proprietario": "",
                "last_update": str(datetime.now().strftime("%d-%m-%Y_%H_%M_%S"))
            }

        else:
            item_data = item
        res_item_updated = ItemModel.update_item(self, nome=nome, item_data=item_data)
        print("resultado")
        # When updated or not, the result is:
        # <pymongo.results.UpdateResult object at 0x108f39b90>
        # <class 'pymongo.results.UpdateResult'>
        # data_encoded-json
        # {'n': 0, 'nModified': 0, 'ok': 1.0, 'updatedExisting': False}

        if res_item_updated:
            data_json = json.dumps(res_item_updated.raw_result)
            data_encoded = json.loads(data_json)
            if data_encoded["updatedExisting"]:
                return make_response(
                    " Item: {nome} atualizado com sucesso ".format(nome=nome), 202
                )
            else:
                abort(404, " documento de item {nome} nao foi encontrado".format(nome=nome))
        else:
            print("item not found")
            abort(400, " update do item {nome} nao e permitido, verifique seus dados".format(nome=nome))

    def delete(self, nome, _id=None):
        """
        Function to delete a document type Item
         :param nome: The name of the document type 'Item' to find if exists in the mongodb collection
        :param _id: ObjectId, the identifier of the document that can be used to find the document and delete it too
        :return: A pymongo.results.DeleteResult object
        """
        print("DELETE")
        res_item_delete = ItemModel.delete_item(self, nome=nome, _id=_id)
        # Checking the response from the Model
        if res_item_delete:
            if "dict" in str(type(res_item_delete)):
                return make_response(
                    " documento de item {nome} apagado com sucesso, _id {_id} ".format(nome=nome,
                                                                                       _id=res_item_delete["_id"]),
                    202
                )
            elif res_item_delete["nome"] == nome:
                return make_response(
                    "documento de item {nome} apagado com sucesso ".format(nome=nome), 202)

        else:
            print("did not find the item")
            abort(404, " documento de item {nome} nao foi encontrado, verifique seus dados".format(nome=nome))
