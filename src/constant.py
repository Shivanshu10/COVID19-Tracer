# constants and global var
from os import getcwd
from os import name
from sys import exit

API='https://covid19-api.org/api'
ICON_NAME="/resource/icon/covid"
SCHEDULE_SCRIPT="/schedulescript.pyw"
SCHEDULED="/resource/data/scheduled.txt"
SUBSCRIPTION="/resource/data/subscribe.txt"
BASH_SCRIPT="/resource/script/schedule.sh"
PWD=""
LOG="/resource/logs/log.txt"
TMP="/resource/temp/tmpfile.txt"

def init():
    global ICON_NAME
    global SCHEDULE_SCRIPT
    global SCHEDULED
    global SUBSCRIPTION
    global BASH_SCRIPT
    global PWD
    global LOG
    global TMP
    PWD=getcwd()
    ICON_NAME=PWD+ICON_NAME
    SCHEDULE_SCRIPT=PWD+SCHEDULE_SCRIPT
    SCHEDULED=PWD+SCHEDULED
    SUBSCRIPTION=PWD+SUBSCRIPTION
    BASH_SCRIPT=PWD+BASH_SCRIPT
    LOG=PWD+LOG
    TMP=PWD+TMP
    if (name == 'nt'):
        # changing '/' to '\' for windows
        ICON_NAME= ICON_NAME.replace("/", "\\")
        SCHEDULE_SCRIPT= SCHEDULE_SCRIPT.replace("/", "\\")
        SCHEDULED= SCHEDULED.replace("/", "\\")
        SUBSCRIPTION= SUBSCRIPTION.replace("/", "\\")
        LOG= LOG.replace("/", "\\")
        TMP= TMP.replace("/", "\\")