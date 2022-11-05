from browser import confirm, alert
from ajax_call import post_data
from sub_window_template import *
from ajax_call import get_data
from shortcut_function import copy_to_clipboard


def add_right_grid(user):
    right_grid = DIV(Class='container_grid')
    group_container = DIV(Class='group_container')
    groups = DIV(id='groups', groups='', Class='groups')
    group_container <= groups
    # groups <= group_template('yes', 'beep', 'beep')
    group_container <= DIV('Create a group', id='create_group', Class='td button_blue group_button')
    group_container <= DIV('Join a group', id='join_group', Class='td button_blue group_button')
    right_grid <= group_container
    document <= right_grid

    @bind('#create_group', 'click')
    def create_group_window(event):
        sub_window = draw_sub_window('create_group')
        sub_window <= (DIV('Group name', Class='td in_line') + INPUT(id='create_group_name', Class='in_line'))
        sub_window <= DIV('Create group and copy your invitation code', id='create_button', Class='td button_blue')

        @bind('#create_button', 'click')
        def create_group(ev):
            group_name = document['create_group_name'].value
            if group_name == '':
                alert('Please give a group name')
            else:
                get_data({'title': 'create',
                          'user': user,
                          'name': document['mergenda_acc_1'].value,
                          'email': document['mergenda_acc_2'].value,
                          'group_name': group_name},
                         'group_assignment',
                         mode='text', callback=group_created)

    @bind('#join_group', 'click')
    def join_group_window(event):
        sub_window = draw_sub_window('join_group')
        sub_window <= (DIV('Invitation code', Class='td in_line') + INPUT(id='join_group_code', Class='in_line'))
        sub_window <= DIV('Join this group!', id='join_button', Class='td button_blue')

        @bind('#join_button', 'click')
        def join_group(ev):
            join_code = document['join_group_code'].value
            if join_code == '':
                alert('Please enter a invitation code')
            elif join_code in document['groups'].attrs['groups'].split('_'):
                alert('You are already in this group')
            else:
                # JSON mode
                get_data({'title': 'join',
                          'user': user,
                          'name': document['mergenda_acc_1'].value,
                          'email': document['mergenda_acc_2'].value,
                          'join_code': join_code},
                         'group_assignment',
                         callback=group_joined)

    return groups


# Event taking place after creating a group
def group_created(req):
    invitation_code = req.text
    # Add a temporary element
    group_invitation = INPUT(value=invitation_code, readonly=True, Class='in_line')
    document['sub_window_container_create_group'] <= (DIV('Invitation code', Class='td in_line') + group_invitation)
    # Copy to the clipboard
    copy_to_clipboard(group_invitation)
    alert('A new group has been created! \n\n'
          'The invitation code is automatically copied to your clipboard. Share it with your mates and let them in!\n\n'
          "You can still access this code by clicking the 'invite' button.")

    # Close the sub window
    fire_close_sub_window('create_group')

    # Add group code to existing-groups list
    document['groups'].attrs['groups'] += f'_{invitation_code}'


# Event taking place after joining a group
def group_joined(req):
    new_group_info = req.json

    # Show success message
    alert("Woohoo! You've joined a group! \n\n"
          "You can go schedule a meeting with other members and enjoy!")
    # Close the sub window
    fire_close_sub_window('join_group')

    # Add new group module
    user = new_group_info.pop('user')
    add_groups(new_group_info.items(), document['groups'], user)


def edit_group_name(ev):
    group_code = ev.target.id.split('_')[-1]
    group_name_ele = document[f'group_name_{group_code}']
    if document[f'edit_group_name_{group_code}'].attrs['edit'] == 'off':
        document[f'edit_group_name_{group_code}'].attrs['edit'] = 'on'
        ev.target.parent.replaceChild(INPUT(value=f'{group_name_ele.text}',
                                            id=f'group_name_{group_code}',
                                            Class='group_name_input'),
                                      ev.target.parent.lastChild)
        document[f'group_name_{group_code}'].bind('blur', edit_group_name)
    else:
        document[f'edit_group_name_{group_code}'].attrs['edit'] = 'off'
        ev.target.parent.replaceChild(SPAN(f'{group_name_ele.value}',
                                           id=f'group_name_{group_code}',
                                           Class='in_line group_name_span'),
                                      ev.target.parent.lastChild)

        # Check if name changes and send new group name to the server
        if group_name_ele.value != document[f'edit_group_name_{group_code}'].attrs['pre-name']:
            post_data({'change': 'group_name', 'group_code': group_code, 'new_name': group_name_ele.value})
            document[f'edit_group_name_{group_code}'].attrs['pre-name'] = group_name_ele.value


def select_group(ev):
    group_code = ev.target.id.split('_')[-1]
    group_name = ev.target.parent.child_nodes[-1].text
    # Add or remove group from the group selection list
    if ev.target.attrs['select'] == 'false':
        document['group_selection'] <= LI(f'{group_name}', id=f'{group_code}_selected')
        ev.target.attrs['select'] = 'true'
    else:
        document['group_selection'].removeChild(document[f'{group_code}_selected'])
        ev.target.attrs['select'] = 'false'

    # Check the status of schedule button
    if 'grey_background' in list(document['schedule'].classList):
        schedule_disable = True
    else:
        schedule_disable = False
    # Enable or disable the schedule button
    if len(document['group_selection'].child_nodes) == 0 and not schedule_disable:
        document['schedule'].classList.add('grey_background')
    elif len(document['group_selection'].child_nodes) != 0 and schedule_disable:
        document['schedule'].classList.remove('grey_background')


def invite_member(ev):
    group_code = ev.target.id.split('_')[-1]
    sub_window = draw_sub_window(group_code)
    group_invitation = INPUT(value=group_code, readonly=True, Class='in_line')
    sub_window <= (DIV('Invitation code', Class='td in_line') +
                   group_invitation +
                   DIV('&#128203', id='copy_invitation_code', Class='in_line mini_button'))
    # Copy to the clipboard
    copy_to_clipboard(group_invitation)

    @bind('#copy_invitation_code', 'click')
    def copy_invitation_code(event):
        copy_to_clipboard(group_invitation)


def quit_group(ev):
    group_code = ev.target.id.split('_')[-1]
    if confirm('Are you sure you want to quit this group?'):
        get_data({'user': ev.target.attrs['user'],
                  'title': 'quit',
                  'name': document['mergenda_acc_1'].value,
                  'group_code': group_code},
                 'group_assignment',
                 mode='text', callback=group_withdrawn)


def group_withdrawn(req):
    group_code = req.text
    # Delete group code from the existing-groups list
    groups_lst = document['groups'].attrs['groups'].split('_')
    groups_lst.remove(group_code)
    document['groups'].attrs['groups'] = '_'.join(groups_lst)
    # Remove module on page
    group_block = document[f'group_name_{group_code}'].parent.parent
    group_block.parent.removeChild(group_block)


# Template of adding one group to the groups container
def group_template(group_code, group_name, group_parent, user, *member):
    group = DIV(Class='one_group')
    # Group title
    group <= DIV(SPAN('&#9998', id=f'edit_group_name_{group_code}', edit='off', pre_name=f'{group_name}',
                      Class='mini_button') +
                 SPAN('Group - ', id=f'select_group_{group_code}', select='false',
                      Class='italic grey_font group_select') +
                 SPAN(f'{group_name}', id=f'group_name_{group_code}',
                      Class='in_line group_name_span'),
                 Class='group_title')
    group_member = TABLE(Class='user_group')
    # Add group members
    for m in member:
        group_member <= TR(TD(f'&#128100 {m}', Class='group_member') +
                           TD(INPUT(type='checkbox', Class='select_people')))
    group_member <= TR(style={'height': '20px'})  # Vertical spacing
    # Functional buttons
    group_member <= TR(TD('Invite', id=f'invite_member_{group_code}', Class='button_blue', colspan=2))
    group_member <= TR(TD('Quit', id=f'quit_group_{group_code}', user=user, Class='button_red', colspan=2))
    # Add to parent elements
    group <= group_member
    group_parent <= group  # Add to the container

    # Bind events
    document[f'edit_group_name_{group_code}'].bind('click', edit_group_name)
    document[f'select_group_{group_code}'].bind('click', select_group)
    document[f'invite_member_{group_code}'].bind('click', invite_member)
    document[f'quit_group_{group_code}'].bind('click', quit_group)


def add_groups(group_info_items, group_parent, user):
    groups_lst = []
    for code, info_dict in group_info_items:
        groups_lst.append(code)
        name, member_lst = info_dict['name'], info_dict['member']
        group_template(code, name, group_parent, user, *member_lst)
    document['groups'].attrs['groups'] = '_'.join(groups_lst)

    # Bind event to all checkboxes
    @bind('input.select_people', 'click')
    def select_member(ev):
        person_name = ev.target.parent.parent.firstChild.text[3:]
        if ev.target.checked:
            document['important_people'] <= LI(f'{person_name}', id=f'{person_name}')
        else:
            document['important_people'].removeChild(document[f'{person_name}'])
