import PySimpleGUI as psg

def listagem(lista):

    tab_group = [[]]
    contador = 1
    for _ in lista:
        tab_group[0].append(psg.Tab(f'Pag.{contador}', [[psg.Text(_)]]))
        contador += 1
    layout = [[psg.Text('Listagem de contratos\n Faça a navegação por páginas.')],
              [psg.TabGroup(tab_group)],
              [psg.OK(), psg.Cancel()]]

    window = psg.Window('Formatação listagem', layout)

    while True:
        event, values = window.read()
        print(event, values)
        if event in (psg.WIN_CLOSED, 'Exit'):
            break
    window.close()


listagem(['AAAAA', 'BBBBB'])