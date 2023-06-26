from telas.tela_gerente import TelaGerente
from entidade.gerente import Gerente
from controladores.controlador_funcionario import ControladorFuncionario


class ControladorGerente(ControladorFuncionario):

    def __init__(self, controlador_sistema):
        super().__init__()
        self.__controlador_sistema = controlador_sistema
        self.__controlador_cargo = self.__controlador_sistema.controlador_cargo
        self.__tela_gerente = TelaGerente()
        self.__gerente_dao = super().gerente_dao

    @property
    def gerente_dao(self):
        return self.__gerente_dao

    def add_gerente(self):
        self.__tela_gerente.mostra_mensagem("\nPor favor, realize o cadastro do gerente na janela seguinte.")

        # Realizando a checagem de repetição de CPF do método super
        while True:
            dados_novo_gerente = self.__tela_gerente.pega_dados_cadastro()
            if self.repeticao_cpf(dados_novo_gerente['CPF']):
                break
            self.__tela_gerente.mostra_mensagem('CPF já cadastrado.')

        # Criação do Obj gerente e adição ao DAO
        obj_novo_gerente = Gerente(dados_novo_gerente['nome'], dados_novo_gerente['CPF'],
                                   dados_novo_gerente['data_nasc'])
        self.__gerente_dao.add(obj_novo_gerente)

        # Infomações constantes para todos os gerentes
        cargo_gerente = self.__controlador_cargo.cargo_dao.get(0)
        infos_gerencia = {'funcionario': obj_novo_gerente, 'empregador': 'Empresa',
                          'cargo': cargo_gerente, 'data_inicio': dados_novo_gerente['data_inicio']}
        return infos_gerencia, obj_novo_gerente

    def subs_cargo(self, filial):
        # Chamada do cadastro de gerente, definição da filial atual
        infos_gerencia, obj_novo_gerente = self.__controlador_sistema.controlador_gerente.add_gerente()

        # Realização do contrato
        dados_contrato = {'data_inicio': infos_gerencia['data_inicio'], 'cargo': infos_gerencia['cargo'],
                          'empregado': infos_gerencia['funcionario'], 'filial': filial,
                          'empregador': infos_gerencia['empregador']}
        self.__controlador_sistema.controlador_contrato.incluir_contrato(dados_contrato)

        # Update do DAO da filial com as novas informações
        filial.gerente = infos_gerencia['funcionario']
        self.__controlador_sistema.filial_dao.update(filial)
        return obj_novo_gerente
