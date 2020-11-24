from os import system, name
from ast import literal_eval
import menu
import userInput
import scheduler
import constant

def subscribe(schedule_script, scheduled):
    # takes script to schedule as parameter
    # clear previous subscriptions
    # asks user which country to subscribe
    # type of data to subscribe
    # create a file containing subscription details
    # schedule given script
    country=input("Country to subscribe: ")
    menu.clear()
    print("Type of Subscription:")
    print("1. Get status by Country")
    print("2. Difference between Latest state and previous one by country")
    type_subscription=int(input("Choose> "))
    menu.clear()
    subscription_data={'country': country.lower(), 'type': type_subscription}
    with open(constant.SUBSCRIPTION, 'a') as subscription_file:
        subscription_file.writelines(str(subscription_data)+"\n")
    if (isScheduled(scheduled)==0):
        scheduler.schedule(schedule_script, scheduled)

def rmSubscribe(schedule_script, scheduled):
    # remove subscription
    # clear subscription data
    # remove from schedule jobs
    # call corresponding func based on OS
    menu.clear()
    print("Unsuscribe")
    choice=(userInput.read("Remove All Subscription (y/n): ")).lower()
    if (choice=='y'):
        if (name=='nt'):
            scheduler.rmScheduleWindows(schedule_script)
        else:
            scheduler.rmScheduleLinux(schedule_script)
        setScheduled(scheduled, str(0))
        system("rm " + constant.SUBSCRIPTION)
        system("rm " + constant.BASH_SCRIPT)
        system("rm " + constant.SCHEDULED)
        system("rm " + constant.LOG)
        exit(0)

    else:
        country=(userInput.read("Country to Unsubscribe")).lower()
        print("Type of Subscription")
        print("1. Get status by Country")
        print("2. Difference between Latest state and previous one by country")
        type_subscription=int(input("Choose> "))
        menu.clear()
        infos=[]
        with open(constant.SUBSCRIPTION, 'r') as subscription_file:
            for line in subscription_file:
                data=literal_eval(line)
                if (data['country']!=country or data['type']!=type_subscription):
                    infos.append(data)
        with open(constant.SUBSCRIPTION, 'w') as subscription_file:
            for info in infos:
                subscription_file.write(str(info)+"\n")


def isScheduled(scheduled):
    with open(scheduled, 'r') as scheduled:
        return int(scheduled.read())

def setScheduled(scheduled, data):
    with open(scheduled, 'w') as scheduled:
        scheduled.write(data)

def checkSubscription():
    # read subscription file
    #data=[]
    with open(constant.SUBSCRIPTION, 'r') as subscription_file:
        for line in subscription_file:
            yield(literal_eval(line))
