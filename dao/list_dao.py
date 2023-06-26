import pickle
from abc import ABC, abstractmethod


class ListDAO(ABC):
    @abstractmethod
    def __init__(self, datasource=''):
        self.__datasource = datasource
        self.__cache = [] #é aqui que vai ficar a lista que estava no controlador. Nesse exemplo estamos usando um dicionario
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    @property
    def cache(self):
        return self.__cache

    def __dump(self):
        pickle.dump(self.__cache, open(self.__datasource, 'wb'))

    def __load(self):
        self.__cache = pickle.load(open(self.__datasource,'rb'))

    #esse método precisa chamar o self.__dump()
    def add(self, indice, obj):
        self.__cache.insert(indice, obj)
        self.__dump()  #atualiza o arquivo depois de add novo amigo

    #cuidado: esse update só funciona se o objeto com essa chave já existe
    def update(self, indice, obj):
        self.__cache[indice] = obj #atualiza a entrada
        self.__dump()  #atualiza o arquivo

    def get(self, cpf):
        try:
            for _ in self.__cache:
                if _.empregado.cpf == cpf:
                    print("O contrato está sendo devolvido do dao", _)
                    return _
            raise KeyError
        except KeyError:
            pass #implementar aqui o tratamento da exceção

    # esse método precisa chamar o self.__dump()
    def remove(self, cpf):
        try:
            for _ in self.__cache:
                if _.empregado.cpf == cpf:
                    self.__cache.remove(_)
                    self.__dump() #atualiza o arquivo depois de remover um objeto
                    return
            raise KeyError
        except KeyError:
            pass #implementar aqui o tratamento da exceção

    def get_all(self):
        return self.__cache