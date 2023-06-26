from entidade.gerente import Gerente
from entidade.fun_comum import FunComum


class Filial:
    def __init__(self, cep: str, cidade: str, gerente: Gerente):
        self.__cep = cep
        self.__cidade = cidade
        self.__gerente = gerente
        self.__funcionarios = []

    @property
    def cep(self):
        return self.__cep

    @property
    def cidade(self):
        return self.__cidade

    @property
    def gerente(self):
        return self.__gerente

    @property
    def funcionarios(self):
        return self.__funcionarios

    @cep.setter
    def cep(self, cep):
        self.__cep = cep

    @cidade.setter
    def cidade(self, cidade):
        self.__cidade = cidade

    @gerente.setter
    def gerente(self, gerente):
        self.__gerente = gerente

    def add_fun_comum(self, fun_comum: FunComum):
        self.__funcionarios.append(fun_comum)

    def setter_funcionarios(self, cpf_novo, fun_comum: FunComum):
        for _ in self.__funcionarios:
            if _.cpf == fun_comum.cpf:
                self.rem_fun_comum(_)
                fun_comum.cpf = cpf_novo
                self.add_fun_comum(fun_comum)

    def rem_fun_comum(self, fun_comum: FunComum):
        self.__funcionarios.remove(fun_comum)
