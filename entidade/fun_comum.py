from entidade.funcionario import Funcionario


class FunComum(Funcionario):
    def __init__(self, nome: str, cpf: str, data_nasc: str, atividade=True):
        super().__init__(nome, cpf, data_nasc, atividade)