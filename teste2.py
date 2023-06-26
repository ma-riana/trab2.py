import PySimpleGUI as sg
from datetime import date

column1 = [
    [sg.Text('Column 1', text_color='black',justification='center', size=(10, 1))],
    [sg.Spin(values=(list(range(1,32))), initial_value=1, key='dia')],
    [sg.Spin(values=(list(range(1,13))), initial_value=1, key='mes', expand_x=True)],
    [sg.Spin(values=(list(range(1960,2024))), initial_value=2020, key='ano')]
 ]
#print(dia)



layout = [
    #[sg.InputOptionMenu(('Menu Option 1', 'Menu Option 2', 'Menu Option 3'))],
    #[sg.InputCombo(('Combobox 1', 'Combobox 2'), size=(20, 1))],
    #[sg.Column(column1)],
    [sg.CalendarButton('Abrir calendário', close_when_date_chosen=True, target='data', no_titlebar=False),
     sg.Input(key='data', size=(20,1))],
    [sg.Submit(tooltip='Click to submit this window'), sg.Cancel()]
]

window = sg.Window('Everything bagel', default_element_size=(40, 1), grab_anywhere=False).Layout(layout)
button, values = window.Read()
f1 = int(values['data'][8:10])
f2 = int(values['data'][5:7])
f3 = int(values['data'][:4])
print(f3, f2, f1)
sg.Popup('Title', 'The results of the window.', 'The button clicked was "{}"'.format(button), 'The values are', values)

