# This  will call the Usuario
from datetime import datetime
from Model.usuario_model import UsuarioModel
from flask_restx import Resource
from flask import make_response, abort, json


class Usuario(Resource):

    # Creating users based on time
    # The GET methood to return an USER
    def get(self, nome):
        """
        Function to get  a document of type 'Usuario' from the mongoDB based on the  keyword 'nome'
        :param nome: str The name of the document type 'Usuario' to find if exists in the mongodb collection,
        it is unique
        :return: mongo document of type 'Usuario'
        """
        print("GET")
        usermodel_obj = UsuarioModel()
        res_docu = usermodel_obj.get_usuario(nome=nome)
        # Checking the response from the Model
        if "ObjectId" in str(type(res_docu)) or "dict" in str(type(res_docu)):
            if res_docu.get("nome") == nome:
                return make_response(
                    "usuario encontrado com sucesso", 200
                )
            elif res_docu["nome"] == nome:
                return make_response(
                    "usuario encontrado com sucesso", 200
                )

        else:
            return make_response("usuario no existente", 404)

    def post(self,  usuario):
        """
        Function to create a new 'Usuario' (proprietario,solicitante), using the 'Factory'pattern
        """
        print("POST")
        # For testing using this dict
        usuario = {
            "nome": "XXX",
            "sobrenome": "Silva" + str(datetime.now().microsecond),
            "email": "test@test.org",
            "address": "av.Testingfying",
            "password": "test2020",
            "username": "u_" + str(datetime.now().microsecond),
            "celular": "11988" + str(datetime.now().microsecond),
            "last_update": str(datetime.now().strftime("%d-%m-%Y_%H_%M_%S"))
        }
        res_user_post = UsuarioModel.novo_solicitante(self, usuario=usuario)
        if "flask.wrappers.Response" in str(type(res_user_post)):
            if res_user_post.status_code < 300 or "nao se criara o usuario" not in str(res_user_post.get_data()):
                return make_response("usuario criado com sucesso", 200)
            else:
                return make_response(
                    "usuario  {nome} nao foi criado, documento ja existente {code}".format(
                        code=res_user_post.status_code,
                        nome=usuario.get("nome")),
                    res_user_post.status_code)
        elif "ObjectId" in str(type(res_user_post) or "dict" in str(type(res_user_post))):
            return make_response(
                "usuario  usuario.get('nome') criado com sucesso", 200
            )

    def put(self, nome, usuario=None):
        """
        Function to update an 'Usuario' object
        :param nome: str The nome of  the 'Usuario' to be updated
        :param usuario: dictionary with the parameters to be used for the update of the document
        :return: dictionary 'Usuario' with new values
        """
        print("PUT")
        # Using mocked data for testing purposes:
        usuario_data = []
        if not usuario:
            print("none usuario retrieved , lets mockup it for tests")
            usuario_data = {
                "nome": nome,
                "sobrenome": "Soarez" + str(datetime.now().microsecond),
                "email": "test_updated" + str(datetime.now().microsecond) + "@test.org",
                "address": "av.TestingfyingUpdate" + str(datetime.now().microsecond),
                "tipo_usuario": "proprietario",
                "last_update": str(datetime.now().strftime("%d-%m-%Y_%H_%M_%S"))
            }
        else:
            usuario_data = usuario

        print(usuario_data)
        res_user_updated = UsuarioModel.update_user(self, nome=nome, usuario_data=usuario_data)
        # Working on the data retrieved
        if res_user_updated:
            data_json = json.dumps(res_user_updated.raw_result)
            data_encoded = json.loads(data_json)
            if data_encoded["updatedExisting"]:
                if "None" not in str(type(usuario_data)):
                    if "flask.wrappers.Response" in str(type(res_user_updated)):
                        if res_user_updated.status_code != 400:
                            abort(404, " documento de item {nome} nao foi encontrado".format(nome=nome))
                    elif res_user_updated.modified_count > 0:
                        return make_response(
                            " documento de usuario {nome} atualizado com sucesso ".format(nome=nome), 202
                        )
            else:
                abort(404, " documento de item {nome} nao foi encontrado".format(nome=nome))
        else:
            print("did not find the user")
            abort(400, " update do usuario {nome} nao e permitido, verifique seus dados".format(nome=nome))

    def delete(self, nome, _id=None):
        """
        Function to delete a  document of 'Usuario' type from the mongoDB collection, using 'nome' as keyword
        :param nome: str The nome of the 'Usuario' to find and delete from the mongoDB collection
        :param _id: ObjectId, the identifier of the document that can be used to find the document and delete it too
        (Not part of the MVP)
        :return: A pymongo.results.DeleteResult object
        """
        print("DELETE")
        res_user_delete = UsuarioModel.delete_user(self, nome=nome, _id=_id)
        # Checking the response from the Model
        if res_user_delete:
            if "ObjectId" in str(type(res_user_delete)):
                return make_response(
                    " documento de usuario {nome} apagado com sucesso, _id {_id} ".format(nome=nome,
                                                                                          _id=res_user_delete["_id"]),
                    202
                )
            elif res_user_delete["nome"] == nome:
                return make_response(
                    "documento de usuario {nome} apagado com sucesso ".format(nome=nome), 202)
        else:
            print("did not find the user")
            abort(404, " documento de usuario {nome} nao foi encontrado, verifique seus dados".format(nome=nome))
