from flask import Flask, request, render_template
from flask_restx import Api

from Model.mongo_conexion import ConexionMongo
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
api.add_resource(Item, '/api/item<data>')

api.add_resource(UsuarioList, '/api/usuarios')
api.add_resource(Usuario, '/api/usuario<data>')


@app_flask.route('/home')
def index():
    print("working with methods on Usuarios object")

    return render_template('index.html')


@app_flask.route('/api/usuario', methods=['GET', 'POST', 'PUT', 'DELETE'])
def crud_usuario():
    print("Checking the CRUD operations for items!")
    if request.method == 'POST':
        req_usuario = request.get_json()
        user = Usuario()
        user.post(req_usuario)
        print("Data result POST ", req_usuario)

    elif request.method == 'GET':
        req_usuario = request.get_json()
        print("GET", req_usuario['nome'])

        user = Usuario()
        user.get(req_usuario['nome'])
        print("Data result GET ", req_usuario)

    elif request.method == 'PUT':
        req_usuario = request.get_json()
        print("PUT", req_usuario['nome'])

        user = Usuario()
        user.put(req_usuario)


    elif request.method == 'DELETE':
        req_usuario = request.get_json()
        print("DELETE", req_usuario['nome'])

        user = Usuario()
        user.delete(req_usuario['nome'])

    return render_template('index.html')


@app_flask.route('/api/item', methods=['GET', 'POST', 'PUT', 'DELETE'])
def crud_item():
    print("Checking the CRUD operations for items!")
    if request.method == 'POST':
        req_item = request.get_json()
        item = Item()
        item.post(req_item)


    elif request.method == 'GET':
        req_item = request.get_json()
        item = Item()
        item.get(req_item['nome'])


    elif request.method == 'PUT':
        req_item = request.get_json()
        item = Item()
        item.put(req_item)


    elif request.method == 'DELETE':
        req_item = request.get_json()
        item = Item()
        item.delete(req_item['nome'])

    return render_template('index.html')


@app_flask.route('/api/items', methods=['GET'])
def items():
    print("getting all items")
    return render_template('index.html')


@app_flask.route('/api/usuarios', methods=['GET'])
def usuarios():
    print("getting all usuarios")
    return render_template('index.html')

#
# @app_flask.before_first_request
# def create_collections():
#     print("This function will run once")
#     try:
#         ConexionMongo.connect_first_time()
#     except Exception as e:
#         print(f"ERROR MONGO:  Cannot connect to mongo {e}")


if __name__ == '__main__':
    app_flask.run(host='0.0.0.0', port=5000, debug=True)
