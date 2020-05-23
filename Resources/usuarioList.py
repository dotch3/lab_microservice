# This  will call the Usuario model
from Model.usuario_model import UsuarioModel
from flask_restx import Resource


class UsuarioList(Resource):

    def get(self):
        """
        Function to get  all the documents of type 'Usuario' from the mongoDB
        :return: list of documents <Usuario>
        """
        user_obj = UsuarioModel()
        print("usuarios")
        return user_obj.get_all_items()
