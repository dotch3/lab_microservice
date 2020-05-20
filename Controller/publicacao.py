from flask import jsonify, make_response, abort
from Model.mongo_conexion import ConexionMongo


class Publicacao:
    def __init__(self, publicacao_id, nome, descricao, item, proprietario, estado):
        self.publicacao_id = publicacao_id
        self.nome = nome
        self.descricao = descricao
        self.item = item
        self.proprietario = proprietario
        self.estado = estado

    def get_publicacoes():
        # Connect database
        conexion_db = ConexionMongo()
        res = conexion_db.get_service(nome="Publicacoes")
        return res

    def get_publicacao(nome_publicacao):
        # Procurando no banco de dados pelo item
        conexion_db = ConexionMongo()
        res = conexion_db.get_service(nome=nome_publicacao)
        return res

    def add_publicacao(new_pub):
        publicacoes = get_publicacoes()
        publicacoes.append(new_pub)
