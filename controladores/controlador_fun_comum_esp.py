from entidade.fun_comum import FunComum
from telas.tela_fun_comum import TelaFuncomum
from exception.nao_existe_exp import NaoExistencia
from exception.filial_errada_exp import FilialErrada
from controladores.controlador_funcionario import ControladorFuncionario


class ControladorFunComumEsp(ControladorFuncionario):

    def __init__(self, controlador_filial, funcionarios):
        super().__init__()
        self.__controlador_filial = controlador_filial
        self.__controlador_sistema = self.__controlador_filial.controlador_sistema
        self.__controlador_contrato = self.__controlador_sistema.controlador_contrato
        self.__controlador_cargo = self.__controlador_sistema.controlador_cargo
        self.__tela_fun_comum = TelaFuncomum()
        self.__funcionarios = funcionarios

    def inicializa_sistema(self):
        lista_opcoes = {1: self.modificar_dados, 2: self.add_fun_comum,
                        3: self.acessar_contrato, 4: self.listar_todos,
                        5: self.demitir, 0: self.retornar}

        while True:
            opcao_escolhida = self.__tela_fun_comum.mostra_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()

    def modificar_dados(self):
        # Modificação dos funcionários da filial atual
        funcionario = self.busca_fun_por_cpf("Digite o CPF do funcionário para modificação: ")
        if funcionario is None:
            return
        opcao = self.__tela_fun_comum.menu_modificacao()
        # nao quer realizar modificacao
        if opcao == 0:
            return
        # alguma modificacao sera feita
        else:
            contrato = self.__controlador_contrato.contrato_dao.get(funcionario.cpf)
            filial = self.__controlador_filial.filial
            # esta modificando a chave do dao
            if opcao == 2:
                # Checagem de CPF para a modificação
                while True:
                    novo_cpf = self.__tela_fun_comum.pega_cpf('Digite o novo CPF: ')
                    if self.repeticao_cpf(novo_cpf):
                        break
                    else:
                        self.__tela_fun_comum.mostra_mensagem('CPF já cadastrado.')
                # Atualização do DAO. Cópia necessária pois é a modificação da chave
                super().fun_comum_dao.remove(funcionario.cpf)
                self.__controlador_contrato.contrato_dao.remove(funcionario.cpf)
                #filial.setter_funcionarios(novo_cpf, funcionario)
                funcionario.cpf = novo_cpf
                contrato.empregado = funcionario
                super().fun_comum_dao.add(funcionario)
                self.__controlador_contrato.contrato_dao.add(contrato)
            # modificacao de outros atributos que nao sao chave
            else:
                if opcao == 1:
                    novo_nome = self.__tela_fun_comum.pega_nome("Digite o novo nome:", 'Modificação de dados.')
                    if novo_nome is None:
                        return
                    funcionario.nome = novo_nome
                    super().fun_comum_dao.update(funcionario)
                elif opcao == 3:
                    nova_data_nasc = self.__tela_fun_comum.pega_data('Data de nascimento:')
                    if nova_data_nasc is None:
                        return
                    funcionario.data_nasc = nova_data_nasc
                # atualizacoes para qualquer uma das modificacoes
                super().fun_comum_dao.update(funcionario)
                contrato.empregado = funcionario
                self.__controlador_contrato.contrato_dao.update(contrato)       
                filial.setter_funcionarios(funcionario.cpf, funcionario)
            self.__controlador_sistema.filial_dao.update(filial)         

    def add_fun_comum(self):
        # Realizando a checagem de repetição de CPF
        while True:
            novo_fun_comum = self.__tela_fun_comum.pega_dados_cadastro()
            if self.repeticao_cpf(novo_fun_comum['CPF']):
                break
            self.__tela_fun_comum.mostra_mensagem('CPF já cadastrado.')

        # Criação do funcionário
        novo_funcionario = FunComum(novo_fun_comum['nome'], novo_fun_comum['CPF'],
                                    novo_fun_comum['data_nasc'])

        # Definição das informações para o contrato
        data_inicio = novo_fun_comum['data_inicio']
        empregador = self.__controlador_filial.filial.gerente
        filial = self.__controlador_filial.filial
        cargo = self.__controlador_cargo.seleciona_cargo()

        dados_contrato = {'data_inicio': data_inicio, 'cargo': cargo, 'empregado': novo_funcionario,
                          'filial': filial, 'empregador': empregador}
        self.__controlador_contrato.incluir_contrato(dados_contrato)

        # Update do DAO
        super().fun_comum_dao.add(novo_funcionario)

    def demitir(self):
        # Demissão realizando a busca por CPF
        fun_comum = self.busca_fun_por_cpf("Digite o CPF do funcionário para a demissão: ")
        if fun_comum is None:
            return
        # Checagem se o funcionário já está demitido
        if fun_comum.atividade:
            # Demissão no contrato e update do DAO
            self.__controlador_contrato.demitir(fun_comum)
            fun_comum.atividade = False
            super().fun_comum_dao.update(fun_comum)
        else:
            self.__tela_fun_comum.mostra_mensagem('Não é possível demitir um funcionário já demitido.')

    def acessar_contrato(self):
        # Acesso ao menu do contrato de um funcionário específico
        fun_comum = self.busca_fun_por_cpf("Digite o CPF do funcionário para acessar o contrato: ")
        if fun_comum is None:
            return
        self.__controlador_contrato.inicializa_sistema(self, fun_comum)

    def listar_todos(self):
        # Listagem completa de funcionários
        lista = []
        funcionarios = self.__controlador_filial.filial.funcionarios
        if len(funcionarios) > 0:
            for fun in funcionarios:
                lista.append(self.__tela_fun_comum.formata_listagem(fun.nome, fun.cpf,
                                                                    fun.data_nasc, fun.atividade))
            self.__tela_fun_comum.listagem('Listagem de funcionários', lista)
        else:
            self.__tela_fun_comum.mostra_mensagem('Lista vazia.')

    def busca_fun_por_cpf(self, msg):
        # Método de busca de funcionário na filial atual
        while True:
            cpf_buscado = self.__tela_fun_comum.pega_cpf(msg)
            if cpf_buscado is None:
                return None
            # Pega uma lista geral para informar se o fun é de outra filial
            lista_fun_geral = super().fun_comum_dao.get_all()
            try:
                for funcionario in self.__funcionarios:
                    if funcionario.cpf == cpf_buscado:
                        return funcionario
                for funcionario in lista_fun_geral:
                    if funcionario.cpf == cpf_buscado:
                        raise FilialErrada(cpf_buscado)
                raise NaoExistencia()
            except NaoExistencia:
                self.__tela_fun_comum.mostra_mensagem('Funcionario não encontrado. Tente novamente.')
            except FilialErrada:
                self.__tela_fun_comum.mostra_mensagem('Este funcionário não atua na filial selecionada, tente pesquisar em outra.')

    def retornar(self):
        self.__controlador_filial.inicializa_sistema()
