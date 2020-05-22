from Model.mongo_conexion import ConexionMongo


# Clase Negociacao realizado
class Negociacao:
    TYPES = ("item", "service")

    def __init__(self, neg_id, descricao, proprietario, solicitante, neg_requerido):
        self.neg_id = neg_id
        self.descricao = descricao
        self.proprietario = proprietario
        self.solicitante = solicitante
        self.neg_requerido = neg_requerido

    def __repr__(self):
        return f"<Negociacao requerida: {self.neg_requerido} ID:{self.neg_id}, {self.descricao}, realizado entre " \
               f"proprietario {self.proprietario} e {self.solicitante}>"

    # Factory applicado
    @classmethod
    def emprestimo_item(cls, neg_id, descricao, proprietario, solicitante):
        return Negociacao(neg_id, descricao, proprietario, solicitante, Negociacao.TYPES[0])

    # Factory applicado
    @classmethod
    def professional_service(cls, neg_id, descricao, proprietario, solicitante):
        return Negociacao(neg_id, descricao, proprietario, solicitante, Negociacao.TYPES[1])

    def procurar_service_prestado(self):
        return ConexionMongo.get_service(self.descricao, self.proprietario, self.solicitante)


svcItem = Negociacao.emprestimo_item(1, "desc_item", "Joao", "Lucas")
svcProf = Negociacao.professional_service(
    10, "desc_prof_serv", "Marcos", "Matheus")

print(svcItem)
print(svcProf)
