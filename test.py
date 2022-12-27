import PySimpleGUI as sg

sg.theme('Dark Grey 13')

layout = [[sg.Text('Filename')],
          [sg.Input(), sg.FileBrowse()],
          [sg.OK(), sg.Cancel()]]

window = sg.Window('Get filename example', layout)

event, values = window.read()
text = sg.popup_get_text('Title', 'Please input something')
sg.popup('Results', 'The value returned from PopupGetText', text)
for i in range(1,1000):
    sg.one_line_progress_meter('My Meter', i+1, 1000, 'key','Optional message')
sg.Print("end")
window.close()