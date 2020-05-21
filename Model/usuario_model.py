from flask import jsonify, make_response, abort
from flask_restful import Resource, reqparse
from pymongo import MongoClient
from Model.mongo_conexion import ConexionMongo
from bson import json_util


class UsuarioModel():
    TYPES_USERS = ("solicitante", "proprietario")
    # Connect database
    # conexion_db = ConexionMongo()

    def __init__(self, user_id=None, nome=None, sobrenome=None, email=None, address=None, username=None, password=None, celular=None, tipo_usuario=None):
        self.user_id = user_id
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.username = username
        self.password = password
        self.address = address
        self.celular = celular
        self.tipo_usuario = tipo_usuario

    @classmethod
    def criar_proprietario(cls, nome=None, sobrenome=None, email=None, address=None, username=None, password=None, celular=None):

        db_conex = conexion_db.get_service(nome="Usuarios")
        try:
            db_conex.add(Usuario(usuario_id, nome,
                                 address, fono, TYPES_USERS[0]))
        except Exception as e:
            raise RuntimeError(
                "Nao foi possivel ingressar o novo usuario proprietario")

    @classmethod
    def criar_solicitante(cls, nome=None, sobrenome=None, email=None, address=None, username=None, password=None, celular=None):
        return UsuarioModel(nome=nome, sobrenome=sobrenome, email=email, address=address, username=username, password=password, celular=celular, tipo_usuario=UsuarioModel.TYPES_USERS[0])

    @staticmethod
    def novo_solicitante(usuario):
        nome = usuario.get("nome", None)
        sobrenome = usuario.get("sobrenome", None)
        email = usuario.get("email", None)
        address = usuario.get("address", None)
        username = usuario.get("username", None)
        password = usuario.get("password", None)
        celular = usuario.get("celular", None)

        # Criando a conexao e procurando se existe o usuario no banco

        ITEMS = ConexionMongo.get_all_data(collection='usuarios')
        db_collection = "usuarios"
        try:
            data_found = UsuarioModel.user_in_database(
                data_response=ITEMS, nome=nome)
            if not data_found:
                # Creating the object UsuarioModel of type "solicitante"
                # Fabric pattern applied here
                new_user = UsuarioModel.criar_solicitante(
                    nome=nome, sobrenome=sobrenome, email=email, address=address, username=username, password=password, celular=celular)
                u = {
                    "nome": new_user.nome,
                    "sobrenome": new_user.sobrenome,
                    "email": new_user.email,
                    "address": new_user.address,
                    "username": new_user.username,
                    "password": new_user.password,
                    "celular": new_user.celular,
                }
                # Connecting to the mongo for
                db_conn = ConexionMongo.create_conexion("local")
                _id = items_db = db_conn[db_collection].insert_one(u)
                assert _id.acknowledged
                # If the insert of the new document was succeeded the _id.acknowledged TRUE  is retrieved
                return _id.inserted_id
            else:
                abort(
                    401, "Usuario {nome} ja existente no banco de dados".format(
                        nome=nome)
                )
        except Exception as e:
            return make_response(
                "usuario nao foi criado", 406
            )

    @ staticmethod
    def get_all_items():
        # Getting all the data from the "usuarios" collection
        return ConexionMongo.get_all_data(collection='usuarios')

    @ classmethod
    def get_item(cls, nome):
        # Getting all the data from the "usuarios" collection
        print(f"looking for {nome}")
        ITEMS = ConexionMongo.get_all_data(collection='usuarios')
        data_found = UsuarioModel.user_in_database(
            data_response=ITEMS, nome=nome)
        if data_found:
            return data_found
        else:
            abort(
                404, "Usuario com nome {nome} nao encontrado".format(
                    nome=nome)
            )

    def user_in_database(data_response, nome):
        data = data_response.get_json()  # to make lists from flask responses
        data_found = None
        for item in data:
            if nome in str(item):
                data_found = item
        return data_found
