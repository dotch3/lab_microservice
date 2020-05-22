from flask import make_response, abort
from Model.mongo_conexion import ConexionMongo
from bson import json_util
from bson import ObjectId


class UsuarioModel:
    TYPES_USERS = ("solicitante", "proprietario")
    collection = "usuarios"
    db_inst = "local"

    # Connect database
    # conexion_db = ConexionMongo()

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

        pass

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

    @staticmethod
    def novo_solicitante(usuario):
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
                                                             collection=UsuarioModel.collection, mode="get_one",
                                                             nome=nome)
            if not data_found:  # Data not found
                # Preparing the user information, this should happening when data is retrieved from UI and pass
                # through the system
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
                return make_response("{nome} ja existe na collection {collection}, nao se criara o usuario".format(
                    nome=nome, collection=UsuarioModel.collection), 401)
        except Exception as e:
            print("Error criando o novo usuario: {}".format(e))
            return make_response(
                "usuario nao foi criado", 500
            )

    @staticmethod
    def get_all_items():
        """
        Function to call all the items of the "usuarios" collection
        :return: a jsonified dictionary of the usuarios
        """
        # Getting all the data from the "usuarios" collection
        return ConexionMongo.get_all_data(collection=UsuarioModel.collection)

    @classmethod
    def get_item(cls, nome):
        """
        This will get an item from an collection
        :param nome: The nome of the item to find
        :return: a dictionary
        """
        # Getting all the data from the "usuarios" collection
        print(f"looking for {nome}")
        # Will get an object BSON if item is found

        # Using the jsonify thing:
        data_found = ConexionMongo.get_dict_from_mongodb(db_inst=UsuarioModel.db_inst,
                                                         collection=UsuarioModel.collection, mode="get_one", nome=nome)
        print(data_found)
        # Verifying if the _id obtained is an ObjectId valid
        if data_found:
            print("eureka! {}".format(data_found["_id"]))
            return data_found  # return a dict
        else:
            print("Oops, the aliens again!")
            abort(
                404, "Usuario com nome {nome} nao encontrado".format(
                    nome=nome)
            )

    @classmethod
    def delete_user(cls, nome=None, _id=None):
        # Checking if the user exists in the collection
        print(f"looking for {nome}")
        ITEMS = ConexionMongo.get_all_data(collection=UsuarioModel.collection)
        # If both values ae provided
        user_in_collection = False
        try:
            # Searching by nome
            print("try")
            if nome and not _id:
                query = {"nome": nome}
                print("nome and not id")
                item_found = UsuarioModel.user_in_database(
                    data_response=ITEMS, nome=nome)
                # When the item is inside the collection
                if item_found:
                    print("ITEM FOUND")
                    # Mongoclient
                    db_conn = ConexionMongo.create_conexion("local")
                    _id = db_conn[UsuarioModel.collection].delete_one(query)
                    # if the deletion was succeeded the count is >0
                    return _id.deleted_count
                else:
                    return make_response(
                        "{nome} nao encontrado".format(nome=nome), 404
                    )
            # Searching by _id
            elif _id:
                # query = {"_id": _id}
                item_found = UsuarioModel.user_in_database(
                    data_response=ITEMS, user_id=_id)
                # When the item is inside the collection
                if item_found:
                    # Mongoclient
                    db_conn = ConexionMongo.create_conexion("local")
                    _id = db_conn.delete_one({'_id': ObjectId(_id)})
                    # Tests
                    assert _id.acknowledged
                    # if the deletion was succeeded the count is >0
                    return _id.deleted_count
                else:
                    return make_response(
                        "{_id} nao encontrado".format(_id=_id), 404
                    )
            else:
                return make_response(
                    "Nome ou _id sao requeridos", 400
                )
        except Exception as e:
            return make_response(
                "usuario nao foi apagado", 403
            )
