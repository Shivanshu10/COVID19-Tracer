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
                descr=data["country"].upper() + "\nCases : " + str(resp['cases']) + "\nDEATHS : "+ str(resp['deaths']) + "\nRECOVERY : " + str(resp["recovered"])
            else:
                resp=tracer.diffCountry(data['country'])
                descr=data["country"].upper()+"\nNew Cases : "  + str(resp['new_cases']) + "\nNew DEATHS : "+ str(resp['new_deaths']) + "\nNew RECOVERY : " + str(resp["new_recovered"])
            notification.createNotification("COVID19", descr, constant.ICON_NAME)
        except:
            continue
main()
