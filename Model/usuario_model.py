from flask import jsonify, make_response, abort
from flask_restful import Resource, reqparse
from pymongo import MongoClient
from Model.mongo_conexion import ConexionMongo


class UsuarioModel():
    TYPES_USERS = ("solicitante", "proprietario")
    # Connect database
    # conexion_db = ConexionMongo()

    def __init__(self, user_id=None, nome=None, sobrenome=None, address=None, celular=None, tipo_usuario=None):
        self.user_id = user_id
        self.nome = nome
        self.sobrenome = sobrenome
        self.address = address
        self.celular = celular
        self.tipo_usuario = tipo_usuario

    @classmethod
    def criar_proprietario(cls, nome, sobrenome, address, celular):

        db_conex = conexion_db.get_service(nome="Usuarios")
        try:
            db_conex.add(Usuario(usuario_id, nome,
                                 address, fono, TYPES_USERS[0]))
        except Exception as e:
            raise RuntimeError(
                "Nao foi possivel ingressar o novo usuario proprietario")

    @classmethod
    def criar_solicitante(cls, nome, sobrenome, address, celular):
        db_conex = conexion_db.get_service(nome="Usuarios")
        try:
            db_conex.add(Usuario(usuario_id, nome,
                                 address, fono, TYPES_USERS[1]))
        except Exception as e:
            raise RuntimeError(
                "Nao foi possivel ingressar o novo usuario solicitante")

    @staticmethod
    def get_all_items():
        # Getting all the data from the "usuarios" collection
        return ConexionMongo.get_all_data(collection='usuarios')

    @classmethod
    def get_item(cls, nome):
        # Getting all the data from the "usuarios" collection
        ITEMS = ConexionMongo.get_all_data(collection='usuarios')
        data = ITEMS.get_json()  # to make lists from flask responses
        data_found = None
        for item in data:
            if nome in str(item):
                data_found = item
        if data_found:
            return data_found
        else:
            abort(
                404, "Usuario com nome {nome} nao encontrado".format(
                    nome=nome)
            )
