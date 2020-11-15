# TODO
# Get choice of user
# request the API server as per choice
# show data to user
# Find what is webhook

# Later
# GUI
# pyaudio
# windows notification

# docs of api
# https://documenter.getpostman.com/view/10877427/SzYW2f8n?version=latest
from requests import get
# make a get request
from json import loads
# convert json string to python dicitionory

def menu():
    print("COVID19 Tracer with ML prediction")
    print("1. Get status for all countries")
    print("2. Get status by date")
    print("3. Get status by Country")
    print("4. Get status by country and date")
    print("5. Difference between Latest state and previous one")
    print("6. Difference between Latest state and previous one by country")
    print("7. Get two weeks prediction by specific country")
site='https://covid19-api.org/api/status'
response=get(site)
print(response.content)