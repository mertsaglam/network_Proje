"""
   ____ ____  _____ _  _    ___  _  _ _____ _  _   
  / ___/ ___|| ____| || |  / _ \| || |___  | || |  
 | |   \___ \|  _| | || |_| | | | || |_ / /| || |_ 
 | |___ ___) | |___|__   _| |_| |__   _/ / |__   _|
  \____|____/|_____|  |_| _\___/___|_|/_/_    |_|  
 |  _ \|  _ \ / _ \    | | ____/ ___|_   _|        
 | |_) | |_) | | | |_  | |  _|| |     | |          
 |  __/|  _ <| |_| | |_| | |__| |___  | |          
 |_|   |_| \_\\___/ \___/|_____\____| |_|          
                                                   

Group Members:
ONURCAN ISLER 150120825
MERT SAGLAM 150119508
"""
import json

# In this Utils class we basically perform business functions.
# We seperated these functions to improve readability of the code.
# All these functions are static and does not have any state.

class ScheduleUtils:
    @staticmethod
    def initializeSchedulesFile():
        # We keep schedules of the rooms in JSON format.
        # It is easy to work with.
        # This function basically initializes that JSON file.
        emptydict = {}
        with open('roomschedules.json', 'w') as json_file:
            json.dump(emptydict, json_file)

    @staticmethod
    def createNewRoom(roomName):
        # To create a new room assign new schedule to it.
        ScheduleUtils.updateSchedule(roomName,ScheduleUtils.getNewSchedule())

    @staticmethod
    def getNewSchedule():
        n = 7
        m = 24
        newschedule = [["empty"] * m for i in range(n)]
        # Each row means hours. Each column means day.
        # So, we have mxn dimensional string matrix for schedules.
        # If schedule is empty at some hour, then it represented as "empty".
        return newschedule

    @staticmethod
    def checkIfScheduleAvailable(roomName,day,hour,duration):
        # This functions has some tricky algorithm.
        # We first start iterating over specified day and hour.
        # While we are iterating, we count the number of empty slots.
        # If the count is smaller than the duration than we dont have enough space for
        # this spacial activity. So, we return False in this case.
        schedule = ScheduleUtils.getSchedule(roomName)
        day = day - 1
        hour = hour - 1
        counthours = 0
        starttimer = 0
        for days in range(7):
            for hours in range(24):
                if days==day and hours==hour:
                    starttimer = 1 # Start counting empty slots after (day,hour)
                if starttimer:
                    counthours = counthours + 1 # Count empty slot.
                    if schedule[days][hours]!="empty":
                        return counthours > duration
        return True

    @staticmethod
    def updateSchedule(newRoomName,schedule):
        # Get the room schedules.
        f = open('roomschedules.json')
        roomsdict = json.load(f)
        f.close()
        # Insert a new schedule.
        roomsdict[newRoomName] = schedule
        # Write the new room schedules back. Thats it, update is done!
        with open('roomschedules.json', 'w') as json_file:
            json.dump(roomsdict, json_file)

    @staticmethod
    def fillSchedule(roomName,activityName,day,hour,duration):
        # The idea almost same as checkIfAvailableSchedule() function.
        # But this time we are filling these slots.
        # Fill total of duration cells with specified activity.
        schedule = ScheduleUtils.getSchedule(roomName)
        day = day - 1
        hour = hour - 1
        newschedule = schedule.copy()
        starttimer = 0
        counthours = 0
        for days in range(7):
            for hours in range(24):
                if days==day and hours==hour:
                    starttimer = 1
                if starttimer:
                    newschedule[days][hours] = activityName # Fill the slot.
                    counthours = counthours + 1
                    if counthours == duration:
                        ScheduleUtils.updateSchedule(roomName,newschedule)
                        return
        ScheduleUtils.updateSchedule(roomName,newschedule)

    @staticmethod
    def getSchedule(roomName):
        # Read the roomschedules.json file and return the schedule of a specific room.
        f = open('roomschedules.json')
        roomsdict = json.load(f)
        f.close()
        if roomsdict.get(roomName)==None:
            ScheduleUtils.createNewRoom(roomName)
            return ScheduleUtils.getSchedule(roomName)
        return roomsdict[roomName]

    @staticmethod
    def removeRoom(roomName):
        # Remove a specific room from roomschedules.json.
        # Probably remove in Room Server is called.
        f = open('roomschedules.json')
        roomsdict = json.load(f)
        f.close()
        del roomsdict[roomName]
        with open('roomschedules.json', 'w') as json_file:
            json.dump(roomsdict, json_file)

    @staticmethod
    def isValidDay(daystring):
        # First of all passed day string must contain all digits.
        # Second it must be >=1 and <=7 since we have 7 weekdays.
        # If any of these checks fails, return False.
        if daystring.isnumeric()==False:
            return False
        day = int(daystring)
        return day>=1 and day<=7

    @staticmethod
    def isValidHour(hourstring):
        # First check if hour string is all digits.
        # Also, working hours starts from 9 to 17.
        # So, make sure specified hour is >=9 and <=17
        if hourstring.isnumeric()==False:
            return False
        hour = int(hourstring)
        return hour>=9 and hour<=17

    @staticmethod
    def isValidRoom(roomName):
        # Room name is a string.
        # We have to make sure there is no room with that same name.
        f = open('roomschedules.json')
        roomsdict = json.load(f)
        f.close()
        if roomsdict.get(roomName)==None:
            return False
        return True

    @staticmethod
    def isValidActivity(activityName):
        # We have to make sure there is no activity with that same name.
        with open("activities.txt", "r") as f:
            if activityName + "\n" in f.read():
                return True
            else:
                return False
        
    @staticmethod
    def isValidReservationId(idstring):
        # Registration IDs are integers.
        # Also we create these IDs by counting pre-existing reservations.
        # So, each reservation would have +1 ID of the previous schedule.
        # In this case ID of a reservation can not be greater than the number of reservations.
        if idstring.isnumeric()==False:
            return False
        id = int(idstring)
        if id <= 0: # ID cannot be negative.
            return False
        with open('reservations.txt', 'r') as file:
            lines = []
            for line in file:
                line = line.strip()
                lines.append(line)
            
            if len(lines)<id: # ID can not be greater than the number of reservations.
                return False
            else:
                return True
    
    @staticmethod
    def getReservationDetails(idstring):
        # We know the passed IDString is valid.
        # We can easily print out the details then.
        id = int(idstring)
        with open('reservations.txt', 'r') as file:
            lines = []
            for line in file:
                line = line.strip()
                lines.append(line)
            
            reservation = lines[id-1]
            #19 M1Z103 Webinar 1 9 1
            roomName = reservation.split(' ')[1]
            activityName = reservation.split(' ')[2]
            day = reservation.split(' ')[3]
            hour = reservation.split(' ')[4]
            duration = reservation.split(' ')[5]
            # Return the details of the specific reservation.
            return "<h1>The reservation, " + idstring + \
                    ", is on " + \
                    ScheduleUtils.getDayName(int(day)) + \
                    " at " + hour + " oclock, and will last " + duration + " hours. " + \
                    activityName + " will be held in " + roomName + ". [200 OK]</h1>\r\n"
    
    @staticmethod
    def isValidDuration(durationstring):
        # We have to make sure passed duration is also valid.
        # It must be a numeric, with all digits.
        # Working hours between 9 to 17, so duration can not be greater than 9.
        # Duration must also be a positive integer.
        if durationstring.isnumeric()==False:
            return False
        duration = int(durationstring)
        return duration>=1 and duration<=9

    @staticmethod
    def getAvailableHours(roomName,day):
        # We get available hours in a specific day.
        # The reason why we are decrementing day by one is that arrays are zero indexed.
        day = day - 1
        schedule = ScheduleUtils.getSchedule(roomName)
        availableHours = []
        for hour in range(9,18):
            if schedule[day][hour-1]=="empty":
                availableHours.append(hour)
                # If the current hour in 'day' is empty, then insert it.
        result = "[ "
        for hour in availableHours:
            result = result + str(hour) + " "
        result = result + "]"
        # Return the result.
        return result

    @staticmethod
    def getDayName(day):
        # Convert day number to word.
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        return days[day-1]

