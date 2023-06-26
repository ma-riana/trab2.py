from entidade.filial import Filial
from controladores.controlador_filial import ControladorFilial
from controladores.controlador_gerente import ControladorGerente
from controladores.controlador_fun_comum import ControladorFunComum
from controladores.controlador_contrato import ControladorContrato
from controladores.controlador_cargo import ControladorCargo
from telas.tela_sistema import TelaSistema
from exception.repeticao_exp import Repeticao
from exception.nao_existe_exp import NaoExistencia
from dao import FilialDAO


class ControladorSistema:

    def __init__(self):
        self.__tela_sistema = TelaSistema()
        self.__controlador_cargo = ControladorCargo(self)
        self.__controlador_gerente = ControladorGerente(self)
        self.__controlador_fun_comum = ControladorFunComum()
        self.__controlador_contrato = ControladorContrato(self)
        self.__filial_dao = FilialDAO()

    @property
    def filial_dao(self):
        return self.__filial_dao

    @property
    def controlador_contrato(self):
        return self.__controlador_contrato

    @property
    def controlador_gerente(self):
        return self.__controlador_gerente

    @property
    def controlador_fun_comum(self):
        return self.__controlador_fun_comum

    @property
    def controlador_cargo(self):
        return self.__controlador_cargo

    def inicializa_sistema(self):
        lista_opcoes = {1: self.adicionar_filial, 2: self.excluir_filial,
                        3: self.modificar_filial, 4: self.listar,
                        0: self.sair}

        while True:
            opcao_escolhida = self.__tela_sistema.mostra_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()

    def adicionar_filial(self):
        dados_nova_filial = self.__tela_sistema.pega_dados_cadastro()
        if dados_nova_filial is None:
            return
        # Checagem de repetição
        dados_nova_filial = self.checagem_repeticao(dados_nova_filial)

        infos_gerencia, obj = self.__controlador_gerente.add_gerente()
        nova_filial = Filial(dados_nova_filial['cep'], dados_nova_filial['cidade'], infos_gerencia['funcionario'])
        self.__filial_dao.add(nova_filial)

        dados_contrato = {'data_inicio': infos_gerencia['data_inicio'], 'cargo': infos_gerencia['cargo'],
                          'empregado': infos_gerencia['funcionario'], 'filial': nova_filial,
                          'empregador': infos_gerencia['empregador']}
        self.__controlador_contrato.incluir_contrato(dados_contrato)

        self.__tela_sistema.mostra_mensagem('Filial cadastrada com sucesso.')

    def excluir_filial(self):
        filial = self.busca_por_cep('Exclusão de filial por CEP')
        if filial is None:
            return
        else:
            self.__filial_dao.remove(filial.cep)
            self.__tela_sistema.mostra_mensagem('Filial excluída com sucesso')

    def modificar_filial(self):
        filial = self.busca_por_cep('Identificação de filial por CEP')
        if filial is None:
            return
        else:
            ControladorFilial(self, filial).inicializa_sistema()

    def listar(self):
        if len(self.__filial_dao.get_all()) > 0:
            lista_listagem = []
            for _ in self.__filial_dao.get_all():
                lista_listagem.append(self.__tela_sistema.formata_listagem(_.cep, _.cidade, _.gerente.nome))
            self.__tela_sistema.listagem('Listagem de Filiais', lista_listagem)
        else:
            self.__tela_sistema.mostra_mensagem('Lista vazia.\n')
        
    def checagem_repeticao(self, dados_nova_filial):
        while True:
            try:
                for _ in self.__filial_dao.get_all():
                    if _.cep == dados_nova_filial['cep']:
                        raise Repeticao('CEP', dados_nova_filial['cep'])
                for _ in self.__filial_dao.get_all():
                    if _.cidade == dados_nova_filial['cidade']:
                        raise ValueError
                return dados_nova_filial
            except Repeticao:
                self.__tela_sistema.mostra_mensagem(Repeticao('CEP', dados_nova_filial['cep']).msg())
                dados_nova_filial = self.__tela_sistema.pega_dados_cadastro()
            except ValueError:
                self.__tela_sistema.mostra_mensagem(Repeticao('Cidade', dados_nova_filial['cidade']).msg())
                dados_nova_filial = self.__tela_sistema.pega_dados_cadastro()

    def busca_por_cep(self, msg):
        while True:
            try:
                cep_buscado = self.__tela_sistema.pega_cep(msg)
                if cep_buscado is None:
                    return None
                for _ in self.__filial_dao.get_all():
                    if _.cep == cep_buscado:
                        return _
                raise NaoExistencia
            except NaoExistencia:
                self.__tela_sistema.mostra_mensagem('Filial não encontrada. Tente novamente.')

    def sair(self):
        exit(0)
