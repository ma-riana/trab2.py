class FilialErrada(Exception):
    def __init__(self, cpf):
        super().__init__()
        self.__cpf = cpf

    def msg(self):
        print(f"Funcionário de CPF '{self.__cpf}' não trabalha na filial sendo manipulada.\n"
              + f"Acesse a listagem geral.")