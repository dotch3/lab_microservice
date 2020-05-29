import socket
import os
from datetime import datetime
from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from flask import Flask
from flask import jsonify, make_response, abort


class ConexionMongo:
    hostname = ""
    host_ip = ""

    def __init__(self, client, service, collection):
        self.client = client
        self.service = service
        self.collection = collection

    def __repr__(self):
        return f"<MongoConnClient:{self.client}, database: {self.service} , collection {self.collection}.>"

    @staticmethod
    def connect_first_time():
        """
        will check the databases on the mongo server
        :return: bool Creation of collections succeeded
        """
        # mongo_client = MongoClient(hostname, 27017)
        print(f"Creating the database and collections")
        connected = False
        try:
            print("Try first time")
            db_name = os.environ['MONGODB_DATABASE']
            uri = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + \
                os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + \
                ':27017/' + os.environ['MONGODB_DATABASE']

            mongo_client = MongoClient(uri)
            db_names = mongo_client.list_database_names()
            print(db_names)
            # Create database
            db_instance = mongo_client[db_name]
            # Cretae the collections and inserting at least one record to have the collections
            collection_usuarios = db_instance["items"]
            result_item = collection_usuarios.insert_one(
                {"nome": "Furadeira", "descricao": "Furadeira 110/220V", "data_inicio": str(datetime.now()),
                 "data_final": "",
                 "status": "Livre"})
            print(result_item.inserted_id)
            collection_items = db_instance["usuarios"]
            result_user = collection_items.insert_one(
                {"nome": "Joaocito", "sobrenome": "Silva", "email": "jsilva@test.com", "address": "Rua Ipiranga 110",
                 "username": "jsilva", "password": "abc123", "celular": "1197332232",
                 "last-update": str(datetime.now())})
            print(result_user.inserted_id)
            db_names = mongo_client.list_database_names()
            print(db_names)
            col = mongo_client[db_name].list_collection_names()
            for c in col:
                print(c)
            if "admin" in db_names:
                connected = True

        except Exception as e:
            print(f"ERROR START:  Cannot connect to mongo {e}")

    @classmethod
    def create_conexion(cls, db_inst):
        """
        This will create the mongo db connexion
        :param db_inst: str The location of the database: local or remote
        :param f_time: bool The flag run the create_conexion and create database
        :return:  mongodb client conexion
        """
        print("create_conexion")

        uri = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + \
            os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + \
            ':27017/' + os.environ['MONGODB_DATABASE']

        # mongo_client = PyMongo(app_flask)
        mongo_client = MongoClient(uri)
        db_conn = mongo_client[db_inst]

        # res_connexion = ConexionMongo.connect_first_time()
        # print(res_connexion)

        return db_conn

    @classmethod
    def get_all_data(cls, db_inst=None, collection=None):
        """
        This method will connect to the mongo db and return the data found in the collection
        :param db_inst: the local or remote mongo database instance
        :param collection: The mongo collection to use
        :return: List jsonified of Items found in the mongo db:collection
        """
        print(f"get_all_data for collection \"{collection}\" ")
        # In order to jsonify the dictionary, is needed to call it inside the app_context
        app = Flask(__name__)
        if not db_inst:
            db_inst = "admin"
        with app.app_context():
            ITEMS = ConexionMongo.get_dict_from_mongodb(
                db_inst=db_inst, collection=collection, mode="get_all")
            # Need code for handle exceptions of 0 data.
            my_dict = []
            for key in sorted(ITEMS.keys()):
                temp = [key, ITEMS[key]]
                my_dict.append(temp)
            dict_items = jsonify(my_dict)
            qtd = len(my_dict)
            content_range = "items 0-" + str(qtd) + "/" + str(qtd)
            # Configuring the headers for the response
            dict_items.headers['Access-Control-Allow-Origin'] = '*'
            dict_items.headers['Access-Control-Expose-Headers'] = 'Content-Range'
            dict_items.headers['Content-Range'] = content_range
            print("End of get_data_service ")
            return dict_items

    @staticmethod
    def get_dict_from_mongodb(db_inst, collection, mode="get_all", nome=None, _id=None):
        """
        This method will iterate all the data found in a collection, jsonify them and return the items
        :param db_inst: the local or remote mongo database instance
        :param collection: The mongo collection to use
        :param mode: The mode to perform the mongo queries: find;findOne;
        :param nome: The name of the item to find
        :param _id: The id of the item to find
        :return: List jsonified of items
        """
        ITEMS = {}
        items_db = ""
        mongo_conn = ConexionMongo.create_conexion(db_inst=db_inst)
        print(str(mongo_conn))
        if mode == "get_all":
            try:
                print("get_dict_from_mongodb::get_all")
                # This is the key!!!
                print("test")
                items_db = mongo_conn[collection].find()
                print("test")
                print("Working with the data retrieved...")
                print(items_db)
                print(type(items_db))
                for i in items_db:
                    print(i)
                    # Let's get the value of the _id and use it for item_id
                    object_id = i.pop('_id')
                    new_id = str(object_id)
                    i["_id"] = new_id
                    # Using the Id for the dictionary
                    ITEMS[new_id] = i
                # Return a list
                print(ITEMS)
                print("End of get_dict_from_mongodb ")
                return ITEMS

            except Exception as e:
                print(f"ERROR MONGO:  get_dict_from_mongodb::end get_all {e}")

        elif mode == "get_one":
            print("get_dict_from_mongodb::get_one")
            print(nome)
            try:
                # Searching by nome
                if nome and not _id:
                    print("by nome")
                    query = {"nome": nome}
                    print(query)
                    items_db = mongo_conn[collection].find_one(query)
                    print(type(items_db))
                    if "ObjectId" in str(type(items_db)):
                        if ObjectId.is_valid(items_db["_id"]):
                            print("Encontrou o documento {}...enviando...".format(
                                items_db["_id"]))
                            return items_db
                    elif "dict" in str(type(items_db)):
                        print("dictionary")
                        print("dictionary " + str(items_db.get("_id")))
                        return items_db
                    else:
                        print(
                            f"Nao se encontra o documento com esse nome {nome}".format(nome=nome))
                        return False

                elif _id:
                    print("by ID")
                    # Using the ObjectId class for BSON objects. Kaboom!w
                    find_id = ObjectId(_id)
                    query = {"_id": find_id}
                    # Return a dictionary
                    items_db = mongo_conn[collection].find_one(query)
                    print("Encontrou o documento {}, enviando".format(
                        items_db["_id"]))
                    if ObjectId.is_valid(items_db["_id"]):
                        print("The object is a BSON")
                        return items_db
                    else:
                        return make_response("Record  com _id {_id} nao foi encontrada".format(
                            _id=_id), 404)
            except Exception as e:
                print(f"ERROR MONGO:  get_dict_from_mongodb::get_one {e}")
        elif mode == "create":
            print("get_dict_from_mongodb::create")
            try:
                # Searching by nome
                if nome and not _id:
                    print("by nome")
                    query = {"nome": nome}
                    print(query)
                    items_db = mongo_conn[collection].find_one(query)

                    if items_db:
                        print(items_db["_id"])
                        return items_db
                    else:
                        return False
            except Exception as e:
                print(f"ERROR MONGO:  get_dict_from_mongodb::create {e}")

    @staticmethod
    def add_document(db_inst, collection, python_dict):
        """
        This will add a new document to the collection
        :param db_inst: the local or remote database
        :param collection: the mongodb collection where to add the document
        :param python_dict: The python dictionary object to be added as mongo document
        :return: InsertOneResult a mongo result
        """
        try:
            print("creating document")
            mongo_conn = ConexionMongo.create_conexion(db_inst)
            result_object = mongo_conn[collection].insert_one(python_dict)
            return result_object
        except Exception as e:
            print(f"ERROR MONGO:  create_document  {e}")

    @staticmethod
    def update_document(db_inst, collection, query, values_set):
        """
        Funtion to dupdate a mongoDB document using the $set operator
        :param db_inst: The  local or remote mongoDB
        :param collection: the collection to use for the operation
        :param query: the query for find the document
        :param values_set: the values to use for the update
        :return:
        """
        try:
            print("updating document ")
            mongo_conn = ConexionMongo.create_conexion(db_inst)
            result = mongo_conn[collection].update_one(query, values_set)
            # print ("acknowledged:", result.acknowledged)
            # # integer of the number of docs modified
            # print ("number of docs updated:", result.modified_count)
            # # dict object with more info on API call
            # print ("raw_result:", result.raw_result)
            if "None" not in str(type(result)):
                print("mongo check results:", result.raw_result)
                if result.modified_count > 0:
                    print("documento atualizado ")
                else:
                    print("not found/updated")
            return result

        except Exception as e:
            print(f"ERROR MONGO:  update_document  {e}")

    @staticmethod
    def remove_document(db_inst, collection, query):
        """
        This will find and remove a document inside a collection
        :param db_inst:the local or remote mongodb location
        :param collection: the mongodb collection to use
        :param query: the mongoquery
        :return:  mongodbResults
        """
        # document matching this query will get deleted
        # some_query = {"target field": "target value"}

        try:
            print("deleting document ")
            print(query)
            mongo_conn = ConexionMongo.create_conexion(db_inst)
            result = mongo_conn[collection].find_one_and_delete(query)
            # when is not find and deleted , the response is None
            # When find and deleted, the response is a
            # {'_id': ObjectId('5ec6ebfe69ee0ddd8088a495'), 'nome': '
            # ObjectId -> result["_id"]) = 5ec6ebfe69ee0ddd8088a495
            print("Mongo DeleteResult")
            print("class", type(result), "value ", str(result))
            if "None" not in str(type(result)):
                if ObjectId.is_valid(result["_id"]):
                    print("document deleted " + str(result["_id"]))
            else:
                print("not deleted returning None")
            return result
        except Exception as e:
            print(f"ERROR MONGO:  remove_document  {e}")

    @staticmethod
    def read_one(db_inst, collection, item_name):
        """
        This will find if an item is part of the mongodb collection
        :param db_inst: the local or remote mongo database instance
        :param collection: The mongo collection to use
        :param item_name: the name of the item to find
        :return: the item if this is found
        """
        item = ""
        ITEMS = ConexionMongo.get_dict_from_mongodb(
            db_inst, collection, mode="get_one")
        if item_name in ITEMS:
            item = ITEMS.get(item_name)
        else:
            abort(
                404, "Record  com nome {item_name} nao foi encontrada".format(
                    item_name=item_name)
            )
        return item

    # Improved Methods to manipulate the data retrieved from MongoDB queries
