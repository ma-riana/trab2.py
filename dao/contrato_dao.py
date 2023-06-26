from dao.dict_dao import DictDAO
from entidade.contrato import Contrato


class ContratoDAO(DictDAO):
    def __init__(self):
        super().__init__('contratos.pkl')

    def add(self, contrato: Contrato):
        if (contrato is not None) and isinstance(contrato, Contrato):
            super().add(contrato.empregado.cpf, contrato)

    def update(self, contrato: Contrato):
        if (contrato is not None) and isinstance(contrato, Contrato):
            super().update(contrato.empregado.cpf, contrato)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if(isinstance(key, str)):
            return super().remove(key)