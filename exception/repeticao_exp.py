class Repeticao(Exception):
    def __init__(self, obj_repetido, valor_repetido):
        super().__init__()
        self.__obj_repetido = obj_repetido
        self.__valor_repetido = valor_repetido
    def msg(self):
        return f"Repetição não permitida em '{self.__obj_repetido}': {self.__valor_repetido}. " \
               f"Cadastre sem repetições."