
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
ICON_NAME="covid"
SCHEDULE_SCRIPT="schedulescript.py"
SCHEDULED="scheduled.txt"

from requests import get
# make a get request
from json import loads
# convert json string to python dicitionory
from sys import exit
# exit program with an exit code and check shell cmd output
from pycountry import countries
# convert country to country code
from os import system, name, getcwd
# Used detect Operating System, getcwd and execute shell cmd
from pynotifier import Notification
# create notification
from ast import literal_eval
# convert str having dict to dict

def init(scheduled):
    with open(scheduled, "w") as scheduled:
        scheduled.write(str(0))

def clear():
    # Clear terminal showing previous outputs
    system('cls' if name == 'nt' else 'clear')

def schedule(schedule_script, scheduled):
    # param, name of script to schedule
    # check if winows or linux and call
    # corresponding func
    setScheduled(scheduled, str(1))
    if (name=='nt'):
        scheduleWindows(schedule_script)
    else:
        scheduleLinux(schedule_script)

def scheduleLinux(schedule_script):
    # takes name of script to schedule on linux
    # schedule a ps in linux using crontab
    # schedule script on every boot
    from subprocess import check_output
    try:
        usrname=check_output('whoami').decode('utf-8')[:-1]
        # cmd='@reboot '+usrname+' export DISPLAY=:0.0 && '
        pwd=getcwd()
        cmd='@reboot '+ usrname + " cd " + pwd + ' && export DISPLAY=:0.0 && '
        python3_path=check_output(['which', 'python3']).decode('utf-8')[:-1] 
        cmd+=(python3_path+" "+getcwd()+"/"+schedule_script) 
        with open("schedule.sh", 'w') as script:
            script.write("sudo echo \""+cmd+"\n\" >> /etc/crontab" )
        system("sudo bash schedule.sh")
    except Exception as err:
        print("Error: " + err)
        exit(1)

def scheduleWindows(schedule_script):
    # takes name of script to schedule on windows
    # schedule a ps on every boot
    pass

def rmScheduleLinux(schedule_script):
    # remove from task scheduler linux
    from subprocess import check_output
    usrname=check_output('whoami').decode('utf-8')[:-1]
    cmd='@reboot '+usrname+' export DISPLAY=:0.0 && '
    python3_path=check_output(['which', 'python3']).decode('utf-8')[:-1] 
    cmd+=(python3_path+" "+getcwd()+"/"+schedule_script) 
    with open("schedule.sh", 'w') as script:
        script.write("sudo sed \"/"+cmd+"/d"+"\" /etc/crontab > /etc/crontab")
    system("sudo bash schedule.sh")

def rmScheduleWindows():
    # rm from task scheduler windows 
    pass

def rmSubscribe(schedule_script, scheduled):
    # remove subscription
    # clear subscription data
    # remove from schedule jobs
    # call corresponding func based on OS
    clear()
    print("Unsuscribe")
    choice=(read("Remove All Subscription (y/n): ")).lower()
    if (choice=='y'):
        if (name=='nt'):
            rmScheduleWindows(schedule_script)
        else:
            rmScheduleLinux(schedule_script)
        setScheduled(scheduled, str(0))
        system("echo \"\" > subscribe.txt")
    else:
        country=(read("Country to Unsubscribe")).lower()
        print("Type of Subscription")
        print("1. Get status by Country")
        print("2. Difference between Latest state and previous one by country")
        type_subscription=int(input("Choose> "))
        clear()
        infos=[]
        with open('subscribe.txt', 'r') as subscription_file:
            for line in subscription_file:
                data=literal_eval(line)
                if (data['country']!=country or data['type']!=type_subscription):
                    infos.append(data)
        with open('subscribe.txt', 'w') as subscription_file:
            for info in infos:
                subscription_file.write(str(info)+"\n")

def subscribe(schedule_script, scheduled):
    # takes script to schedule as parameter
    # clear previous subscriptions
    # asks user which country to subscribe
    # type of data to subscribe
    # create a file containing subscription details
    # schedule given script
    country=input("Country to subscribe: ")
    clear()
    print("Type of Subscription:")
    print("1. Get status by Country")
    print("2. Difference between Latest state and previous one by country")
    type_subscription=int(input("Choose> "))
    clear()
    subscription_data={'country': country.lower(), 'type': type_subscription}
    with open('subscribe.txt', 'a') as subscription_file:
        subscription_file.writelines(str(subscription_data)+"\n")
    if (isScheduled(scheduled)==0):
        schedule(schedule_script, scheduled)

def isScheduled(scheduled):
    with open(scheduled, 'r') as scheduled:
        return int(scheduled.read())

def setScheduled(scheduled, data):
    with open(scheduled, 'w') as scheduled:
        scheduled.write(data)

def checkSubscription():
    # read subscription file
    data=[]
    with open('subscribe.txt', 'r') as subscription_file:
        for line in subscription_file:
            yield(literal_eval(line))

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
        resp=get(site+subUrl+"/"+countrytoCode(country))
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
        resp=get(site+subUrl+"/"+countrytoCode(country), params={'date':date})
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
        resp=get(site+"/diff/"+countrytoCode(country))
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
        resp=get(site+"/prediction/"+countrytoCode(country))
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
        resp=get(site+"/timeline/"+countrytoCode(country))
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

def menu(site, schedule_script, scheduled):
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
            country=countrytoCode(read('Country'))
            parse(statusCountry(site, country))
        elif (choice==2):
            country=countrytoCode(read('Country'))
            date=read('Date (YYYY-MM-DD)')
            parse(statusCountryDate(site, country, date))
        elif (choice==3):
            country=countrytoCode(read('Country'))
            parse(diffCountry(site, country))
        elif (choice==4):
            country=countrytoCode(read('Country'))
            listParse(predictionCountry(site, country))
        elif (choice==5):
            country=countrytoCode(read('Country'))
            listParse(timeCases(site, country))
        elif (choice==6):
            subscribe(schedule_script, scheduled)
        elif (choice == 7):
            rmSubscribe(schedule_script, scheduled)
        elif (choice==99):
            exit(0)
        else:
            print("Not a valid input")

def main():
    # main method
    # clear screen
    # show menu
    clear()
    init(SCHEDULED)
    menu(API, SCHEDULE_SCRIPT, SCHEDULED)

if __name__ == "__main__":
    # call main when this python file is not imported
    # to other python file
    main()
