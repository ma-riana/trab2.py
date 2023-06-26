from abc import ABC, abstractmethod
from datetime import date
import PySimpleGUI as sg


class AbstractTela(ABC):

    @abstractmethod
    def __init__(self):
        self.__window = None
        self.colorir()

    def colorir(self):
        sg.SetOptions(background_color='#FA91BA', 
                      text_color='#000000',
                      text_element_background_color='#FA91BA', 
                      input_elements_background_color='#FDABE1', 
                      scrollbar_color='#FA91BA',
                      element_background_color='#FF4A91', 
                      button_color=('white','#FF4A91'),
                      font=("Yu Gothic UI Semibold", 11),
                      input_text_color='#000000',
                      margins=(10, 15),
                      element_padding=(3, 3)) 
        
    def mostra_opcoes(self):
        pass

    def init_components(self):
        pass

    def mostra_mensagem(self, msg):
        sg.popup(msg, title='Mensagem')

    def pega_input(self, msg: str, titulo):
        inp = sg.popup_get_text(msg, title=titulo)
        return inp
    
    def pega_nome(self, msg: str, titulo):
        while True:
            inp = sg.popup_get_text(msg, title=titulo)
            if inp is None:
                return
            if inp.strip() != '':
                break
            self.mostra_mensagem('Digite um nome válido\n')
        return inp.title()

    def le_cpf(self, cpf):
        while True:
            try:
                cpf_int = int(cpf)
                if isinstance(cpf_int, int):
                    if len(cpf) == 11:
                        return True
                raise ValueError
            except ValueError:
                return False

    def formata_cpf(self, cpf):
        f1 = cpf[:3]
        f2 = cpf[3:6]
        f3 = cpf[6:9]
        f4 = cpf[9:]
        return f'{f1}.{f2}.{f3}-{f4}'

    def le_cep(self, cep):
        while True:
            try:
                int_cep = int(cep)
                if isinstance(int_cep, int):
                    if len(cep) == 8:
                        return True
                raise ValueError
            except ValueError:
                return False

    def formata_cep(self, cep):
        f1 = cep[:5]
        f2 = cep[5:]
        return f'{f1}-{f2}'

    def le_data(self, data):
        while True:
            try:
                data = self.formata_data(data)
                if isinstance(data, date):
                    return True
                raise ValueError
            except ValueError:
                return False

    def formata_data(self, data):
        f1 = int(data[8:10])
        f2 = int(data[5:7])
        f3 = int(data[:4])
        return date(f3, f2, f1)

    def le_salario(self, salario):
        try:
            salario_float = float(salario)
            if salario_float > 500:
                return True
            raise ValueError
        except ValueError:
            return False

    def listagem(self, titulo, lista_listagem):
        layout = [[sg.Text(titulo)]]
        lista = ''
        for _ in lista_listagem:
            lista += _ + '\n'
        layout.append([sg.Multiline(default_text=lista, size=(30, 5))])
        self.__window = sg.Window('Listagem', layout, element_justification='c')
        event = self.__window.Read()
        if event in [sg.WIN_CLOSED]:
            self.init_components()
