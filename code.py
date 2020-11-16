# TODO
# Get choice of user
# request the API server as per choice
# show data to user
# Find what is webhook

# Later
# GUI
# pyaudio
# windows notification

# TASK (GAURAV)
# find what is webhooks
# API provides a facility of webhooks
# but i couldnt understand what it is

# docs of api
# https://documenter.getpostman.com/view/10877427/SzYW2f8n?version=latest

from requests import get
# make a get request
from json import loads
# convert json string to python dicitionory
from os import exit
# exit program with an exit code

def statusCountry(site):
    # takes API site as param
    # returns python  dict reprsenting status of all country
    # request API using GET method
    # convert response string to python dict
    # if error occurs print error code and reason of error
    resp=get(site)
    if (resp.status_code==200):
        json_dict=loads(resp.content)
    else:
        print("Error " + resp.status_code + ":" + resp.reason)
        exit(1)

def statusCountryDate(site):
    # takes API site as param
    # get date on which data is required
    # returns python dict reprsenting status of all country
    # on specific date
    # request API using GET method
    # convert response string to python dict
    # if error occurs print error code and reason of error
    date=input("Date (YYYY-MM-DD): ")
    resp=get(site, data={'date':date})
    if (resp.status_code==200):
        json_dict=loads(resp.content)
    else:
        print("error " + resp.status_code + ":" + resp.reason)
        exit(1)


def diff(site):
    pass

def diffCountry(site):
    pass

def predictionCountry(site):
    pass

def menu(site):
    # pass site url as parameter
    # get what user wants to do
    # and call corresponding function
    while (True):
        print("COVID19 Tracer with ML prediction")
        print("1. Get status by Country")
        print("2. Get status by country and date")
        print("3. Difference between Latest state and previous one")
        print("4. Difference between Latest state and previous one by country")
        print("5. Get two weeks prediction by specific country")
        print("99. Exit")
        choice = int(input("Choice> "))

        if (choice==1):
            statusCountry(site)
        elif (choice==2):
            statusCountryDate(site)
        elif (choice==3):
            diff(site)
        elif (choice==4):
            diffCountry(site)
        elif (choice==5):
            predictionCountry(site)
        elif (choice==99):
            exit(0)
def main():
    # main method
    menu('https://covid19-api.org/api/status')

if __name__ == "__main__":
    # call main when this python file is not imported
    # to other python file
    main()