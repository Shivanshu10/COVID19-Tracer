import code

def main():
    subcriptionData=code.checkSubscription()
    for data in subcriptionData:
        if (data['type']==1):
            resp=code.statusCountry(code.API, data['country'])
            descr="Number of Cases in " + data["country"].upper() + " on " + resp['last_update'] + " is " + str(resp['cases']) + ", number of deaths is "+ str(resp['deaths']) + " number of recoveries " + str(resp["recovered"]) + "."
        else:
            resp=code.diffCountry(code.API, data['country'])
            descr="Number of New Cases in " + data["country"].upper() + " on " + resp['last_update'] + " is " + str(resp['new_cases']) + ", number of new deaths is "+ str(resp['new_deaths']) + " number of new recoveries is " + str(resp["new_recovered"]) + "."
        code.notification("COVID19", descr, code.ICON_NAME)
        print("done")
main()