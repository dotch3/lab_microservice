import os
import connexion
from flask import render_template
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields

from Resources.usuario import Usuario
from Resources.usuarioList import UsuarioList
from Resources.item import Item
from Resources.itemList import ItemList


# Defining the path for the templates
# APP_PATH = os.path.dirname(os.path.abspath(__file__))

# Creating the conexion with app flask
# app = connexion.App(__name__, specification_dir=APP_PATH)

# app.add_api('swagger.yml')
# CORS(app.app, resources=r'/api/*',
#      methods=['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE'])


# Create a Flask WSGI application
app_flask = Flask(__name__)
api = Api(app_flask,
          version="1.0",
          title="CRUD operations FIAP SW ENG Lab2",
          description="Laboratory for microservices",
          default='Test: uServices SW Eng',
          default_label='This is the swagger UI for API testing')

# Items
api.add_resource(Item, '/api/item/<string:nome>')
api.add_resource(ItemList, '/api/items')
# Users
api.add_resource(Usuario, '/api/usuario/<string:nome>')
api.add_resource(UsuarioList, '/api/usuarios')
# @TODO crear los demas recursos listados


@ app_flask.route('/home', methods=['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE'])
def home():
    return render_template('index.html')


@ app_flask.route('/api/items', methods=['GET'])
def items():
    return "You said"


@ app_flask.route('/api/item/<string:nome>', methods=['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE'])
def item_nome():
    return render_template('items.html')


@ app_flask.route('/api/usuarios', methods=['GET'])
def usuarios():
    return render_template('usuarios.html')


@ app_flask.route('/api/usuario/<string:nome>', methods=['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE'])
def usuario_nome():
    return render_template('items.html')


if __name__ == '__main__':
    app_flask.run(host='0.0.0.0', port=5000, debug=True)
