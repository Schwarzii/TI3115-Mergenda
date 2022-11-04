from browser import document, bind
from browser.html import *
from sub_window_template import draw_sub_window


def add_event_container(parent):
    event_container = DIV(Class='event_container')  # Component showing the recent scheduled event
    event_container <= DIV('Recent events:')
    event_list = UL(id='event_list', Class='list_no_bullet')
    event_container <= event_list
    parent <= event_container


def add_new_event(event_info):
    """
    :param event_info:
    input example: schedule = {'time': ['2022-11-05', '10:00', '16:00'],
                               'event_name': 'project meeting',
                               'event_code': '00022',
                               'group_name': 'mergenda',
                               'scheduler': 'sheep',
                               'availability': '...'}
    """
    new_event = LI()
    event_intro = DIV(Class='in_line')
    event_intro <= DIV(f"&#127915 {event_info['event_name']}", Class='event_title')
    event_intro <= DIV(SPAN('&#128197', Class='event_cell') +
                       SPAN(event_info['time'][0]) +
                       SPAN('&#128337', Class='event_cell') +
                       SPAN(f"{event_info['time'][1]} - {event_info['time'][2]}"),
                       Class='event_row')
    event_intro <= DIV(SPAN('&#128101', Class='event_cell') +
                       SPAN(f"{event_info['group_name']}") +
                       SPAN(f"Scheduled by: {event_info['scheduler']}", Class='italic grey_font event_cell'),
                       Class='event_row')
    new_event <= event_intro
    button = DIV('View availability', id=f"availability_{event_info['event_code']}",
                 name='check_availability', data=event_info['availability'],
                 Class='td button_blue in_line align_top')
    new_event <= button
    document['event_list'] <= new_event

    @bind(f"#availability_{event_info['event_code']}", 'click')
    def show_availability(ev):
        sub_window = draw_sub_window()
        event_availability_container = DIV(id='availability_table')
        event_availability = TABLE()
        print(ev.target.attrs['data'])
        for line in ev.target.attrs['data'].split('\n'):
            if line[0] == 'A':
                sub_window <= DIV(line, Class='availability_note title')
            else:
                event_availability_row = TR()
                for cell in line.split('  '):
                    if cell == '':
                        continue
                    event_availability_row <= TD(cell)
                event_availability <= event_availability_row
        event_availability_container <= event_availability
        sub_window <= event_availability_container
        sub_window <= DIV("Each 'x' mark means being available in this time slot.",
                          Class='availability_note grey_font')
