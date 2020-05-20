from boavizinhanca_microservice.Model.mongo_conexion import ConexionMongo


class Proposta:
    def __init__(self, proposta_id, nome, descricao, item, solicitante, proprietario):
        self.proposta_id = proposta_id
        self.nome = nome
        self.descricao = descricao
        self.item = item
        self.solicitante = solicitante
        self.proprietario = proprietario

    def existe_propostas(self):
        return ConexionMongo.get_service(self.descricao, self.solicitante, self.proprietario)

    def procurar_proposta(self.nome):
        # Procurando no banco de dados pelo item
        conexion_db = ConexionMongo()
        res = conexion_db.get_service(nome=nome)
        return res
