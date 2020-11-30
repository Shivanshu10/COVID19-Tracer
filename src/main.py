import menu
import constant
import scheduler

def main():
    menu.clear()
    constant.init()
    scheduler.init()
    
    menu.createMenu(constant.API, constant.SCHEDULE_SCRIPT, constant.SCHEDULED)

if __name__=="__main__":
    main()
