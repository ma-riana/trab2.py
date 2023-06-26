from telas.tela_cargo import TelaCargo
from entidade.cargo import Cargo
from dao.cargo_dao import CargoDAO


class ControladorCargo:

    def __init__(self, control_sistema):
        self.__cargo_dao = CargoDAO()
        self.__tela_cargo = TelaCargo()
        self.__control_sistema = control_sistema

    @property
    def cargo_dao(self):
        return self.__cargo_dao

    def incluir_cargo(self):
        dados_cargo = self.__tela_cargo.pega_dados_cargo()
        if dados_cargo is None:
            return
        novo_cargo = Cargo(dados_cargo["id"], dados_cargo["titulo"], dados_cargo["salario"])
        self.__cargo_dao.add(novo_cargo)

    def alterar_cargo(self):
        pass

    def listar_cargos_comuns(self):
        if len(self.__cargo_dao.get_all()) == 1: # se tiver apenas o gerente
            self.__tela_cargo.mostra_mensagem("A empresa ainda não possui cadastro de " +
                                              "cargos de funcionários comuns no sistema.")
        else:
            lista = []
            for cargo in self.__cargo_dao.get_all():
                if cargo.titulo != "Gerente":
                    lista.append(self.__tela_cargo.formata_listagem(cargo.id, cargo.titulo, cargo.salario))
                    self.__tela_cargo.listagem('Listagem de cargos', lista)

    def listar_todos_cargos(self):
        lista = []
        for cargo in self.__cargo_dao.get_all():
            lista.append(self.__tela_cargo.formata_listagem(cargo.id, cargo.titulo, cargo.salario))
        self.__tela_cargo.listagem('Listagem de cargos', lista)

    def listar_cargo(self, cargo: Cargo):
        lista = []
        self.__tela_cargo.formata_listagem(cargo.id, cargo.titulo, cargo.salario)
        self.__tela_cargo.listagem('Listagem de cargo', lista)

    def excluir_cargo(self):
        cargo = self.seleciona_cargo()
        if cargo is None:
            return
        self.__cargo_dao.remove(cargo.id)
        self.__tela_cargo.exclui_id(cargo.id)

    def seleciona_cargo(self):
        cargo_id = self.__tela_cargo.pega_cargo(self.__cargo_dao.get_all())
        if cargo_id is None:
            return cargo_id
        cargo = self.pega_cargo_por_id(cargo_id)
        return cargo

    def pega_cargo_por_id(self, id: int):
        for cargo in self.__cargo_dao.get_all():
            if cargo.id == id:
                return cargo

    def retornar(self):
        self.__control_sistema.inicializa_sistema()

    def abre_tela(self):
        lista_opcoes = {1: self.incluir_cargo, 2: self.alterar_cargo, 3: self.excluir_cargo,
                        4: self.listar_todos_cargos, 5: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__tela_cargo.mostra_opcoes()]()
