from requests import get
# make a get request
from json import loads
# convert json string to python dicitionory
from sys import exit
# exit program with an exit code
from pycountry import countries
# convert country to country code
import os


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
    os.system('cls' if os.name == 'nt' else 'clear')

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

def menu(site):
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
        elif (choice==99):
            exit(0)
        else:
            print("Not a valid input")
def main():
    # main method
    clear()
    menu('https://covid19-api.org/api')

if __name__ == "__main__":
    # call main when this python file is not imported
    # to other python file
    main()
