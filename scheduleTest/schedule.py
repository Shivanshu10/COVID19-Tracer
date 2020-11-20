import datetime
import win32com.client

scheduler = win32com.client.Dispatch('Schedule.Service')
scheduler.Connect()
root_folder = scheduler.GetFolder('\\')
task_def = scheduler.NewTask(0)

# For Daily Trigger set this variable to 2 ; for One time run set this value as 1
TASK_TRIGGER_DAILY = 2
trigger = task_def.Triggers.Create(TASK_TRIGGER_DAILY)

#Repeat for a duration of number of day
num_of_days = 10
trigger.Repetition.Duration = "P"+str(num_of_days)+"D"

#use PT2M for every 2 minutes, use PT1H for every 1 hour
trigger.Repetition.Interval = "PT2M"
trigger.StartBoundary = start_time.isoformat()

# Create action
TASK_ACTION_EXEC = 0
action = task_def.Actions.Create(TASK_ACTION_EXEC)
action.ID = 'TRIGGER BATCH'
action.Path = 'cmd.exe'
action.Arguments ='/c start "" "D:\\Projects\\Python\\Notification Test\\dist\\notification.exe"'

# Set parameters
task_def.RegistrationInfo.Description = 'COVID19-Tracer Info Notification'
task_def.Settings.Enabled = True
task_def.Settings.StopIfGoingOnBatteries = False

# Register task
# If task already exists, it will be updated
TASK_CREATE_OR_UPDATE = 6
TASK_LOGON_NONE = 0
root_folder.RegisterTaskDefinition(
    'COVID19-Tracer Info Notification',  # Task name
    task_def,
    TASK_CREATE_OR_UPDATE,
    '',  # No user
    '',  # No password
    TASK_LOGON_NONE
)