from telas.abstract_tela import AbstractTela
import PySimpleGUI as sg


class TelaContrato(AbstractTela):

    def __init__(self):
        super().__init__()
        self.__window = None
        self.init_components()

    def mostra_opcoes(self):
        self.init_components()
        event, values = self.__window.Read()
        self.__window.Close()
        if event in (None, 'Cancelar'):
            exit(0)
        return int(event)
    
    def init_components(self):
        layout = [
            [sg.Text('TELA DE MODIFICAÇÃO: CONTRATO')],
            [sg.Text('O que deseja fazer?')],
            [sg.Button('Mostrar contrato', key=1, size=(30, 1))],
            [sg.Button('Excluir contrato (desativar funcionário)', key=2, size=(30, 1))],
            [sg.Button('Modificar informações', key=3, size=(30, 1))],
            [sg.Button('Retornar', key=0, size=(30, 1))]
        ]
        self.__window = sg.Window('Controle do Contrato', layout, element_justification='c')

    def menu_modificacao(self):
        layout = [
            [sg.Text('TELA DE MODIFICAÇÃO: CONTRATO')],
            [sg.Text('O que deseja modificar?')],
            [sg.Button('Data de emissão', key=1, size=(30, 1))],
            [sg.Button('Data de finalização', key=2, size=(30, 1))],
            [sg.Button('Filial', key=3, size=(30, 1))],
            [sg.Button('Cargo', key=4, size=(30, 1))],
            [sg.Button('Retornar', key=0, size=(30, 1))]
        ]
        self.__window = sg.Window('Controle do Contrato', layout, element_justification='c')

        event, values = self.__window.Read()
        self.__window.Close()
        return int(event)

    def formata_contrato(self, contrato):
        # Mantive a procura pelo empregador empresa, mas mudei a forma de listagem para generalizar
        if contrato.empregador == "Empresa":
            empregador = "Empresa"
        else:
            empregador = contrato.empregador.nome
        if contrato.data_final is None:
            data_final = 'Indisponível.'
        else:
            data_final = contrato.data_final
        return f'''
 ===== CONTRATO =====
Funcionario: {contrato.empregado.nome}
CPF: {contrato.empregado.cpf}
Empregador: {empregador}
Cargo: {contrato.cargo.titulo}
Filial: {contrato.filial.cep}
Data de emissão: {contrato.data_inicio}
Data de termino: {data_final}
        '''

    def listagem(self, lista):

        tab_group = [[]]
        contador = 1
        for _ in lista:
            tab_group[0].append(sg.Tab(f'Pag.{contador}', [[sg.Text(_)]]))
            contador += 1
        layout = [[sg.Text('Listagem de contratos')],
                  [sg.Text('Faça a navegação por páginas.')],
                  [sg.TabGroup(tab_group)],
                  [sg.Button('Retornar')]]

        self.__window = sg.Window('Controle do Contrato', layout, element_justification='c')

        while True:
            event, values = self.__window.read()
            if event in (sg.WIN_CLOSED, 'Retornar'):
                break
        self.__window.close()
        return

    def pega_data(self, msg):
        layout = [
        [sg.Text(str(msg), size=(16, 1)),
            sg.Input(key='data', size=(29,1)),
            sg.CalendarButton('Abrir calendário', close_when_date_chosen=True, target='data', no_titlebar=False, title='Escolha a data')],
        [sg.Text(size=(23, 1), key='-OUTPUT-')],
        [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Controle do Contrato', layout, element_justification='c')

        while True:
            event, values = self.__window.read()

            if event in [sg.WIN_CLOSED, 'Cancelar']:
                self.__window.Close()
                return None
            if self.le_data(values['data']):
                data = self.formata_data(values['data'])
                self.__window.Close()
                return data
            else:
                self.__window['-OUTPUT-'].update('Digite uma data válida.')
