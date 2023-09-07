import PySimpleGUI as sg
import re
import json
from webbrowser import open as wbopen
import subprocess, os, platform
import sys

class Option:
    def __init__(self,Jsonfilepath = "options.json") -> None:
        self.Jsonfilepath = Jsonfilepath
        
    def prepare_choices(self):
        with open(self.Jsonfilepath,"r") as reader:
            self.jsondict = json.load(reader)
        return list(self.jsondict)
    
    def _open_file(self,path):
        if platform.system() == 'Windows':    # Windows
            os.startfile(path)
        else:                                   # linux variants
            subprocess.call(('xdg-open', path))

    def execute(self ,keyword):
        value = self.jsondict[keyword]['value']
        if self.jsondict[keyword]['type'] == 'link':
            wbopen(value)
        elif self.jsondict[keyword]['type'] == 'file':
            self._open_file(value)
        else:
            pass
def move_center(window):
    screen_width, screen_height = window.get_screen_dimensions()
    win_width, win_height = window.size
    x, y = (screen_width - win_width)//2, (screen_height - win_height)//2
    window.move(x, y)

def filter_list_elements(input, lista):
    pattern = re.compile('.*' + input + '.*',flags=re.IGNORECASE)
    return [w for w in lista if re.match(pattern, w)]

def main():
    # The list of choices that are going to be searched
    # In this example, the PySimpleGUI Element names are used
    option = Option()
    choices = option.prepare_choices()
    input_width = 75
    num_items_to_show = 4

    layout = [
        [sg.Input(size=(input_width, 1), enable_events=True, key='-IN-')],
        [sg.pin(sg.Col([[sg.Listbox(values=[], size=(input_width, num_items_to_show), enable_events=True, key='-BOX-',
                                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, no_scrollbar=True)]],
                       key='-BOX-CONTAINER-', pad=(0, 0), visible=False))]
            ]

    window = sg.Window('kamui - a  space time ninjutsu              *AYRA Technologies*', layout, return_keyboard_events=True, finalize=True, font= ('Console', 16),icon="kamui.ico")
    window.bind("<Return>", "_Enter")
    list_element:sg.Listbox = window.Element('-BOX-')           # store listbox element for easier access and to get to docstrings
    prediction_list, input_text, sel_item = [], "", 0
    window.move_to_center()
    while True:  # Event Loop
        event, values = window.read()
        # print(event, values)
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "_Enter":
            option.execute(prediction_list[sel_item])
            break
        # pressing down arrow will trigger event -IN- then aftewards event Down:40
        elif event.startswith('Escape'):
            break
        elif event.startswith('Down') and len(prediction_list):
            sel_item = (sel_item + 1) % len(prediction_list)
            list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)
        elif event.startswith('Up') and len(prediction_list):
            sel_item = (sel_item + (len(prediction_list) - 1)) % len(prediction_list)
            list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)
        elif event == '\r':
            if len(values['-BOX-']) > 0:
                window['-IN-'].update(value=values['-BOX-'])
                window['-BOX-CONTAINER-'].update(visible=False)
        elif event == '-IN-':
            text = values['-IN-']
            if text == input_text:
                continue
            else:
                input_text = text
            prediction_list = []
            if text:
                prediction_list = filter_list_elements(input_text,choices)
            list_element.update(values=prediction_list)
            sel_item = 0
            list_element.update(set_to_index=sel_item)

            if len(prediction_list) > 0:
                window['-BOX-CONTAINER-'].update(visible=True)
            else:
                window['-BOX-CONTAINER-'].update(visible=False)
        elif event == '-BOX-':
            window['-IN-'].update(value=values['-BOX-'])
            window['-BOX-CONTAINER-'].update(visible=False)

    window.close()


if __name__ == '__main__':
    path = re.sub("kamui.py","",sys.argv[0])
    os.chdir(path)
    main()