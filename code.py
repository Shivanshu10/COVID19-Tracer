# TODO
# test 

# Later
# GUI
# pyaudio
# windows notification

# TASK (GAURAV)
# make functions for windows

# docs of api
# https://documenter.getpostman.com/view/10877427/SzYW2f8n?version=latest

API='https://covid19-api.org/api'
ICON_NAME=""
SCHEDULE_SCRIPT=""

from requests import get
# make a get request
from json import loads
# convert json string to python dicitionory
from sys import exit
# exit program with an exit code
from pycountry import countries
# convert country to country code
from os import system, name, getcwd
# Used detect Operating System, getcwd and execute shell cmd
from pynotifier import Notification
# create notification
from crontab import CronTab
# schedule script

def schedule(schedule_script):
    # param, name of script to schedule
    # check if winows or linux and call
    # corresponding func
    if (name=='nt'):
        scheduleWindows(schedule_script)
    else:
        scheduleLinux(schedule_script)

def scheduleLinux(schedule_script):
    # takes name of script to schedule on linux
    # schedule a ps in linux using crontab
    # schedule script on every boot
    cron=CronTab()
    cmd='export DISPLAY=:0.0 && '
    python3_path=system('which python3')
    cmd+=(python3_path+" "+getcwd()+"/"+schedule_script) 
    schedule=cron.new(command=cmd, comment='COVID19 Tracer Info notification')
    schedule.every_reboot()
    cron.write()

def scheduleWindows(schedule_script):
    # takes name of script to schedule on windows
    # schedule a ps on every boot
    pass

def rmScheduleLinux():
    # remove from task scheduler linux
    cron=CronTab()
    jobs=cron.find_comment("COVID19 Tracer Info notification")
    for job in jobs:
        cron.remove(job)

def rmScheduleWindows():
    # rm from task scheduler windows 
    pass

def rmSubscribe():
    # remove subscription
    # clear subscription data
    # remove from schedule jobs
    # call corresponding func based on OS
    if (name=='nt'):
        rmScheduleWindows()
    else:
        rmScheduleLinux()
    with open('subscribe.txt', 'w') as subscription_file:
        subscription_file.seek(0)
        subscription_file.write("")

def subscribe(schedule_script):
    # takes script to schedule as parameter
    # clear previous subscriptions
    # asks user which country to subscribe
    # type of data to subscribe
    # create a file containing subscription details
    # schedule given script
    rmSubscribe()
    country=input("Country to subscribe: ")
    clear()
    print("Type of Subscription:")
    print("1. Get status by Country")
    print("2. Difference between Latest state and previous one by country")
    type_subscription=int(input("Choose> "))
    clear()
    subscription_data={'country': country, 'type': type_subscription}
    with open('subscribe.txt', 'wb') as subscription_file:
        subscription_file.seek(0)
        subscription_file.write(subscription_data)
    schedule(schedule_script)

def checkSubscription():
    # read subscription file
    with open('subscribe.txt', 'rb') as subscription_file:
        subscription_data=subscription_file.read()
    return (subscription_data)

def notification(notifyTitle, notifyDescription, notifyIcon):
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

def parse(dic):
    # takes dict as param
    # repr json data
    # iterate over every key, and print element at that key
    print("\n**********************")
    for key in dic.keys():
        print(key +" : "+str(dic[key]))
    print("\n**********************\n")
    input("Press Enter to continue....") 
    clear() 

def listParse(list):
    # takes list as param
    # list contains dic
    print("\n**********************")
    for dic in list:
        for key in dic.keys():
           print(key +" : "+str(dic[key]))
        print("\n",end="")
    print("\n**********************\n")
    input("Press Enter to continue....") 
    clear()

def clear():
    # Clear terminal showing previous outputs
    system('cls' if name == 'nt' else 'clear')

def read(key):
    return(input(key+": "))

def countrytoCode(country):
    # convert country to country code
    try:
        country_code = countries.search_fuzzy(country)[0].alpha_2
    except LookupError:
        print("Couldn't find country try different one")
        return countrytoCode()
    return(country_code)

def statusCountry(site, country):
    # get country name whose data is required
    # takes API site as param
    # returns python  dict reprsenting status of country
    # request API using GET method
    # convert response string to python dict
    # if error occurs print error code and reason of error
    subUrl = '/status'
    try:
        resp=get(site+subUrl+"/"+country)
    except Exception as err:
        print("Error: " + str(err))
        exit(1)
    if (resp.status_code==200):
        return(loads(resp.content))
    else:
        print("Error: " + str(resp.status_code) + ":" + resp.reason)
        exit(1)

def statusCountryDate(site, country, date):
    # get country name and date at which status is required
    # get date on which data is required
    # takes API site as param
    # returns python dict reprsenting status of country till given date
    # request API using GET method
    # convert response string to python dict
    # if error occurs print error code and reason of error
    subUrl= '/status'
    try:
        resp=get(site+subUrl+"/"+country, params={'date':date})
        #print(resp.url)
    except Exception as err:
        print("Error: " + str(err))
        exit(1)
    if (resp.status_code==200):
        return(loads(resp.content))
    else:
        print("Error: " + str(resp.status_code) + ":" + resp.reason)
        exit(1)

def diffCountry(site, country):
    # get country name
    # takes API site as param
    # returns python dict reprsenting difference
    # of current case and previous case
    # request API using GET method
    # convert response string to python dict
    # if error occurs print error code and reason of error
    try:
        resp=get(site+"/diff/"+country)
    except Exception as err:
        print("Error: " + str(err))
        exit(1)
    if (resp.status_code==200):
        return(loads(resp.content))
    else:
        print("Error: " + str(resp.status_code) + ":" + resp.reason)
        exit(1)

def predictionCountry(site, country):
    # get country name
    # takes API site as param
    # returns python dict reprsenting data 
    # of prediction of cases in next 2 weeks using ML
    # request API using GET method
    # convert response string to python dict
    # if error occurs print error code and reason of error
    try:
        resp=get(site+"/prediction/"+country)
    except Exception as err:
        print("Error: " + str(err))
        exit(1)
    if (resp.status_code==200):
        return(loads(resp.content))
    else:
        print("Error: " + str(resp.status_code) + ":" + resp.reason)
        exit(1)   

def timeCases(site, country):
    # get country name
    # takes API site as param
    # returns python dict reprsenting data of cases by country and time
    # request API using GET method
    # convert response string to python dict
    # if error occurs print error code and reason of error
    try:
        resp=get(site+"/timeline/"+country)
    except Exception as err:
        print("Error: " + str(err))
        exit(1)
    if (resp.status_code==200):
        return(loads(resp.content))
    else:
        print("Error: " + str(resp.status_code) + ":" + resp.reason)
        exit(1)

def getChoice():
    #Method to get user Input
    try:
        choice = int(input("Choice> "))
    except ValueError:
        print("Not a valid input")
        return getChoice()
    return choice

def menu(site, schedule_script):
    # pass site url as parameter
    # get what user wants to do
    # and call corresponding function
    while (True):
        print("COVID19 Tracer with ML prediction")
        print("1. Get status by Country")
        print("2. Get status by country and date")
        print("3. Difference between Latest state and previous one by country")
        print("4. Get two weeks prediction by specific country")
        print("5. Get timeline of cases by Country")
        print("6. Subscribe")
        print("7. Remove Subscription")
        print("99. Exit")
        choice = getChoice()
        if (choice==1):
            country=countrytoCode(read('country'))
            parse(statusCountry(site, country))
        elif (choice==2):
            country=countrytoCode(read('country'))
            date=read('date (YYYY-MM-DD)')
            parse(statusCountryDate(site, country, date))
        elif (choice==3):
            country=countrytoCode(read('country'))
            parse(diffCountry(site, country))
        elif (choice==4):
            country=countrytoCode(read('country'))
            listParse(predictionCountry(site, country))
        elif (choice==5):
            country=countrytoCode(read('country'))
            listParse(timeCases(site, country))
        elif (choice==6):
            subscribe(schedule_script)
        elif (choice == 7):
            rmSubscribe()
        elif (choice==99):
            exit(0)
        else:
            print("Not a valid input")

def main():
    # main method
    # clear screen
    # show menu
    clear()
    menu(API, SCHEDULE_SCRIPT)

if __name__ == "__main__":
    # call main when this python file is not imported
    # to other python file
    main()
