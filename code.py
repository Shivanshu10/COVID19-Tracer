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
    python3_path=system('where python3' if name == 'nt' else 'which python3')
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

def subscribe():
    # asks user which country to subscribe
    # type of data to subscribe
    # create a file containing subscription details
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

def countrytoCode():
    # convert country to country code
    country=input("Country: ")
    try:
        country_code = countries.search_fuzzy(country)[0].alpha_2
    except LookupError:
        print("Couldn't find country try different one")
        return countrytoCode()
    return(country_code)

def statusCountry(site):
    # get country name whose data is required
    # takes API site as param
    # returns python  dict reprsenting status of country
    # request API using GET method
    # convert response string to python dict
    # if error occurs print error code and reason of error
    subUrl = '/status'
    country=countrytoCode()
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

def statusCountryDate(site):
    # get country name and date at which status is required
    # get date on which data is required
    # takes API site as param
    # returns python dict reprsenting status of country till given date
    # request API using GET method
    # convert response string to python dict
    # if error occurs print error code and reason of error
    country=countrytoCode()
    subUrl= '/status'
    date=input("Date (YYYY-MM-DD): ")
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

def diffCountry(site):
    # get country name
    # takes API site as param
    # returns python dict reprsenting difference
    # of current case and previous case
    # request API using GET method
    # convert response string to python dict
    # if error occurs print error code and reason of error
    country=countrytoCode()
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

def predictionCountry(site):
    # get country name
    # takes API site as param
    # returns python dict reprsenting data 
    # of prediction of cases in next 2 weeks using ML
    # request API using GET method
    # convert response string to python dict
    # if error occurs print error code and reason of error
    country=countrytoCode()
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

def timeCases(site):
    # get country name
    # takes API site as param
    # returns python dict reprsenting data of cases by country and time
    # request API using GET method
    # convert response string to python dict
    # if error occurs print error code and reason of error
    country=countrytoCode()
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

def menu(site, iconname):
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
            parse(statusCountry(site))
        elif (choice==2):
            parse(statusCountryDate(site))
        elif (choice==3):
            site = 'https://covid19-api.org/api'
            parse(diffCountry(site))
        elif (choice==4):
            listParse(predictionCountry(site))
        elif (choice==5):
            listParse(timeCases(site))
        elif (choice==6):
            subscribe()
        elif (choice == 7):
            rmSubscribe()
        elif (choice==99):
            exit(0)
        else:
            print("Not a valid input")\

def main():
    # main method
    clear()
    menu('https://covid19-api.org/api', 'covid')

if __name__ == "__main__":
    # call main when this python file is not imported
    # to other python file
    main()
