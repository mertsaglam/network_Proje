import subprocess
from scheduleUtils import ScheduleUtils

ScheduleUtils.initializeSchedulesFile()
subprocess.Popen(["python3", "activityServer.py"])
subprocess.Popen(["python3", "reservationServer.py"])
subprocess.Popen(["python3", "roomServer.py"])
