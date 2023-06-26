from dao.dict_dao import DictDAO
from entidade.fun_comum import FunComum


class FunComumDAO(DictDAO):
    def __init__(self):
        super().__init__('funcionarios_comuns.pkl')

    def add(self, fun_comum: FunComum):
        if((fun_comum is not None) and isinstance(fun_comum, FunComum) and isinstance(fun_comum.cpf, str)):
            super().add(fun_comum.cpf, fun_comum)

    def update(self, fun_comum: FunComum):
        if((fun_comum is not None) and isinstance(fun_comum, FunComum) and isinstance(fun_comum.cpf, str)):
            super().update(fun_comum.cpf, fun_comum)

    def get(self, key:str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key:str):
        if(isinstance(key, str)):
            return super().remove(key)
