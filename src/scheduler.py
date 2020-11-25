import constant
from os import name, system, getcwd, popen

def init():
    scheduled = constant.SCHEDULED
    with open(scheduled, "w") as scheduled:
        scheduled.write(str(0))

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
        # cmd='@reboot '+ usrname + " cd " + pwd + ' && export DISPLAY=:0.0 && '
        cmd='@reboot sleep 300 '+ usrname + " cd " + constant.PWD + ' && export DISPLAY=:0.0 && '
        python3_path=check_output(['which', 'python3']).decode('utf-8')[:-1] 
        cmd=cmd+(python3_path+" "+schedule_script+" >> " + constant.LOG + " 2>&1 ") 
        with open(constant.BASH_SCRIPT, 'w') as script:
            script.write("sudo echo \""+cmd+"\n\" >> /etc/crontab" )
        system("sudo bash " + constant.BASH_SCRIPT)
    except Exception as err:
        print("Error: " + err)
        exit(1)

def scheduleWindows(schedule_script):
    # takes name of script to schedule on windows
    # schedule a ps on every boot
    cwd = getcwd()
    command = 'schtasks -create -delay 0010:00 -tn "CovidTracer" -tr "%s\schedulescript.pyw" -sc onstart -v1' % cwd 
    system(command)

def rmScheduleLinux(schedule_script):
    # remove from task scheduler linux
    from subprocess import check_output
    usrname=check_output('whoami').decode('utf-8')[:-1]
    # cmd='@reboot '+usrname+' export DISPLAY=:0.0 && '
    cmd='@reboot sleep 300 '+ usrname + " cd " + constant.PWD + ' && export DISPLAY=:0.0 && '
    python3_path=check_output(['which', 'python3']).decode('utf-8')[:-1] 
    cmd=cmd+(python3_path+" "+schedule_script+" >> " + constant.LOG + " 2>&1 ") 
    with open(constant.BASH_SCRIPT, 'w') as script:
        script.write("sudo grep -v \""+ cmd +"\" /etc/crontab > " + constant.TMP + " && sudo mv " + constant.TMP + " /etc/crontab")
    system("sudo bash " + constant.BASH_SCRIPT)
    system("sudo rm " + constant.SUBSCRIPTION)
    system("sudo rm " + constant.BASH_SCRIPT)
    system("sudo rm " + constant.SCHEDULED)
    system("sudo rm " + constant.LOG)
    exit(0)

def rmScheduleWindows(placeholder):
    # rm from task scheduler windows
    command = "schtasks -delete -tn CovidTracer -f"
    popen(command)
    pass

def isScheduled(scheduled):
    with open(scheduled, 'r') as scheduled:
        return int(scheduled.read())

def setScheduled(scheduled, data):
    with open(scheduled, 'w') as scheduled:
        scheduled.write(data)