# This  will call the Usuario model
from datetime import datetime
from Model.usuario_model import UsuarioModel
from flask_restx import Resource, Api
from flask import jsonify, make_response, abort


class Usuario(Resource):

    # Creating users based on time

    def get(self, nome):
        print("GET")
        user_obj = UsuarioModel()
        return user_obj.get_item(nome=nome)

    def post(self, nome, sobrenome=None, email=None, address=None, password=None, username=None, celular=None):
        print("POST")

        usuario = {
            "nome": nome,
            "sobrenome": "Silva"+str(datetime.now().microsecond),
            "email": "test@test.org",
            "address": "av.Testingfying",
            "password": "test2020",
            "username":  "u_"+str(datetime.now().microsecond),
            "celular": "11988"+str(datetime.now().microsecond)
        }
        user_obj = UsuarioModel()
        res_user_post = user_obj.novo_solicitante(usuario=usuario)
        # if the HTTP code or messages are not the expected
        #  Based on the type of object retrieved. <ObjectId =MongoDB response of _id created>, <flask.wrappers.Response = Response retrieved>
        if "flask.wrappers.Response" in str(type(res_user_post)):
            if res_user_post.status_code < 300 or "usuario nao foi criado" not in str(res_user_post.get_data()):
                return make_response("User criado com sucesso", 200)
            else:
                return make_response(
                    "usuario  nao foi criado", res_user_post.status_code)
        elif "ObjectId" in str(type(res_user_post)):
            return make_response(
                "usuario  criado", 200
            )
