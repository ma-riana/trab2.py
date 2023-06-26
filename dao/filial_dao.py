from dao.dict_dao import DictDAO
from entidade.filial import Filial


class FilialDAO(DictDAO):
    def __init__(self):
        super().__init__('filiais.pkl')

    def add(self, filial: Filial):
        if((filial is not None) and isinstance(filial, Filial) and isinstance(filial.cep, str)):
            super().add(filial.cep, filial)

    def update(self, filial: Filial):
        if((filial is not None) and isinstance(filial, Filial) and isinstance(filial.cep, str)):
            super().update(filial.cep, filial)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if(isinstance(key, str)):
            return super().remove(key)