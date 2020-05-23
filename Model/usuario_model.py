from flask import make_response
from Model.mongo_conexion import ConexionMongo
from bson import ObjectId


class UsuarioModel:
    TYPES_USERS = ("solicitante", "proprietario")
    collection = "usuarios"
    db_inst = "local"

    def __init__(self, user_id=None, nome=None, sobrenome=None, email=None, address=None, username=None, password=None,
                 celular=None, tipo_usuario=None):
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
    def criar_solicitante(cls, nome=None, sobrenome=None, email=None, address=None, username=None, password=None,
                          celular=None):
        """
        Class function following the "FABRIC" pattern, it will create a "usuario" object but with
        "tipo_usaurio=solicitante"
        :param nome: str Nome do usuario
        :param sobrenome: str o sobrenome do usuario
        :param email: email The email of the usuario
        :param address: The address of the usuario
        :param username: This is the username to identify the usuario in the system
        :param password: This by the moment is being type text, it is the password for the usuario
        :param celular: The cellphone of the usuario
        :return: A new usuario object of "solicitante" type
        """
        return UsuarioModel(nome=nome, sobrenome=sobrenome, email=email, address=address, username=username,
                            password=password, celular=celular, tipo_usuario=UsuarioModel.TYPES_USERS[0])

    @classmethod
    def criar_proprietario(cls, nome=None, sobrenome=None, email=None, address=None, username=None, password=None,
                           celular=None):
        """
        Class function following the "FABRIC" pattern, it will create a "usuario" object but with
        "tipo_usaurio=proprietario"
        :param nome: str Nome do usuario
        :param sobrenome: str o sobrenome do usuario
        :param email: email The email of the usuario
        :param address: The address of the usuario
        :param username: This is the username to identify the usuario in the system
        :param password: This by the moment is being type text, it is the password for the usuario
        :param celular: The cellphone of the usuario
        :return: A new usuario object of "proprietario" type
        """

        return UsuarioModel(nome=nome, sobrenome=sobrenome, email=email, address=address, username=username,
                            password=password, celular=celular, tipo_usuario=UsuarioModel.TYPES_USERS[1])

    def novo_solicitante(self, usuario):
        """
        This function will create a new Usuario of type "solicitante" and store it in the mongo database
        :param usuario: this is a dictionary with the data of the user
        """
        print("NOVO SOLICITANTE")
        nome = usuario.get("nome", None)
        sobrenome = usuario.get("sobrenome", None)
        email = usuario.get("email", None)
        address = usuario.get("address", None)
        username = usuario.get("username", None)
        password = usuario.get("password", None)
        celular = usuario.get("celular", None)

        try:
            print("TRY")
            data_found = ConexionMongo.get_dict_from_mongodb(db_inst=UsuarioModel.db_inst,
                                                             collection=UsuarioModel.collection, mode="create",
                                                             nome=nome)
            if not data_found:  # Data not found
                # Creating the object UsuarioModel of type "solicitante"
                # Fabric pattern applied here
                new_user = UsuarioModel.criar_solicitante(
                    nome=nome, sobrenome=sobrenome, email=email, address=address, username=username, password=password,
                    celular=celular)
                python_dict_usuario = {
                    "nome": new_user.nome,
                    "sobrenome": new_user.sobrenome,
                    "email": new_user.email,
                    "address": new_user.address,
                    "username": new_user.username,
                    "password": new_user.password,
                    "celular": new_user.celular,
                }

                res_creation = ConexionMongo.add_document(db_inst=UsuarioModel.db_inst,
                                                          collection=UsuarioModel.collection,
                                                          python_dict=python_dict_usuario)
                # res_creation.acknowledged  # <-- should return: True
                # res_creation.inserted_id  # <--- returns a bson ObjectId

                if res_creation.acknowledged and ObjectId.is_valid(res_creation.inserted_id):
                    return make_response("Usuario {nome} criado com sucesso ".format(
                        nome=nome), 201)


            elif ObjectId.is_valid(data_found["_id"]):
                print("The object exists")
                return make_response("usuario ja existe na collection, nao se criara o usuario", 401)
        except Exception as e:
            print("Error criando o novo usuario: {}".format(e))
            return make_response(
                "usuario nao foi criado, ja existe", 500
            )

    def get_all_items(self):
        """
        Function to call all the items of the "usuarios" collection
        :return: a jsonified dictionary of the usuarios
        """
        # Getting all the data from the "usuarios" collection
        return ConexionMongo.get_all_data(collection=UsuarioModel.collection)

    def get_usuario(self, nome):
        """
        This will get an usuario from an collection
        :param nome: The nome of the usuario to find
        :return: a dictionary
        """
        # Getting all the data from the "usuarios" collection
        print(f"looking for {nome}")
        # Will get an object BSON if item is found

        # Using the jsonify thing:
        data_found = ConexionMongo.get_dict_from_mongodb(db_inst=UsuarioModel.db_inst,
                                                         collection=UsuarioModel.collection, mode="get_one", nome=nome)
        # Verifying if the _id obtained is an ObjectId valid

        if "dict" in str(type(data_found)) or "ObjectId" in str(type(data_found)):
            return data_found
        else:
            return make_response(
                "usuario  nao foi encontrado, documento inexistente", 404)

    def update_user(self, nome, usuario_data):
        """
        This will update a document type "Usuario" if found
        :param nome: the nome of the 'Usuario' document
        :param usuario_data: the dictionary to use for the update
        :return: a flask response
        """
        # create the query to find the user first

        print("TRY ")
        try:
            query = {"nome": nome}
            user_set_values = {"$set": {
                "nome": nome,
                "sobrenome": usuario_data.get("sobrenome"),
                "email": usuario_data.get("email"),
                "address": usuario_data.get("address"),
                "tipo_usuario": usuario_data.get("tipo_usuario"),
                "last_update": usuario_data.get("last_update"), }
            }
            result = ConexionMongo.update_document(db_inst=UsuarioModel.db_inst,
                                                   collection=UsuarioModel.collection, query=query,
                                                   values_set=user_set_values)
            # Verifying the results obtained
            return result

        except Exception as e:
            print("Error atualizando o  usuario: {}".format(e))
            return make_response(
                "usuario nao foi atualizado", 400
            )

    def delete_user(self, nome=None, _id=None):
        """
        Will delete a document type "Usuario" if found
        :param nome: str The nome of the usuario to be removed
        :param _id: ObjectID The id of the usuario to be removed (not available for MVP)
        :return: a response object
        """
        # Checking if the user exists in the collection
        print(f"looking for {nome}")
        user_deleted = False
        try:
            # Searching by nome
            print("try")
            if nome and not _id:
                query = {"nome": nome}
                result = ConexionMongo.remove_document(db_inst=UsuarioModel.db_inst, collection=UsuarioModel.collection,
                                                       query=query)
                return result
        except Exception as e:
            print(f"Delete failed {e}")
            return e
