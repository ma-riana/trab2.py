from abc import ABC
from dao import FunComumDAO
from dao.gerente_dao import GerenteDAO
from exception.repeticao_exp import Repeticao

class ControladorFuncionario(ABC):

    def __init__(self):
        self.__gerente_dao = GerenteDAO()
        self.__fun_comum_dao = FunComumDAO()

    @property
    def gerente_dao(self):
        return self.__gerente_dao

    @property
    def fun_comum_dao(self):
        return self.__fun_comum_dao

    def todos_funcionarios(self):
        funcionarios = []
        for fun in self.__gerente_dao.get_all():
            funcionarios.append(fun)
        for fun in self.__fun_comum_dao.get_all():
            funcionarios.append(fun)
        return funcionarios

    def repeticao_cpf(self, cpf):
        while True:
            try:
                funcionarios = self.todos_funcionarios()
                if funcionarios is not None:
                    for fun in funcionarios:
                        if fun.cpf == cpf:
                            raise Repeticao('CPF', cpf)
                return True
            except Repeticao:
                return False
