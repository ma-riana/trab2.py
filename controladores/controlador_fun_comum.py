from controladores.controlador_funcionario import ControladorFuncionario


class ControladorFunComum(ControladorFuncionario):

    def __init__(self):
        super().__init__()
        self.__fun_comum_dao = super().fun_comum_dao

    @property
    def fun_comum_dao(self):
        return self.__fun_comum_dao
