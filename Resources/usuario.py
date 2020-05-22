# This  will call the Usuario model
from datetime import datetime
from Model.usuario_model import UsuarioModel
from flask_restx import Resource
from flask import make_response, abort


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
        res_docu = usermodel_obj.get_item(nome=nome)
        # Checking the response from the Model
        if "ObjectId" in str(type(res_docu)) or "dict" in str(type(res_docu)):
            print("The object is a BSON")
            if res_docu.get("nome") == nome:
                return make_response(
                    "usuario encontrado com sucesso", 200
                )
            elif res_docu["nome"] == nome:
                return make_response(
                    "usuario encontrado com sucesso", 200
                )

        else:
            return make_response("usuario no existe na collection", 404)

    def post(self, nome, sobrenome=None, email=None, address=None, password=None, username=None, celular=None):
        """
        Function to create a new 'Usuario' (proprietario,solicitante), using the 'Factory'pattern
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
                    "usuario  {nome} nao foi criado, documento existente {code}".format(code=res_user_post.status_code,
                                                                                        nome=usuario.get("nome")),
                    res_user_post.status_code)
        elif "ObjectId" in str(type(res_user_post) or "dict" in str(type(res_user_post))):
            return make_response(
                "usuario  usuario.get('nome') criado com sucesso", 200
            )

    def put(self, nome, usuario=None):
        """
        Function to update an existent document of type 'Usuario' base don nome keyword entered
        :param nome: str The nome of  the document type 'Usuario' to be updated
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
            print("data retrieved")
            usuario_data = usuario

        print(usuario_data)
        res_user_updated = UsuarioModel.update_user(nome=nome, usuario_data=usuario_data)
        print("resultado")
        print(str(type(res_user_updated)))
        if "None" not in str(type(usuario_data)):
            if res_user_updated.modified_count > 0:
                return make_response(
                    " documento de usuario {nome} atualizado com sucesso ".format(nome=nome), 202
                )
            elif "flask.wrappers.Response" in str(type(res_user_updated)):
                if res_user_updated.status_code != 400:
                    abort(404, " documento de usuario {nome} nao foi encontrado".format(nome=nome))
        else:
            print("did not find the user")
            abort(400, " update do usuario {nome} nao e permitido, verifique seus dados".format(nome=nome))

    # else:
    #     abort(
    #         404, "Pessoa com sobrenome {lname} nao encontrada".format(lname=lname)
    #     )

    def delete(self, nome, _id=None):
        """
        Function to delete a  document of 'Usuario' type from the mongoDB collection, using 'nome' as keyword
        :param nome: str The nome of the 'Usuario' to find and delete from the mongoDB collection
        :param _id: ObjectId, the identifier of the document that can be used to find the document and delete it too
        (Not part of the MVP)
        :return: A pymongo.results.DeleteResult object
        """
        print("DELETE")
        user_obj = UsuarioModel()
        res_user_delete = user_obj.delete_user(nome=nome, _id=_id)
        # Checking the response from the Model
        if "ObjectId" in str(type(res_user_delete)) or "dict" in str(type(res_user_delete)):
            print("The object is a BSON")
            if res_user_delete.get("nome") == nome:
                return make_response(
                    " documento de usuario {nome} apagado com sucesso ".format(nome=nome), 202
                )
            elif res_user_delete["nome"] == nome:
                return make_response(
                    "documento de usuario {nome} apagado com sucesso ".format(nome=nome), 202)

        else:
            print("did not find the user")
            abort(404, " documento de usuario {nome} nao foi encontrado, verifique seus dados".format(nome=nome))
