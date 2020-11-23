
from pynotifier import Notification
# create notification

from os import name, getcwd

def createNotification(notifyTitle, notifyDescription, notifyIcon):
    # params are notification title, descr, iconname
    # pass full path of icon
    # select icon type accrdg to os name
    # urgent notification
    notifyIcon=getcwd()+'/'+notifyIcon
    if (name == 'nt'):
        notifyIcon+='.ico'
    else:
        notifyIcon+='.png'
    Notification(
        title=notifyTitle,
        description=notifyDescription,
        icon_path=notifyIcon, # On Windows .ico is required, on Linux - .png
        duration=5,                              # Duration in seconds
        urgency=Notification.URGENCY_CRITICAL
    ).send()

