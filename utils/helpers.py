import datetime

def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.datetime.now().strftime("%A, %d %B %Y")

def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning sir!"
    elif hour < 18:
        return "Good afternoon sir!"
    else:
        return "Good evening sir!"
