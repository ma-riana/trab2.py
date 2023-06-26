from dao import FunComumDAO
from dao import ContratoDAO

#cargo = Cargo(4, 'titulo', 1200)
#data = date(2000, 11, 11)
#gerente = Gerente('paula', '123.456.789-10', data, True)
#funcomum = FunComum('andre', '444.444.444-44', data, True)
#filial = Filial('00000-000', 'cidade', gerente)
#contrato = Contrato(data, cargo, funcomum, filial, gerente)
#gerente.nome = 'mudou de nome'
#gerente.contratos.append(contrato)
#print(gerente.contratos[0].empregador.nome)
#print(filial.funcionarios[0].nome)

dao = FunComumDAO()
#print(len(dao.get_all()))
#lista = dao.get('611.111.111-11')
#print(lista.cpf)
#print(len(dao.get_all()))

dao_contratos = ContratoDAO()
todos = dao_contratos.get_all()
lista = []
for i in todos:
    lista.append(i)
for j in range(len(lista)):
    dao_contratos.remove(lista[j].empregado.cpf)
print(len(dao_contratos.get_all()))

dao_funcomum = FunComumDAO()
todos = dao_funcomum.get_all()
lista = []
for i in todos:
    lista.append(i)
for j in range(len(lista)):
    dao_funcomum.remove(lista[j].cpf)
print(len(dao_funcomum.get_all()))

