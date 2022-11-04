from browser import document, bind, window
from browser.html import *
from shortcut_function import fire_mouse_event


def draw_sub_window(shadow_id=''):
    shadow = DIV(id=f'shadow_{shadow_id}', Class='shadow')
    sub_window = DIV(id=f'sub_window_container_{shadow_id}', Class='sub_window_container')
    sub_window <= DIV('&#215', id=f'close_sub_window_{shadow_id}', Class='close')

    shadow <= sub_window
    document <= shadow

    # Close the sub window event
    @bind(f'#close_sub_window_{shadow_id}', 'click')
    def close_sub_window(ev):
        close_shadow_id = '_'.join(ev.target.id.split('_')[3:])
        document[f'shadow_{close_shadow_id}'].parent.removeChild(document[f'shadow_{close_shadow_id}'])

    return sub_window


def fire_close_sub_window(shadow_id):
    fire_mouse_event(document[f'close_sub_window_{shadow_id}'])
