from browser import document, window


def copy_to_clipboard(element):
    element.focus()
    element.select()
    document.execCommand("copy")


def round_nearest_time(time_str, multiple=15):
    time = time_str.split(':')
    hour, minute = int(time[0]), int(time[1])
    minute = multiple * round(minute / multiple)
    if minute == 60:
        hour += 1
        minute = 0
    return f'{hour:02}:{minute:02}'


def fire_mouse_event(element, event='click'):
    element.dispatchEvent(window.MouseEvent.new(event))
