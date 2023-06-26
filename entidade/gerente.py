from entidade.funcionario import Funcionario
from datetime import date


class Gerente(Funcionario):
    def __init__(self, nome: str, cpf: str, data_nasc: date, atividade=True):
        super().__init__(nome, cpf, data_nasc, atividade)
        self.__contratos = []

    @property
    def contratos(self):
        return self.__contratos

    def add_contrato(self, contrato):
        self.__contratos.append(contrato)

    def rem_contrato(self, contrato):
        self.__contratos.remove(contrato)
