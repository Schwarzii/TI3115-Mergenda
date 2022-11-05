from browser import ajax, alert
from browser.session_storage import storage

if len(storage) != 0:
    server_host = storage['url']
else:  # Must log in account first
    server_host = '127.0.0.1:5000'


# Show server response message as alert
def alert_resp(req):
    alert(req.text)


# Send data to the server using POST method
def post_data(send_data, route='update', callback=alert_resp):
    ajax.post(f"https://{server_host}/{route}",
              data=send_data,
              oncomplete=callback)


# Send data to the server using GET method
def get_data(send_data, route, callback=alert_resp, mode='json'):
    ajax.get(f"https://{server_host}/{route}",
             data=send_data,
             mode=mode,
             cache=True,
             oncomplete=callback)
