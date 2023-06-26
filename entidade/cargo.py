class Cargo:
    def __init__(self, id, titulo, salario):
        self.__id = id
        self.__titulo = titulo
        self.__salario = salario

    @property
    def id(self):
        return self.__id

    @property
    def titulo(self):
        return self.__titulo

    @property
    def salario(self):
        return self.__salario

    @id.setter
    def id(self, id: int):
        self.__id = id

    @titulo.setter
    def titulo(self, titulo: str):
        if isinstance(titulo, str):
            self.__titulo = titulo

    @salario.setter
    def salario(self, salario: float):
        if isinstance(salario, float):
            self.__salario = salario
