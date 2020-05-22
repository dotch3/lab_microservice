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
        """
        Function to get  a document of type 'Usuario' from the mongoDB based on the  keyword 'nome'
        :param nome: str The name of the document type 'Usuario' to find if exists in the mongodb collection, it is unique
        :return: mongo document of type 'Usuario'
        """
        print("GET")
        usermodel_obj = UsuarioModel()
        res_docu = usermodel_obj.get_item(nome=nome)
        # Checking the response from the Model
        if "ObjectId" in str(type(res_docu)) or "dict" in str(type(res_docu)):
            print("The object is a BSON")
            if res_docu.get("nome") == nome:
                return make_response(
                    "usuario encontrado com sucesso", 200
                )
            elif res_docu["nome"]==nome:
                return make_response(
                    "usuario encontrado com sucesso", 200
                )

        else:
            return make_response("usuario no existe na collection", 404)


    def post(self, nome, sobrenome=None, email=None, address=None, password=None, username=None, celular=None):
        """
        Function to create a new document of 'Usuario' type, using the 'Factory'pattern. 2 types of Usuarios: <solicitante>, <proprietario>
        :param nome: str The nome of the new usuario that is unique
        :param sobrenome: str The sobrenome of the new usuario, not unique
        :param email: str The email of the new usuario, not unique
        :param address: str The address of the new usuario, not unique
        :param password: str The password of the new usuario, not unique
        :param username: str The username of the new usuario, not unique (for MVP)
        :param celular: int  The mobile number of the new usuario, not unique
        :return: The new document of 'Usuario' type
        """
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
                    "usuario  nao foi criado, documento existente", res_user_post.status_code)
        elif "ObjectId" in str(type(res_user_post)):
            return make_response(
                "usuario  usuario.get('nome') criado com sucesso", 200
            )

    def delete(self, nome=None, _id=None):
        """
        Function to delete a  document of 'Usuario' type from the mongoDB collection, based on the existence of keyword entered: 'nome'
        :param nome: str The nome of the 'Usuario' to find and delete from the mongoDB collection
        :param _id: ObjectId, the identifier of the document that can be used to find the document and delete it too (Not part of the MVP)
        :return: A pymongo.results.DeleteResult object
        """
        print("DELETE")
        user_obj = UsuarioModel()
        res_user_delete = user_obj.delete_user(nome=nome, _id=_id)
        # Checking the response from the Model
        if res_user_delete:
            if "ObjectId" in str(type(res_user_delete)):
                print("docs deleted:", res_user_delete["nome"])
                return make_response(
                    "documento de usuario apagado com sucesso {res_user_delete.get_data()}", 202
                )
        else:
            return make_response(
                "usuario nao foi deletado", 304)
