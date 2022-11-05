from browser import document, window, ajax, timer
from browser.session_storage import storage
from browser.html import *

# All login components
container = TABLE(id='container')
# User input
container <= TR(TD('Username', Class='title_col') + TD(INPUT(id='username')))
container <= TR(TD('Password', Class='title_col') +
                TD(INPUT(id='password', type='password')) +
                TD('&#128065', id='show_pass', mode='pass', Class='mini_col'))
container <= TR(id='double_pass_row', style={'height': '37px'})
# Error prompt
container <= TR(TD('', id='response', colspan=2, Class='response'))
# Functional buttons
container <= TR(TD('Login', colspan=2, Class='button', id='login'))
container <= TR(TD('Sign up', colspan=2, Class='button', id='signup'))
# Show in the window
document <= container

server_host = 'schwarzi.pythonanywhere.com'
# server_host = '127.0.0.1:5000'


def prompt(message):
    document['response'].text = message


def check_none_input():
    if document['username'].value == '':
        prompt("Please enter your username")
        document['username'].bind('focus', cancel_prompt)
        return True
    elif document['password'].value == '':
        prompt("Please enter your password")
        document['password'].bind('focus', cancel_prompt)
        return True
    else:
        return False


def redirection():
    storage['username'] = document['username'].value  # Save login user info to session storage
    storage['password'] = document['password'].value
    storage['url'] = server_host
    window.location.href = "../Main_UI/index.html"  # Redirect to the main UI


def login(ev):
    if not check_none_input():  # No empty input fields of username and password
        ajax.get(f"http://{server_host}/login",
                 data={'user': document['username'].value, 'pass': document['password'].value},
                 cache=True,
                 oncomplete=resp_redirect)


def resp_redirect(req):
    if req.status == 201:  # Successful login
        redirection()
    else:  # Show error prompt
        document['username'].bind('focus', cancel_prompt)
        document['password'].bind('focus', cancel_prompt)
        prompt(req.text)


def cancel_prompt(ev):
    prompt('')
    ev.target.unbind('focus', cancel_prompt)


def back_to_login(ev):
    prompt('')

    document['login'].style['color'] = 'initial'
    document['login'].text = 'Login'
    document['login'].bind('click', login)
    document['login'].unbind('click', back_to_login)

    document['signup'].bind('click', signup_layout)
    document['signup'].unbind('click', signup)

    document['double_pass_row'].innerHTML = ''


def signup_layout(ev):
    prompt('')

    document['login'].style['color'] = '#a9a9a9'
    document['login'].text = 'Back to login'
    document['login'].unbind('click', login)
    document['login'].bind('click', back_to_login)

    document['signup'].unbind('click', signup_layout)
    document['signup'].bind('click', signup)

    document['double_pass_row'] <= (TD('Confirm password', Class='title_col') +
                                    TD(INPUT(id='password_double', type='password')) +
                                    TD('&#128065', id='show_double_pass', mode='pass', Class='mini_col'))
    document['show_double_pass'].bind('click', show_pass)


def signup(ev):
    if not check_none_input():  # No empty input fields of username and password
        document['password_double'].bind('focus', cancel_prompt)
        if document['password_double'].value == '':
            prompt("Please enter your password again")
        else:
            if document['password'].value == document['password_double'].value:
                ajax.get(f"http://{server_host}/signup",
                         data={'user': document['username'].value, 'pass': document['password'].value},
                         cache=True,
                         oncomplete=signup_success)
            else:
                prompt("Two passwords don't match")
                document['password'].bind('focus', cancel_prompt)


def signup_success(req):
    if req.text == 'account exists':
        prompt('Account exists! You may click "Back to login"')
        document['username'].bind('focus', cancel_prompt)
        document['password'].bind('focus', cancel_prompt)
        document['password_double'].bind('focus', cancel_prompt)
    elif req.status == 201:
        document['login'].unbind('click', back_to_login)
        document['signup'].unbind('click', signup)
        document['container'] <= TR(TD("Successfully signed up!", Class='signup', colspan=2,
                                       style={'padding-top': '10px'}))
        document['container'] <= TR(TD("You will automatically login in 2 seconds", Class='signup', colspan=2))
        timer.set_timeout(redirection, 2000)


def show_pass(ev):
    if ev.target.attrs['mode'] == 'pass':  # Show password input
        ev.target.innerHTML = '&#9729'
        ev.target.parent.child_nodes[1].firstChild.type = 'text'
        ev.target.attrs['mode'] = 'text'
    else:  # Hide password input
        ev.target.innerHTML = '&#128065'
        ev.target.parent.child_nodes[1].firstChild.type = 'password'
        ev.target.attrs['mode'] = 'pass'


document['login'].bind('click', login)
document['signup'].bind('click', signup_layout)
document['show_pass'].bind('click', show_pass)
