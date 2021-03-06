from os import system, name
# Used detect Operating System, getcwd and execute shell cmd
from pycountry import countries
import subscription
import apiParser
import userInput
import tracer
import ctypes, sys

def countrytoCode(country):
    # convert country to country code
    try:
        country_code = countries.search_fuzzy(country)[0].alpha_2
    except LookupError:
        print("Couldn't find country try different one")
        return countrytoCode(userInput.read('Country'))
    return(country_code)

def is_admin():
    # Check for windows if admin access is available
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def clear():
    # Clear terminal showing previous outputs
    system('cls' if name == 'nt' else 'clear')

def createMenu(site, schedule_script, scheduled):
    # pass site url as parameter
    # get what user wants to do
    # and call corresponding function
    while (True):
        clear()
        print("COVID19 Tracer with ML prediction")
        print("1. Get status by Country")
        print("2. Get status by country and date")
        print("3. Difference between Latest state and previous one by country")
        print("4. Get two weeks prediction by specific country")
        print("5. Get timeline of cases by Country")
        print("6. Subscribe")
        print("7. Remove Subscription")
        print("99. Exit")
        choice = userInput.getChoice()
        if (choice==1):
            country=countrytoCode(userInput.read('Country'))
            apiParser.parse(tracer.statusCountry(country))
        elif (choice==2):
            country=countrytoCode(userInput.read('Country'))
            date=userInput.read('Date (YYYY-MM-DD)')
            apiParser.parse(tracer.statusCountryDate(country, date))
        elif (choice==3):
            country=countrytoCode(userInput.read('Country'))
            apiParser.parse(tracer.diffCountry(country))
        elif (choice==4):
            country=countrytoCode(userInput.read('Country'))
            apiParser.listParse(tracer.predictionCountry(country))
        elif (choice==5):
            country=countrytoCode(userInput.read('Country'))
            apiParser.listParse(tracer.timeCases(country))
        elif (choice==6):
            if (is_admin() or name != 'nt'):
                # Code of your program here
                subscription.subscribe(schedule_script, scheduled)
            else:
                # Re-run the program with admin rights
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        elif (choice == 7):
            if (is_admin() or name != 'nt'):
                subscription.rmSubscribe(schedule_script, scheduled)
            else:
                # Re-run the program with admin rights
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        elif (choice==99):
            exit(0)
        else:
            print("Not a valid input")
