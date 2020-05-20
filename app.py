import os
import connexion
from flask import render_template
from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api

from Resources.item import Item

# Defining the path for the templates
APP_PATH = os.path.dirname(os.path.abspath(__file__))

# TEMPLATE_PATH = os.path.join(APP_PATH, 'templates/')
# TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, 'usuarios.html')

# print(APP_PATH)
# print(TEMPLATE_PATH)

# Creating the conexion with app flask
app = connexion.App(__name__, specification_dir=APP_PATH)


app.add_api('swagger.yml')
CORS(app.app, resources=r'/api/*', methods=['GET'])

# Adding more services

app_flask = Flask(__name__)
api = Api(app_flask)
# Items
api.add_resource(Item, '/item/<string:nome>')
api.add_resource(ItemList, '/items')
# Users
api.add_resource(User, '/user/<string:nome>')
api.add_resource(UserList, '/users')
# @TODO crear los demas recursos listados
# Register new Users/Proposta/Publicacao/Negociacao

# api.add_resource(Proposta, '/proposta')
# api.add_resource(Publicacao, '/publicacao')
# api.add_resource(Negociacao, '/negociacao')
# api.add_resource(UserRegister, '/register')


@ app.route('/')
def home():
    # Load the home page
    return render_template('home.html')


@ app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')


@ app.route('/usuariosMongoLocal')
def otros():
    return render_template('usuarios.html')


@ app.route('/items')
def items():
    return render_template('usuarios.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
