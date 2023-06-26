from telas.tela_gerente import TelaGerente
from controladores.controlador_funcionario import ControladorFuncionario


class ControladorGerenteEsp(ControladorFuncionario):

    def __init__(self, controlador_filial, gerente):
        super().__init__()
        self.__controlador_filial = controlador_filial
        self.__controlador_sistema = self.__controlador_filial.controlador_sistema
        self.__controlador_contrato = self.__controlador_sistema.controlador_contrato
        self.__tela_gerente = TelaGerente()
        self.__gerente = gerente

    def inicializa_sistema(self):
        lista_opcoes = {1: self.modificar_dados, 2: self.demitir,
                        3: self.listar_contratos, 4: self.acessar_contrato,
                        0: self.retornar}

        while True:
            opcao_escolhida = self.__tela_gerente.mostra_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()

    def modificar_dados(self):
        # Chamada do menu de modificação (apenas possível quando uma filial já está selecionada)
        opcao = self.__tela_gerente.menu_modificacao()
        # nao ocorrera modificacao
        if opcao == 0:
            return
        # ocorrera modificacao
        else:
            # modificacao de atributo usado como chave
            contrato = self.__controlador_contrato.contrato_dao.get(self.__gerente.cpf) # pega antes de modificar o cpf
            if opcao == 2:
                # Checagem de repetição de CPF durante a troca
                while True:
                    novo_cpf = self.__tela_gerente.pega_cpf('Digite o novo CPF: ')
                    if self.repeticao_cpf(novo_cpf):
                        break
                    else:
                        self.__tela_gerente.mostra_mensagem('CPF já cadastrado.')
                # Atualização do DAO. Cópia necessária pois é a modificação da chave
                super().gerente_dao.remove(self.__gerente.cpf)
                self.__controlador_contrato.contrato_dao.remove(contrato.empregado.cpf)
                self.__gerente.cpf = novo_cpf
                contrato.empregado = self.__gerente
                super().gerente_dao.add(self.__gerente)
                self.__controlador_contrato.contrato_dao.add(contrato)

            # modificacao de outros atributos
            else:
                if opcao == 1:
                    novo_nome = self.__tela_gerente.pega_nome("Digite o novo nome:", 'Modificação de dados.')
                    self.__gerente.nome = novo_nome
                elif opcao == 3:
                    nova_data_nasc = self.__tela_gerente.pega_data('Data de nascimento:')
                    if nova_data_nasc is None:
                        return
                    self.__gerente.data_nasc = nova_data_nasc
                super().gerente_dao.update(self.__gerente)
                contrato.empregado = self.__gerente
                self.__controlador_contrato.contrato_dao.update(contrato)
            # atualizacao aplicada apos qualquer modificacao
            filial = self.__controlador_filial.filial
            filial.gerente = self.__gerente
            self.__controlador_sistema.filial_dao.update(filial)

    def demitir(self):
        # Cadastro de novo gerente após a demissão do anterior
        self.__tela_gerente.mostra_mensagem("Cadastre um novo gerente antes de demitir o anterior")
        self.subs_cargo()
        #super().gerente_dao.update(gerente)
        self.__tela_gerente.mostra_mensagem('Gerente demitido com sucesso.')

    def subs_cargo(self):
        # Chamada do cadastro de gerente, definição da filial atual
        infos_gerencia, obj = self.__controlador_sistema.controlador_gerente.add_gerente()
        filial = self.__controlador_contrato.pega_contrato_por_cpf(self.__gerente.cpf).filial

        # Realização do contrato
        dados_contrato = {'data_inicio': infos_gerencia['data_inicio'], 'cargo': infos_gerencia['cargo'],
                          'empregado': infos_gerencia['funcionario'], 'filial': filial,
                          'empregador': infos_gerencia['empregador']}
        self.__controlador_contrato.incluir_contrato(dados_contrato)

        # Update do DAO da filial com as novas informações
        self.__gerente.atividade = False
        super().gerente_dao.update(self.__gerente)
        self.__controlador_contrato.demitir(self.__gerente)

        filial.gerente = infos_gerencia['funcionario']
        self.__gerente = filial.gerente
        super().gerente_dao.add(self.__gerente)
        self.__controlador_sistema.filial_dao.update(filial)

    def listar_contratos(self):
        # Listagem de contratos realizados durante a gerência
        if len(self.__gerente.contratos) > 0:
            lista = []
            for contrato in self.__gerente.contratos:
                lista.append(self.__controlador_contrato.tela_contrato.formata_contrato(contrato))
            self.__controlador_contrato.tela_contrato.listagem(lista)
        else:
            self.__tela_gerente.mostra_mensagem('Lista vazia.')

    def acessar_contrato(self):
        self.__controlador_contrato.inicializa_sistema(self, self.__gerente)

    def retornar(self):
        self.__controlador_filial.inicializa_sistema()

    @property
    def gerente(self):
        return self.__gerente

    @gerente.setter
    def gerente(self, gerente):
        self.__gerente = gerente
