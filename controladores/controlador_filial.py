from telas.tela_filial import TelaFilial
from entidade.filial import Filial
from controladores.controlador_gerente_esp import ControladorGerenteEsp
from controladores.controlador_fun_comum_esp import ControladorFunComumEsp
from controladores.controlador_gerente import ControladorGerente


class ControladorFilial:

    def __init__(self, controlador_sistema, filial: Filial):
        self.__controlador_sistema = controlador_sistema
        self.__controlador_contrato = self.__controlador_sistema.controlador_contrato
        self.__controlador_gerente = ControladorGerente(controlador_sistema)
        self.__filial = filial
        self.__tela_filial = TelaFilial()

    @property
    def filial(self):
        return self.__filial

    @property
    def controlador_sistema(self):
        return self.__controlador_sistema
    
    @property
    def controlador_gerente(self):
        return self.__controlador_gerente

    def inicializa_sistema(self):
        lista_opcoes = {1: self.controlador_fun_comum_esp, 2: self.controlador_gerente_esp,
                        3: self.modificar_dados, 4: self.acessar_contratos,
                        5: self.listar_fun_ativos, 0: self.retornar}

        while True:
            opcao_escolhida = self.__tela_filial.mostra_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()

    def controlador_fun_comum_esp(self):
        ControladorFunComumEsp(self, self.__filial.funcionarios).inicializa_sistema()

    def controlador_gerente_esp(self):
        ControladorGerenteEsp(self, self.__filial.gerente).inicializa_sistema()

    def modificar_dados(self):
        # Realizando a chamada do menu de modificação
        opcao = self.__tela_filial.menu_modificacao()
        # sem midificacao
        if opcao == 0:
            return
        # escolheu um atributo para modificar
        else:
            # Checagem de CEP para a troca
            if opcao == 1:
                while True:
                    cep_novo = self.__tela_filial.pega_input('Digite o novo CEP: ', 'Controle de Filiais')
                    if self.__controlador_sistema.checagem_repeticao_cep(cep_novo):
                        cep_novo = self.__tela_filial.formata_cep(cep_novo)
                        break
                cep_antigo = self.__filial.cep
                self.__filial.cep = cep_novo
                self.__controlador_sistema.filial_dao.change_key(cep_antigo, cep_novo)
                self.atualizar_contratos(cep_antigo)
            # Checagem de cidade para troca
            if opcao == 2:
                while True:
                    cidade_nova = self.__tela_filial.pega_input('Digite a nova cidade: ', 'Controle de Filiais')
                    if self.__controlador_sistema.checagem_repeticao_cidade(cidade_nova):
                        break
                self.__filial.cidade = cidade_nova
                self.__controlador_sistema.filial_dao.update(self.__filial)

    def atualizar_contratos(self, cep):
        contratos = self.__controlador_contrato.contrato_dao.get_all()
        for contrato in contratos:
            contrato.filial = self.__filial
            self.__controlador_contrato.contrato_dao.update(contrato)

    def acessar_contratos(self):
        contratos = self.__controlador_contrato.contrato_dao.get_all()
        contratos_locais = []
        for contrato in contratos:
            if contrato.filial.cep == self.__filial.cep:
                contratos_locais.append(contrato)
        self.__controlador_contrato.listar_contrato(contratos_locais)

    def listar_fun_ativos(self):
        gerente = self.__controlador_sistema.filial_dao.get(self.__filial.cep).gerente
        lista_fun = self.__controlador_sistema.filial_dao.get(self.__filial.cep).funcionarios
        lista_listagem = []

        lista_listagem.append(self.__tela_filial.formata_listagem(gerente.nome, gerente.cpf,
                                                                  gerente.data_nasc, gerente.atividade))
        if len(lista_fun) > 0:
            for fun in lista_fun:
                if fun.atividade is True:
                    lista_listagem.append(self.__tela_filial.formata_listagem(fun.nome, fun.cpf,
                                                                              fun.data_nasc, fun.atividade))
        else:
            self.__tela_filial.mostra_mensagem('Lista de funcionários comuns vazia.')
        self.__tela_filial.listagem('Lista de funcionários ativos', lista_listagem)

    def retornar(self):
        self.__controlador_sistema.inicializa_sistema()
