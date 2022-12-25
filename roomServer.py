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

import socket
import threading
from scheduleUtils import ScheduleUtils

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 8081  # Port to listen on (non-privileged ports are > 1023)



#################################################
#                                               #
#              SERVING FUNCTION                 #
# (The code running this funcion is at the end) #
#                                               #
#################################################

def serveRequest(conn):
    with conn:
        data = conn.recv(1024)
        utfdata = data.decode("utf-8")
        method = utfdata.split(" ")[0]
        url = utfdata.split(" ")[1]
        funcType = url.split("?")[0]
        

        if method!="GET" and method!="POST":
            print("[INFO]: " +"The requested query contains methods that are not yet implemented in the server.\n")
            response = 'HTTP/1.1 501 Not Implemented\r\n' + \
                        'Content-Type: text/html\r\n\r\n' + \
                        '<h1>The requested query contains methods that are not yet implemented in the server. [501 Not Implemented]</h1>\r\n'
            conn.sendall(response.encode())
            return




        
        if funcType == "/add": # WORKING FINE.
            # /add?name=M1Z103
            query_string = url.split('?')[1]
            qparams  = dict(param.split('=') for param in query_string.split('&'))

            if qparams.get("name")==None:
                print("[INFO]: " + "The query parameters are missing or invalid.\n")
                response = 'HTTP/1.1 400 Bad Request\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The queries are missing or invalid. [400 Bad Request]</h1>\r\n'
                conn.sendall(response.encode())
                return

            roomName = qparams["name"]
            
            f = open("rooms.txt", "r")
            if roomName in f.read():
                print("[INFO]: " + "Room already exists")
                response = 'HTTP/1.1 403 Forbidden\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>Room with the name '+ roomName + ' already exists. [403 Forbidden]</h1>\r\n'
                conn.sendall(response.encode())
                return
            else:
                f = open("rooms.txt", "a")
                f.write(roomName+"\n")
                f.close()

                # CREATE A NEW ROOM WITH EMPTY SCHEDULE.
                ScheduleUtils.createNewRoom(roomName)                    

                print("[INFO]: " + roomName + " is added to the rooms.txt file")
                response = 'HTTP/1.1 200 OK\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>Room with the name '+ roomName + ' is successfully added. [200 OK]</h1>\r\n'
                conn.sendall(response.encode())










        elif funcType == "/remove": # WORKING FINE.
            query_string = url.split('?')[1]
            qparams  = dict(param.split('=') for param in query_string.split('&'))

            if qparams.get("name")==None:
                print("[INFO]: " +"The query parameters are missing or invalid.\n")
                response = 'HTTP/1.1 400 Bad Request\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The queries are missing or invalid. [400 Bad Request]</h1>\r\n'
                conn.sendall(response.encode())
                return
                
            roomName = qparams["name"]
            # open the rooms.txt file to check if the room is already added
            # if it is added remove it
            f = open("rooms.txt", "r")
            if roomName in f.read():
                f = open("rooms.txt", "r")
                lines = f.readlines()
                f.close()
                f = open("rooms.txt", "w")
                for line in lines:
                    if line.strip("\n") != roomName:
                        f.write(line)
                    else:
                        continue
                f.close()

                # REMOVE THE ROOM ALONG WITH ITS ACTIVITIES...
                ScheduleUtils.removeRoom(roomName)

                print("[INFO]: The room," + roomName + " is successfully removed")
                response = 'HTTP/1.1 200 OK\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>Room with the name '+ roomName + ' is successfully removed. [200 OK]</h1>\r\n'
                conn.sendall(response.encode())
            else:
                print("[INFO]: No room with that name.")
                response = 'HTTP/1.1 403 Forbidden\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>Room with the name '+ roomName + ' does not exist. [403 Forbidden]</h1>\r\n'
                conn.sendall(response.encode())








        elif funcType == "/reserve": # WORKING FINE.
            # /reserve?room=roomname&activity=activityname&day=x&hour=y&duration=z
            query_string = url.split('?')[1]
            qparams  = dict(param.split('=') for param in query_string.split('&'))
            #print(qparams)

            if qparams.get("room")==None or qparams.get("activity")==None or qparams.get("day")==None or qparams.get("hour")==None or qparams.get("duration")==None:
                print("[INFO]: " + "The queries are missing or invalid.\n") 
                response = 'HTTP/1.1 400 Bad Request\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The queries are missing or invalid. [400 Bad Request]</h1>\r\n'
                conn.sendall(response.encode())
                return
            
            roomName = qparams["room"]
            activityName = qparams["activity"]
            day = qparams["day"]
            hour = qparams["hour"]
            duration = qparams["duration"]

            #print("Room Server - Room: " + roomName)
            #print("Room Server - Activity: " + activityName)
            #print("Room Server - Day: " + day)
            #print("Room Server - Hour: " + hour)
            #print("Room Server - Duration: " + duration)


            if ScheduleUtils.isValidActivity(activityName)==False or ScheduleUtils.isValidDay(day)==False or ScheduleUtils.isValidHour(hour)==False or ScheduleUtils.isValidRoom(roomName)==False or ScheduleUtils.isValidDuration(duration)==False:
                print("[INFO]: " +"The queries are missing or invalid.\n") 
                response = 'HTTP/1.1 400 Bad Request\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The queries are missing or invalid. [400 Bad Request]</h1>\r\n'
                conn.sendall(response.encode())
                return
            
            day = int(day)
            hour = int(hour)
            duration = int(duration)

            if ScheduleUtils.checkIfScheduleAvailable(roomName,day,hour,duration)==False:
                print("[INFO]: " +"The room is already reserved during these day and hours.\n") 
                response = 'HTTP/1.1 403 Forbidden\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The room is already reserved during that day and hours. [403 Forbidden]</h1>\r\n'
                conn.sendall(response.encode())
                return
            
            # 1 M2Z06 Webinar 1 1 3
            # reservation id, room name, activity name, day, hour, duration
            f = open("reservations.txt", "r")
            generatedid = len(f.readlines()) + 1
            f.close()
            f = open("reservations.txt", "a")
            f.write(str(generatedid)+" "+roomName+" "+activityName+" "+str(day)+" "+str(hour)+" "+str(duration)+"\n")
            f.close()
            #print("Generated ID is:" + str(generatedid))
            
            
            ScheduleUtils.fillSchedule(roomName,activityName,day,hour,duration)
            
            print("[INFO]: The room is successfully reserved during that day and hours.")
            response = 'HTTP/1.1 200 OK\r\n' + \
                        'Content-Type: text/html\r\n\r\n' + \
                        '<h1>The room is successfully reserved during that day and hours. Reservation ID:'+str(generatedid)+'. [200 OK]</h1>\r\n'
            conn.sendall(response.encode())
            






        elif funcType == "/checkavailability": # WORKING FINE.
            #/checkavailability?name=roomname&day=x
            query_string = url.split('?')[1]
            qparams  = dict(param.split('=') for param in query_string.split('&'))
            if qparams.get("name")==None or qparams.get("day")==None:
                print("[INFO]: " +"The queries are missing or invalid.\n")
                response = 'HTTP/1.1 400 Bad Request\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The queries are missing or invalid. [400 Bad Request]</h1>\r\n'
                conn.sendall(response.encode())
                return

            roomName = qparams["name"]
            day = qparams["day"]

            if ScheduleUtils.isValidDay(day)==False:
                print("[INFO]: " +"The queries are missing or invalid.\n") 
                response = 'HTTP/1.1 400 Bad Request\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The queries are missing or invalid. [400 Bad Request]</h1>\r\n'
                conn.sendall(response.encode())
                return
            
            if ScheduleUtils.isValidRoom(roomName)==False:
                print("[INFO]: " +"The requested room is not found.\n") 
                response = 'HTTP/1.1 404 Not Found\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The requested room is not found. [404 Not Found]</h1>\r\n'
                conn.sendall(response.encode())
                return
            
            day = int(day)
            availableHours = ScheduleUtils.getAvailableHours(roomName,day)
            response = 'HTTP/1.1 200 OK\r\n' + \
                        'Content-Type: text/html\r\n\r\n' + \
                        '<h1>The room, ' + roomName + ', is available in hours:'+ availableHours +' during that day. [200 OK]</h1>\r\n'
            conn.sendall(response.encode())


        else: # WORKING FINE.
            print("[INFO]: " +"Requested URL is not found in Room Server.")
            response = 'HTTP/1.1 404 Not Found\r\n' + \
                        'Content-Type: text/html\r\n\r\n' + \
                        '<h1>The requested URL is not found in Room Server. [404 Not Found]</h1>\r\n'
            conn.sendall(response.encode())
        if not data:
            return







#################################################
#                                               #
#                 RUNNER CODE                   #
#                                               #
#################################################
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[INFO]: Room Server is started to listening to the address, " + socket.gethostbyname(HOST) + ":" + str(PORT))
    while True:
        conn, addr = s.accept()
        threading.Thread(target=serveRequest, args=(conn,)).start()
        print("[INFO]: The number of active connections in Room Server at the moment: "+str(threading.active_count()-1))


    
                
            

                