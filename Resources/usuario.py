# This  will call the Usuario model
from datetime import datetime
from Model.usuario_model import UsuarioModel
from flask_restx import Resource
from flask import make_response
from bson import ObjectId


class Usuario(Resource):

    # Creating users based on time
    # The GET methood to return an USER
    def get(self, nome):
        print("GET")
        usermodel_obj = UsuarioModel()
        res_docu = usermodel_obj.get_item(nome=nome)
        # Checking the response from the Model
        if ObjectId.is_valid(res_docu["_id"]):
            print("The object is a BSON")
            return make_response(
                "usuario encontrado com sucesso", 200
            )

    def post(self, nome, sobrenome=None, email=None, address=None, password=None, username=None, celular=None):
        print("POST")
        # For testing using this dict
        usuario = {
            "nome": nome,
            "sobrenome": "Silva" + str(datetime.now().microsecond),
            "email": "test@test.org",
            "address": "av.Testingfying",
            "password": "test2020",
            "username": "u_" + str(datetime.now().microsecond),
            "celular": "11988" + str(datetime.now().microsecond)
        }
        user_obj = UsuarioModel()
        res_user_post = user_obj.novo_solicitante(usuario=usuario)
        # if the HTTP code or messages are not the expected
        #  Based on the type of object retrieved. <ObjectId =MongoDB response of _id created>,
        #  <flask.wrappers.Response = Response retrieved>
        # abort(
        #     401, "Usuario {nome} ja existe no banco de dados".format(
        #         nome=nome)
        # )
        if "flask.wrappers.Response" in str(type(res_user_post)):
            if res_user_post.status_code < 300 or "nao se criara o usuario" not in str(res_user_post.get_data()):
                return make_response("usuario criado com sucesso", 200)
            else:
                return make_response(
                    "usuario  nao foi criado", res_user_post.status_code)
        elif "ObjectId" in str(type(res_user_post)):
            return make_response(
                "usuario  usuario.get('nome') criado com sucesso", 200
            )

    def delete(self, nome=None, _id=None):
        print("DELETE")
        user_obj = UsuarioModel()
        res_user_delete = user_obj.delete_user(nome=nome, _id=_id)
        # Checking the response from the Model
        if "flask.wrappers.Response" in str(type(res_user_delete)):
            if res_user_delete.status_code < 300 or "usuario nao foi apagado" not in str(res_user_delete.get_data()):
                return make_response("usuario apagado com sucesso", 200)
            else:
                return make_response(
                    "usuario nao foi apagado", res_user_delete.status_code)
        elif "ObjectId" in str(type(res_user_delete)):
            return make_response(
                "usuario apagado com sucesso", 200
            )
