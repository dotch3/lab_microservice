from flask import Flask, request, render_template
from flask_restx import Api

from Model.mongo_conexion import ConexionMongo
from Resources.usuario import Usuario
from Resources.usuarioList import UsuarioList
from Model.usuario_model import UsuarioModel
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
    '/api/usuario',
    # '/api/item/update/<int:id>/<string:action>', # will need this for later - not MVP
]
api.add_resource(UsuarioList, '/api/usuarios')
api.add_resource(Usuario, '/api/usuario<data>')


# @TODO crear los demas recursos listados


@app_flask.route('/api/usuario', methods=['GET', 'POST', 'PUT', 'DELETE'])
def crud_usuario():
    print("entrou!")
    if request.method == 'POST':
        req_usuario = request.get_json()
        print(req_usuario['nome'])

        user = Usuario()
        user.post(req_usuario)

        print("Data result POST ", req_usuario)
    elif request.method == 'GET':
        req_usuario = request.get_json()
        print(req_usuario['nome'])
        user = Usuario()
        user.get(req_usuario['nome'])
        print("Data result GET ", req_usuario)
    elif request.method == 'PUT':
        req_usuario = request.get_json()
        print(req_usuario['nome'])
        user = Usuario()
        user.put(req_usuario)
        print("Data result PUT ", req_usuario)
    elif request.method == 'DELETE':
        req_usuario = request.get_json()

        user = Usuario()
        user.delete(req_usuario['nome'])

    return render_template('index.html')


@app_flask.route('/home')
def index():
    print("working with methods on Usuarios object")

    return render_template('index.html')



@app_flask.route('/api/items', methods=['GET'])
def items():
    print("getting all items")
    return render_template('items.html')
#
#
# @app_flask.route('/api/item/<string:nome>', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def item_nome():
#     print("working with methods on Item object")
#     return render_template('items.html')

#
@app_flask.route('/api/usuarios', methods=['GET'])
def usuarios():
    print("getting all usuarios")
    return render_template('index.html')


#
# @app_flask.before_first_request
# def create_collections():
#     print("This function will run once")
#     res = ConexionMongo.connect_first_time()
#     print(res)


if __name__ == '__main__':
    app_flask.run(host='0.0.0.0', port=5000, debug=True)
