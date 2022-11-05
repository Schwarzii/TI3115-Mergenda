import datetime
import json

from browser import alert
from browser.session_storage import storage

import group_management as gm
from ajax_call import post_data, get_data
from sub_window_template import *
from shortcut_function import round_nearest_time
from scheduled_events import *


def redirect_to_login():
    window.location.href = "../Login/login.html"  # Redirect to the main UI


# Check the login account and load data
if len(storage) != 0:
    user = storage['username']
    password = storage['password']
    server_host = storage['url']
else:  # Must log in account first
    redirect_to_login()
    user = 'sheep'
    password = '2222'
    server_host = 'Schwarzi.pythonanywhere.com'
    # server_host = '127.0.0.1:5000'

# Components showing the user's group related info
left_grid = DIV(Class='container_grid')
left_grid <= DIV(f'Hello, {user}!', Class='account_user')

account_container = DIV(Class='account_container')
account_container <= DIV(SPAN('Mergenda account', Class='italic grey_font') +
                         SPAN('&#128393', id='mergenda', name='edit_account_info', edit='off', Class='mini_button'))
account_info = TABLE()
account_info <= TR(TD('Name') + TD(INPUT(value=f'{user}', id='mergenda_acc_1', readonly=True, pre='', disabled=True)))
account_info <= TR(TD('Email') + TD(INPUT(id='mergenda_acc_2', pre='', disabled=True)))
account_info <= TR(TD('Change password', id='change_pass', colspan=2, Class='button_blue'))
account_container <= account_info

account_container <= DIV(SPAN('Google account', Class='italic grey_font') +
                         SPAN('&#128393', id='google', name='edit_account_info', edit='off', Class='mini_button'),
                         style={'padding-top': '15px'})
google_info = TABLE()
google_info <= TR(TD('Email') + TD(INPUT(id='google_acc_1', pre='', disabled=True, ) +
                                   SPAN('@gmail.com')))
google_info <= TR(TD('Password ') + TD(INPUT(id='google_acc_2', type='password', pre='', disabled=True) +
                                       SPAN('&#128065', id='show_google_pass', name='show_pass', Class='mini_col')))
account_container <= google_info
left_grid <= account_container

document <= left_grid

# Components updating user's preferences and managing events
middle_grid = DIV(Class='container_grid middle_background')
preference_container = DIV(Class='pref_container')
preference = DIV()
pref_simple_input = TABLE(name='preference', Class='in_line align_top')
pref_simple_input <= TR(TD('Date picking interval', Class='pref_col') +
                        TD(INPUT(value=f'{datetime.date.today()}', min=f'{datetime.date.today()}', type='date',
                                 id='start_date', Class='date_picker') + SPAN(' - ') +
                           INPUT(value=f'{datetime.date.today() + datetime.timedelta(days=7)}',
                                 min=f'{datetime.date.today()}', type='date', id='end_date', Class='date_picker'),
                           colspan=2),
                        name='preference')
now = datetime.datetime.now().strftime("%H:%M")
next_hour = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%H:%M")
pref_simple_input <= TR(TD('Time picking interval', Class='pref_col') +
                        TD(INPUT(value=f'{round_nearest_time(now)}', type='time', Class='time_picker', step=900,
                                 id='start_time') +
                           SPAN(' - ') +
                           INPUT(value=f'{round_nearest_time(next_hour)}', type='time', Class='time_picker', step=900,
                                 id='end_time'),
                           colspan=2),
                        name='preference')
pref_simple_input <= TR(TD('Minimum event duration', Class='pref_col') +
                        TD(INPUT(value=15, min=0, max=60, step=15, type='range', id='duration_bar',
                                 Class='duration_bar')) +
                        TD(INPUT(value='00:15', step='900', name='no_clock', id='duration_display', readonly=True,
                                 type='time')),
                        name='preference')
pref_simple_input <= TR(TD('Minimum number of participants', Class='pref_col') +
                        TD(INPUT(value='1', min='0', type='number', id='min_participant')),
                        name='preference')
pref_simple_input <= TR(TD('Schedule mode', Class='pref_col') +
                        TD(SELECT(OPTION('Most people') + OPTION('Longest duration') + OPTION('Balanced'), id='mode')),
                        name='preference')
preference <= pref_simple_input

day_pick = DIV(Class='in_line align_top list_block')
day_pick <= DIV('Day picking', Class='ul_title')
pref_week_pick = UL(id='day_pick_list', Class='list_no_bullet pick_list')
# pref_week_pick = UL('Day picking', Class='list_no_bullet pick_list')
week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
for w in week:
    if w != 'Saturday' and w != 'Sunday':
        li_class = 'day_pick weekday'
    else:
        li_class = 'day_pick weekend'
    pref_week_pick <= LI(f'{w}', selected='0', Class=li_class)
day_pick <= pref_week_pick
preference <= day_pick

people_pick = DIV(Class='in_line align_top list_block')
people_pick <= DIV('Important people', Class='ul_title')
important_people = UL(id='important_people', Class='list_no_bullet pick_list')
people_pick <= important_people
people_pick <= DIV(INPUT(id='all_important', type='checkbox', Class='in_line') + SPAN('All present'),
                   Class='ul_title')
preference <= people_pick

preference_container <= preference
# preference_container <= (DIV('Save as default', id='save_pref', Class='td button_blue in_line') +
#                          DIV('Reset to default', id='reset_pref', Class='td button_blue in_line'))
middle_grid <= preference_container

schedule_container = DIV(Class='schedule_container')
group_event = DIV(Class='schedule')
group_event <= DIV('Schedule for chosen group', id='schedule', Class='td button_blue grey_background')
group_selection = UL(id='group_selection', Class='schedule_selection list_no_bullet')
group_event <= group_selection
schedule_container <= group_event

event_name = DIV(Class='in_line event_name')
event_name <= (SPAN('Event name (optional)', Class='in_line align_top') +
               INPUT(id='event_name', Class='align_top'))
schedule_container <= event_name

# schedule_container <= (DIV('Save as default', id='save_pref', Class='td button_blue in_line') +
#                        DIV('Use default', id='reset_pref', Class='td button_blue in_line'))

middle_grid <= schedule_container

# Add container for placing event elements
add_event_container(middle_grid)

document <= middle_grid

# Test event style
# schedule = {'time': ['2022-10-20', '10:00', '16:00'], 'event_name': 'project meeting', 'event_code': '00022',
#             'group_name': 'mergenda',
#             'scheduler': 'Jaap de Ruiter'}
# add_new_event(schedule)

# Add group module
group_parent = gm.add_right_grid(user)


# Callback function after fetching data
def parse_init_data(req):
    data = req.json
    print(data)
    # Load Mergenda account setting
    document['mergenda_acc_1'].value = data['name']
    document['mergenda_acc_1'].attrs['pre'] = data['name']
    document['mergenda_acc_2'].value = data['email']
    document['mergenda_acc_2'].attrs['pre'] = data['email']
    # Load linked Google account setting
    document['google_acc_1'].value = data['google']['email']
    document['google_acc_1'].attrs['pre'] = data['google']['email']
    document['google_acc_2'].value = data['google']['password']
    document['google_acc_2'].attrs['pre'] = data['google']['password']

    # Insert groups
    gm.add_groups(data['groups'].items(), group_parent, user)

    # Insert scheduled events
    for ec, ei in data['events'].items():  # event_code (ec) and event_info (ei)
        # Transform event code to be an item in event info
        ei.update({'event_code': ec})
        add_new_event(ei)


# Fetch data and assign to fields
get_data({'user': user, 'request_data': 'init'}, 'load_user_data', parse_init_data)


# Account info setting events
@bind("span[name='edit_account_info']", 'click')
def edit_account_info(ev):
    # draw_sub_window()
    account_type = ev.target.id
    if ev.target.attrs['edit'] == 'off':
        ev.target.attrs['edit'] = 'on'
        ev.target.innerHTML = '&#128190'
        document[f'{account_type}_acc_1'].disabled = False
        document[f'{account_type}_acc_2'].disabled = False
    else:
        ev.target.attrs['edit'] = 'off'
        ev.target.innerHTML = '&#128393'
        document[f'{account_type}_acc_1'].disabled = True
        document[f'{account_type}_acc_2'].disabled = True

        # Send input values to the server if changed
        if (document[f'{account_type}_acc_1'].value != document[f'{account_type}_acc_1'].attrs['pre'] or
                document[f'{account_type}_acc_2'].value != document[f'{account_type}_acc_2'].attrs['pre']):
            post_data({'change': 'account_info',
                       'user': user,
                       'account': account_type,
                       'info_1': document[f'{account_type}_acc_1'].value,
                       'info_2': document[f'{account_type}_acc_2'].value})


# Change password module
@bind('#change_pass', 'click')
def change_password(ev):
    # ev.target.style.backgroundColor = '#a9a9a9'
    ev.target.classList.add('grey_background')
    ev.target.style.cursor = 'default'
    ev.target.unbind('click', change_password)
    parent_table = ev.target.parent.parent
    parent_table <= TR(TD('New password') + TD(INPUT(name='new_pass', type='password') +
                                               SPAN('&#128065', id='show_new_pass', name='show_pass',
                                                    Class='mini_col')))
    parent_table <= TR(TD('Confirm') + TD(INPUT(name='new_pass', type='password') +
                                          SPAN('&#128065', id='show_new_pass_d', name='show_pass', Class='mini_col')))
    parent_table <= TR(TD('', id='prompt', Class='red_font', colspan=2))
    parent_table <= TR(TD('Cancel', id='cancel_update_pass', Class='button_red') +
                       TD('Update password', id='update_pass', Class='button_blue'))
    document['show_new_pass'].bind('click', show_pass)
    document['show_new_pass_d'].bind('click', show_pass)

    @bind('#cancel_update_pass', 'click')
    def cancel_update_password(event):
        account_info_table = event.target.parent.parent
        for i in range(6, 2, -1):
            account_info_table.removeChild(account_info_table.child_nodes[i])
        document['change_pass'].classList.remove('grey_background')
        document['change_pass'].style.cursor = 'pointer'
        document['change_pass'].bind('click', change_password)

    @bind('#update_pass', 'click')
    def update_pass(ev_update):
        global password

        @bind("input[name='new_pass']", 'focus')
        def cancel_prompt(event):
            document['prompt'].text = ''
            event.target.unbind('focus', cancel_prompt)

        new, check = document.select("input[name='new_pass']")
        if new.value == '' or check.value == '':  # No empty input field
            document['prompt'].text = "Input fields can't be empty"
        elif new.value != check.value:  # Inputs match
            document['prompt'].text = "Passwords don't match"
        elif new.value == password:  # Repeated password
            document['prompt'].text = "New password is the same as current one"
        else:  # Successfully change password
            password = new.value

            def finish_change_pass(req):
                alert(req.text)
                document['cancel_update_pass'].dispatchEvent(window.MouseEvent.new("click"))

            post_data({'change': 'password', 'user': user, 'new_password': new.value},
                      callback=finish_change_pass)


@bind('#show_google_pass', 'click')
def show_pass(ev):
    input_field = ev.target.parent.firstChild
    if input_field.type == 'password':
        ev.target.innerHTML = '&#9729'
        input_field.type = 'text'
        ev.target.attrs['mode'] = 'text'
    else:
        ev.target.innerHTML = '&#128065'
        input_field.type = 'password'
        ev.target.attrs['mode'] = 'pass'


# Dynamically change the min date of end
@bind('#start_date', 'change')
def end_date_check(ev):
    # Set min selectable date of the end date no earlier than the start date
    document['end_date'].min = ev.target.value
    # Update current value of end_date if earlier than the min
    if document['end_date'].value < ev.target.value:
        document['end_date'].value = ev.target.value


# User can't select the weekdays that do not lay in the date range
@bind('.date_picker', 'change')
def limit_weekday_select(ev):
    start_date_idx = datetime.datetime.strptime(document['start_date'].value, '%Y-%m-%d').weekday()
    end_date_idx = datetime.datetime.strptime(document['end_date'].value, '%Y-%m-%d').weekday()
    print(start_date_idx, end_date_idx)
    day_diff = end_date_idx - start_date_idx
    if day_diff > 0:
        weekday_select = [True if start_date_idx <= d <= end_date_idx else False for d in range(7)]
    elif day_diff < 0:
        weekday_select = [False if end_date_idx < d < start_date_idx else True for d in range(7)]
    else:
        if document['start_date'].value == document['end_date'].value:
            weekday_select = [True if d == start_date_idx else False for d in range(7)]
        else:
            weekday_select = [True for d in range(7)]
    for child, select in zip(document['day_pick_list'].child_nodes, weekday_select):
        self_class = 'day_pick'
        if not select and child.attrs['selected'] != '-1':
            if child.attrs['selected'] == '1':
                fire_mouse_event(child)
            child.classList.add('grey_font')
            child.classList.add('day_no_pick')
            child.unbind('click', select_day_pick)
            child.attrs['selected'] = '-1'
        if select and child.attrs['selected'] == '-1':
            child.classList.remove('grey_font')
            child.classList.remove('day_no_pick')
            child.bind('click', select_day_pick)
            child.attrs['selected'] = '0'


# Dynamically round the time input to the nearest 15 minute
@bind('.time_picker', 'blur')
def round_time_input(ev):
    ev.target.value = round_nearest_time(ev.target.value)


# Dynamically adjust the range of the duration as a slider
@bind('.time_picker', 'change')
def duration_bar_range(ev):
    # Split hour and minute, convert to int list
    start_time = list(map(int, document['start_time'].value.split(':')))
    end_time = list(map(int, document['end_time'].value.split(':')))
    # The case that end_time crosses the day
    if end_time[0] < start_time[0]:
        end_time[0] += 24
    # Change range
    interval = (int(end_time[0]) - int(start_time[0])) * 60 + (int(end_time[1]) - int(start_time[1]))
    interval = 15 * (interval // 15)
    document['duration_bar'].max = str(interval)
    # If the interval decreases, the display value should also change accordingly
    if document['duration_bar'].value == document['duration_bar'].max:
        document['duration_display'].value = f'{interval // 60:02}:{interval % 60:02}'


# Display the current value of the duration as a slider
@bind('#duration_bar', 'input')
def duration_bar_display(ev):
    bar_value = int(ev.target.value)
    duration_display = ev.target.parent.parent.lastChild.lastChild
    duration_display.value = f'{bar_value // 60:02}:{bar_value % 60:02}'


# Pick day(s) of the week
day_pick = []


@bind("li.day_pick", 'click')
def select_day_pick(ev):
    selected = ev.target.attrs['selected']
    if selected == '0':
        # Toggle background color change
        ev.target.classList.add('day_pick_selected')
        day_pick.append(ev.target.text)
    elif selected == '1':
        ev.target.classList.remove('day_pick_selected')
        day_pick.remove(ev.target.text)
    print(day_pick)
    # else case: selection limited
    ev.target.attrs['selected'] = '01'.replace(selected, '')


# Change schedule mode
@bind('#mode', 'change')
def select_schedule_mode(ev):
    if ev.target.value == 'Balanced':
        pref_simple_input <= TR(TD('Ideal duration', Class='pref_col') +
                                TD(INPUT(value=60, min=0, max=480, step=15, type='range', id='ideal_duration_bar',
                                         Class='duration_bar')) +
                                TD(INPUT(value='01:00', step='900', name='no_clock', id='ideal_duration_display',
                                         readonly=True, type='time')),
                                name='preference')
        document['ideal_duration_bar'].bind('input', duration_bar_display)
    elif len(pref_simple_input.child_nodes) == 6:
        pref_simple_input.removeChild(pref_simple_input.lastChild)


# Schedule an event and send settings to the server
@bind('#schedule', 'click')
def schedule_event(ev):
    if len(document['group_selection'].child_nodes) == 0:
        alert('Please select a group first! Click the grayed word "Group".')
    elif len(document['group_selection'].child_nodes) > 1:
        alert('Please select only one group. Scheduling events for multiple groups will be available closely :)')
    elif len(day_pick) == 0:
        alert('Please pick the days that you want the event to take place')
    else:
        input_fields = {'start_date': document['start_date'].value, 'end_date': document['end_date'].value,
                        'start_time': document['start_time'].value, 'end_time': document['end_time'].value,
                        'min_duration': int(document['duration_bar'].value),
                        'min_participants': int(document['min_participant'].value),
                        'schedule_mode': document['mode'].value.lower(),
                        'day_pick': day_pick}

        # Check schedule mode
        if document['mode'].value == 'Balanced':
            input_fields['schedule_mode'] = 'mixed'
            input_fields['ideal_duration'] = int(document['ideal_duration_bar'].value)

        # Read important people
        people_pick_lst = []
        for n in document['important_people'].child_nodes:
            people_pick_lst.append(n.id)
        input_fields['important_people'] = people_pick_lst
        input_fields['important_people_all'] = document['all_important'].checked

        # Read the group(s) that is scheduling for
        selected_groups = []
        for g in document['group_selection'].child_nodes:
            selected_groups.append(g.id.split('_')[0])
        input_fields['schedule_groups'] = selected_groups

        # Read customized event name (can be left empty)
        input_fields['event_name'] = document['event_name'].value

        # Extra info
        input_fields['scheduler_user'] = user

        def schedule_response(req):
            if req.status == 201:
                # Show success message
                alert('An event has been scheduled!')

                schedule = req.json
                # Add element on web page
                add_new_event(schedule)
            else:
                alert('Unfortunately such an event is not able to schedule. You may check your inputs')

        # Send to the server
        post_data(json.dumps(input_fields), 'schedule_event', callback=schedule_response)


def save_preference(ev):
    pass

# document['save_pref'].bind('click', save_preference)
