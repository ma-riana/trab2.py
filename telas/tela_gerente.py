from telas.tela_funcionarios import TelaFuncionario
import PySimpleGUI as sg


class TelaGerente(TelaFuncionario):

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
            [sg.Text('TELA DE MODIFICAÇÃO: GERENTE')],
            [sg.Text('O que deseja fazer?')],
            [sg.Button('Modificar informações do gerente atual', key=1, size=[30, 1])],
            [sg.Button('Demitir', key=2, size=[30, 1])],
            [sg.Button('Listagem de contratos realizados', key=3, size=[30, 1])],
            [sg.Button('Acessar contrato', key=4, size=[30, 1])],
            [sg.Button('Retornar', key=0, size=[30, 1])]
        ]
        self.__window = sg.Window('Controle do Gerente', layout, element_justification='c')
