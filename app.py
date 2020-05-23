from flask import render_template
from flask import Flask
from flask_restx import Api

from Resources.usuario import Usuario
from Resources.usuarioList import UsuarioList
from Resources.item import Item
from Resources.itemList import ItemList

# Create a Flask WSGI application
app_flask = Flask(__name__)
api = Api(app_flask,
          version="1.0",
          title="CRUD operations FIAP SW ENG Lab2",
          description="Laboratory for microservices",
          default='Test: uServices SW Eng',
          default_label='This is the swagger UI for API testing')

# Items
api.add_resource(ItemList, '/api/items')
api.add_resource(Item, '/api/item/<string:nome>')

# Users
routes = [
    '/api/usuario/<string:nome>',
    # '/api/item/update/<int:id>/<string:action>', # will need this for later - not MVP
]
api.add_resource(UsuarioList, '/api/usuarios')
api.add_resource(Usuario, *routes)


# @TODO crear los demas recursos listados

@app_flask.route('/home', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():

    return render_template('index.html')


@app_flask.route('/home/aux', methods=['GET', 'POST', 'DELETE', 'PUT'])
def home():
    return render_template('usuarios.html')


@app_flask.route('/api/items', methods=['GET'])
def items():
    return render_template('items.html')


@app_flask.route('/api/item/<string:nome>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def item_nome():
    return render_template('items.html')


@app_flask.route('/api/usuarios', methods=['GET'])
def usuarios():
    return render_template('usuarios.html')


@app_flask.route('/api/usuario/<string:nome>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def usuario_nome():
    return render_template('usuario.html')


if __name__ == '__main__':
    app_flask.run(host='0.0.0.0', port=5000, debug=True)
