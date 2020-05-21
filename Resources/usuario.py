# This  will call the Usuario model
from Model.usuario_model import UsuarioModel
from flask_restx import Resource, Api


class Usuario(Resource):
    def get(self, nome):
        user_obj = UsuarioModel()
        return user_obj.get_item(nome)

    def post(self):
        user_obj = UsuarioModel()
        return user_obj.criar_solicitante(), 201


class UsuarioList(Resource):

    def get(self):
        user_obj = UsuarioModel()
        return user_obj.get_all_items()
