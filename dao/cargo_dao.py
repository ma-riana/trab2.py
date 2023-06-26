from dao.dict_dao import DictDAO
from entidade.cargo import Cargo


class CargoDAO(DictDAO):
    def __init__(self):
        super().__init__('cargos.pkl')
        # inicia já com algumas opções
        cargo1 = Cargo(0, "Gerente", 1000)
        cargo2 = Cargo(1, "Atendente", 600)
        cargo3 = Cargo(2, "Faxineiro interno", 800)
        self.add(cargo1)
        self.add(cargo2)
        self.add(cargo3)

    def add(self, cargo: Cargo):
        if((cargo is not None) and isinstance(cargo, Cargo) and isinstance(cargo.id, int)):
            super().add(cargo.id, cargo)

    def update(self, cargo: Cargo):
        if((cargo is not None) and isinstance(cargo, Cargo) and isinstance(cargo.id, int)):
            super().update(cargo.id, cargo)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)