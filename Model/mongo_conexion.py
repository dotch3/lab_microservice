from datetime import datetime
from pymongo import MongoClient
from flask import Flask
from flask import jsonify, make_response, abort


class ConexionMongo:

    def __init__(self, client, service, collection):
        self.client = client
        self.service = service
        self.collection = collection

    def __repr__(self):
        return f"<MongoConnClient:{self.client}, database: {self.service} , collection {self.collection}.>"

    @staticmethod
    def create_conexion(db_inst):
        """
        Thie will create the mongo db connexion
        :param db_inst: str The location of the database: local or remote
        :return:  mongodb client conexion
        """
        print("create_conexion")
        if db_inst == "local":
            mongo_client = MongoClient("mongodb://localhost:27017/")  # Local
        elif db_inst == "docker":
            mongo_client = "other config-maybe"  # Docker
        db_conn = mongo_client[db_inst]
        return db_conn

    @staticmethod
    def get_dict_from_mongodb(db_inst, collection):
        """
        This method will iterate all the data found in a collection, jsonify them and return the items
        :param db_inst: the local or remote mongo database instance
        :param collection: The mongo collection to use
        :return: List jsonified of items
        """
        db_conn = ConexionMongo.create_conexion(db_inst)
        print("get_dict_from_mongodb")
        items_db = db_conn[collection].find()
        # Dictionary of items
        ITEMS = {}
        for i in items_db:
            # Let's get the value of the _id and use it for item_id
            object_id = i.pop('_id')
            new_id = str(object_id)
            # Using the Id for the dictionary
            ITEMS[new_id] = i
        print(ITEMS)
        print("End of get_dict_from_mongodb ")
        return ITEMS

    @classmethod
    def get_all_data(cls, db_inst=None, collection=None):
        """
        This method will connect to the mongo db and return the data found in the collection
        :param db_inst: the local or remote mongo database instance
        :param collection: The mongo collection to use
        :return: List jsonified of Items found in the mongo db:collection
        """
        print(f"get_all_data for collection \"{collection}\"")
        # In order to jsonify the dictionary, is needed to call it inside the app_context
        app = Flask(__name__)
        if not db_inst:
            db_inst='local'
        with app.app_context():

            ITEMS = ConexionMongo.get_dict_from_mongodb(db_inst, collection)
            my_dict = []
            for key in sorted(ITEMS.keys()):
                temp = [key, ITEMS[key]]
                my_dict.append(temp)
            print(my_dict)
            dict_items = jsonify(my_dict)
            qtd = len(my_dict)
            content_range = "items 0-" + str(qtd) + "/" + str(qtd)
            # Configuring the headers for the response
            dict_items.headers['Access-Control-Allow-Origin'] = '*'
            dict_items.headers['Access-Control-Expose-Headers'] = 'Content-Range'
            dict_items.headers['Content-Range'] = content_range
            print("End of get_data_service ")
            return dict_items

    @classmethod
    def read_one(cls, db_inst, collection, item_name):
        """
        This will find if an item is part of the mongodb collection
        :param db_inst: the local or remote mongo database instance
        :param collection: The mongo collection to use
        :param item_name: the name of the item to find
        :return: the item if this is found
        """
        ITEMS = ConexionMongo.get_dict_from_mongodb(db_inst, collection)
        if item_name in ITEMS:
            item = ITEMS.get(item_name)
        else:
            abort(
                404, "Record  com nome {item_name} nao foi encontrada".format(
                    item_name=item_name)
            )
        return item
