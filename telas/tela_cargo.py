from telas.abstract_tela import AbstractTela
from exception.nao_existe_exp import NaoExistencia
import PySimpleGUI as sg


class TelaCargo(AbstractTela):

    def __init__(self):
        super().__init__()
        self.__id_gerados = [0, 1, 2]
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
            [sg.Text('TELA DE MODIFICAÇÃO: CARGOS')],
            [sg.Text('O que deseja fazer?')],
            [sg.Button('Adicionar cargo', key=1, size=(30, 1))],
            [sg.Button('Alterar cargo', key=2, size=(30, 1))],
            [sg.Button('Excluir cargo', key=3, size=(30, 1))],
            [sg.Button('Listar todos os cargos', key=4, size=(30, 1))],
            [sg.Button('Retornar', key=0, size=(30, 1))]
        ]
        self.__window = sg.Window('Controle dos Cargos', layout, element_justification='c')

    def pega_dados_cargo(self, id=None):
        layout = [
            [sg.Text('Inserindo os dados do cargo')],
            [sg.Text(size=(23, 1), key='-OUTPUT-')],
            [sg.Text('Titulo:', size=(15, 1)), sg.InputText('', key='titulo')],
            [sg.Text('Salário:', size=(15, 1)), sg.InputText('', key='salario')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Controle de cargos', layout, element_justification='c')

        event, values = self.__window.read()
        if event == 'Confirmar':
            if self.le_salario(values['salario']):
                if id is None:
                    id = self.gera_id()
                return {"id": id, "titulo": values['titulo'], "salario": values['salario']}
            else:
                self.__window['-OUTPUT-'].update('Digite um CEP válido.')
        if event in [sg.WIN_CLOSED, 'Cancelar']:
            self.__window.close()
            return None

    def formata_listagem(self, id, titulo, salario):
        return f'ID: {id}\nTítulo: {titulo}\nSalário: {salario}\n'

    def pega_cargo(self, lista):
        # Definição do layout para a lista de cargos
        layout = [[sg.Text('Selecionador de cargos. Faça a busca por id.')]]
        lista_cargos = ''
        for cargo in lista:
            # Tirando a opção de cadastro de gerente
            if cargo.id != 0:
                lista_cargos += f'ID: {cargo.id} Título: {cargo.titulo}\n'

        # Atribuição ao layout
        layout.append([sg.Multiline(default_text=lista_cargos, size=(35, 3))])
        layout.append([sg.Text('ID para a busca:', size=(15, 1)), sg.InputText('', key='id')])
        layout.append([sg.Button('Confirmar'), sg.Button('Cancelar')])
        layout.append( [sg.Text(size=(23, 1), key='-OUTPUT-')])
        self.__window = sg.Window('Controle de cargos', layout, element_justification='c')

        # Checagem de opções
        while True:
            event, values = self.__window.read()
            if event == 'Confirmar':
                try:
                    if values['id'] == '':
                        raise ValueError
                    else:
                        id = int(values['id'])
                        if id not in self.__id_gerados:
                            raise NaoExistencia()
                        self.__window.Close()
                        return id
                except ValueError:
                    self.__window['-OUTPUT-'].update('Digite um ID.')
                except NaoExistencia:
                    self.__window['-OUTPUT-'].update('Digite um ID válido.')
            if event in [sg.WIN_CLOSED, 'Cancelar']:
                self.__window.Close()
                return None

    def gera_id(self):
        novo_id = (self.__id_gerados[-1] + 1)
        self.__id_gerados.append(novo_id)
        return novo_id

    def exclui_id(self, id: int):
        self.__id_gerados.remove(id)
