import subscription
import tracer
import constant
import notification

def main():
    constant.init()
    subcriptionData=subscription.checkSubscription()
    for data in subcriptionData:
        try:
            if (data['type']==1):
                resp=tracer.statusCountry(data['country'])
                descr="Number of Cases in " + data["country"].upper() + " on " + resp['last_update'] + " is " + str(resp['cases']) + ", number of DEATHS is "+ str(resp['deaths']) + " number of RECOVERY " + str(resp["recovered"]) + "."
            else:
                resp=tracer.diffCountry(data['country'])
                descr="Number of New Cases in " + data["country"].upper() + " on " + resp['last_update'] + " is " + str(resp['new_cases']) + ", number of new DEATHS is "+ str(resp['new_deaths']) + " number of new RECOVERY is " + str(resp["new_recovered"]) + "."
            notification.createNotification("COVID19", descr, constant.ICON_NAME)
        except:
            continue
main()
