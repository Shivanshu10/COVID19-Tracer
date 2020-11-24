from pynotifier import Notification

notifyTitle="Test"
notifyDescription="test"

notice=Notification(title=notifyTitle, description=notifyDescription, duration=5, urgency=Notification.URGENCY_CRITICAL)
notice.send()
