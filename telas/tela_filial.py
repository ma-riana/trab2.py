from telas.abstract_tela import AbstractTela
import PySimpleGUI as sg


class TelaFilial(AbstractTela):

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
            [sg.Text('TELA DE MODIFICAÇÃO: FILIAL')],
            [sg.Text('O que deseja fazer?')],
            [sg.Button('Acessar opções de funcionários comuns', key=1, size=(30, 1))],
            [sg.Button('Acessar opções de gerencia', key=2, size=(30, 1))],
            [sg.Button('Modificar dados da filial', key=3, size=(30, 1))],
            [sg.Button('Acessar contratos da filial', key=4, size=(30, 1))],
            [sg.Button('Acessar funcionários ativos', key=5, size=(30, 1))],
            [sg.Button('Retornar', key=0, size=(30, 1))]
        ]
        self.__window = sg.Window('Controle da Filial', layout, element_justification='c')

    def menu_modificacao(self):
        sg.ChangeLookAndFeel('Dark Gray 13')
        layout = [
            [sg.Text('O que deseja modificar?')],
            [sg.Text('(Para demais modificações, consulte as outras opções do menu.)')],
            [sg.Button('CEP', key=1, size=(30, 1))],
            [sg.Button('Cidade', key=2, size=(30, 1))],
            [sg.Button('Retornar', key=0, size=(30, 1))]
        ]
        self.__window = sg.Window('Controle da Filial', layout, element_justification='c')
        event, values = self.__window.Read()
        self.__window.close()
        return int(event)

    def mod_cep(self):
        layout = [
            [sg.Text('Modificação de Filial')],
            [sg.Text('Digite no campo abaixo o novo CEP da filial')],
            [sg.Text(size=(23, 1), key='-OUTPUT-')],
            [sg.Text('CEP:', size=(15, 1)), sg.InputText('', key='cep')],
            [sg.Button('Confirmar')]
        ]
        self.__window = sg.Window('Controle da Filial', layout, element_justification='c')
        while True:
            event, values = self.__window.Read()
            if self.le_cep(values['cep']):
                cep = self.formata_cep(values['cep'])
                return cep
            else:
                self.__window['-OUTPUT-'].update('Digite um CEP válido.')

    def mod_cidade(self):
        layout = [
            [sg.Text('Modificação de Filial')],
            [sg.Text('Digite no campo abaixo a nova cidade da filial')],
            [sg.Text('Cidade:', size=(15, 1)), sg.InputText('', key='cidade')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]
        self.__window = sg.Window('Controle da Filial', layout, element_justification='c')
        event, values = self.__window.Read()
        self.__window.Close()
        return values['cidade']

    def formata_listagem(self, nome, cpf, data_nasc, status):
        if status == True:
            status = 'Ativo'
        else:
            status = 'Não ativo'
        return f'Nome: {nome}\nCPF: {cpf}\nData nascimento: {data_nasc}\nStatus: {status}\n'

    def close(self):
        self.__window.Close()

    def open(self):
        button, values = self.__window.Read()
        return button, values
