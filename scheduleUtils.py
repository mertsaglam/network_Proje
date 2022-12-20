import json

class ScheduleUtils:
    @staticmethod
    def initializeSchedulesFile():
        emptydict = {}
        with open('roomschedules.json', 'w') as json_file:
            json.dump(emptydict, json_file)

    @staticmethod
    def createNewRoom(roomName):
        ScheduleUtils.updateSchedule(roomName,ScheduleUtils.getNewSchedule())

    @staticmethod
    def getNewSchedule():
        n = 7
        m = 24
        newschedule = [["empty"] * m for i in range(n)]
        return newschedule

    @staticmethod
    def checkIfScheduleAvailable(roomName,day,hour,duration):
        schedule = ScheduleUtils.getSchedule(roomName)
        day = day - 1
        hour = hour - 1
        counthours = 0
        starttimer = 0
        for days in range(7):
            for hours in range(24):
                if days==day and hours==hour:
                    starttimer = 1
                if starttimer:
                    counthours = counthours + 1
                    if schedule[days][hours]!="empty":
                        return counthours > duration
        return True

    @staticmethod
    def updateSchedule(newRoomName,schedule):
        # Get the room schedules
        f = open('roomschedules.json')
        roomsdict = json.load(f)
        f.close()
        # Insert a new schedule.
        roomsdict[newRoomName] = schedule
        # Write the new room schedules.
        with open('roomschedules.json', 'w') as json_file:
            json.dump(roomsdict, json_file)

    @staticmethod
    def fillSchedule(roomName,activityName,day,hour,duration):
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
                    newschedule[days][hours] = activityName
                    counthours = counthours + 1
                    if counthours == duration:
                        ScheduleUtils.updateSchedule(roomName,newschedule)
                        return
        ScheduleUtils.updateSchedule(roomName,newschedule)

    @staticmethod
    def getSchedule(roomName):
        f = open('roomschedules.json')
        roomsdict = json.load(f)
        f.close()
        if roomsdict.get(roomName)==None:
            ScheduleUtils.createNewRoom(roomName)
            return ScheduleUtils.getSchedule(roomName)
        return roomsdict[roomName]

    @staticmethod
    def removeRoom(roomName):
        f = open('roomschedules.json')
        roomsdict = json.load(f)
        f.close()
        del roomsdict[roomName]
        with open('roomschedules.json', 'w') as json_file:
            json.dump(roomsdict, json_file)

    @staticmethod
    def isValidDay(daystring):
        if daystring.isnumeric()==False:
            return False
        day = int(daystring)
        return day>=1 and day<=7

    @staticmethod
    def isValidHour(hourstring):
        if hourstring.isnumeric()==False:
            return False
        hour = int(hourstring)
        return hour>=9 and hour<=17

    @staticmethod
    def getAvailableHours(roomName,day):
        schedule = ScheduleUtils.getSchedule(roomName)
        availableHours = []
        for hour in range(9,18):
            if schedule[day][hour]=="empty":
                availableHours.append(hour)
        return availableHours

