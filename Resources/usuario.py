# This  will call the Usuario model
from flask_restful import Resource
from Model.usuario_model import Usuario


class Users(Resource):
    def get_all(self):
        user_obj = Usuario()
        return user_obj.get_all_items()


class UsersList(Resource):
    def get_all_items(self):
        # Getting all the data from the "usuarios" collection
        user_obj = Usuario()
        return user_obj.get_all_items()
