import socket
from scheduleUtils import ScheduleUtils
HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 8081  # Port to listen on (non-privileged ports are > 1023)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            # print(f"Connected by {addr}")
            data = conn.recv(1024)
            #get the URL
            url = data.decode("utf-8").split(" ")[1]
            # print(url)
            funcType = url.split("?")[0]
            # print(funcType)
            #check for the function type if it is add
            if funcType == "/add":
                query_string = url.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))

                if qparams.get("name")==None:
                    print("The query parameters are missing or invalid.\n")
                    conn.sendall(b"HTTP/1.1 400 Bad Request\n"+b"Content-Type: text/html\n"+b"\n")

                roomName = qparams["name"]
                #open the rooms.txt file to check if the room is already added
                f = open("rooms.txt", "r")
                if roomName in f.read():
                    print("Room already exists")
                    conn.sendall(b"HTTP/1.1 403 Forbidden\n"+b"Content-Type: text/html\n"+b"\n")
                else:
                    f = open("rooms.txt", "a")
                    f.write(roomName+"\n")
                    f.close()

                    # CREATE A NEW ROOM WITH EMPTY SCHEDULE.
                    ScheduleUtils.createNewRoom(roomName)                    

                    print(roomName + "added to the rooms.txt file")
                    conn.sendall(b"HTTP/1.1 200 OK\n"+b"Content-Type: text/html\n"+b"\n")
            #check for the function type if it is remove
            elif funcType == "/remove":
                query_string = url.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))

                if qparams.get("name")==None:
                    print("The query parameters are missing or invalid.\n")
                    conn.sendall(b"HTTP/1.1 400 Bad Request\n"+b"Content-Type: text/html\n"+b"\n")
                    
                roomName = qparams["name"]
                #open the rooms.txt file to check if the room is already added
                #if it is added remove it
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

                    print(roomName + "removed from the rooms.txt file")
                    conn.sendall(b"HTTP/1.1 200 OK\n"+b"Content-Type: text/html\n"+b"\n")
                else:
                    print("No room with that name.")
                    conn.sendall(b"HTTP/1.1 403 Forbidden\n"+b"Content-Type: text/html\n"+b"\n")


            elif funcType == "/reserve":
                #/reserve?room=roomname&activity=activityname&day=x&hour=y&duration=z
                query_string = url.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))
                print(qparams)

                if qparams.get("room")==None or qparams.get("activity")==None or qparams.get("day")==None or qparams.get("hour")==None or qparams.get("duration")==None:
                    print("The queries are missing or invalid.\n") 
                    conn.sendall(b"HTTP/1.1 400 Bad Request\n"+b"Content-Type: text/html\n"+b"\n")
                    continue
                
                roomName = qparams["room"]
                activityName = qparams["activity"]
                day = qparams["day"]
                hour = qparams["hour"]
                duration = qparams["activity"]

                print("Room Server - Room: " + roomName)
                print("Room Server - Activity: " + activityName)
                print("Room Server - Day: " + day)
                print("Room Server - Hour: " + hour)
                print("Room Server - Duration: " + duration)


                if ScheduleUtils.isValidDay(day)==False or ScheduleUtils.isValidHour(hour)==False:
                    print("The queries are missing or invalid.\n") 
                    conn.sendall(b"HTTP/1.1 400 Bad Request\n"+b"Content-Type: text/html\n"+b"\n")
                    continue
                
                # 1 M2Z06 Webinar 1 1 3
                # reservation id, room name, activity name, day, hour, duration
                f = open("reservations.txt", "r")
                generatedid = len(f.readlines()) + 1
                f.close()
                f = open("reservations.txt", "a")
                f.write(str(generatedid)+" "+roomName+" "+activityName+" "+day+" "+hour+" "+duration+"\n")
                f.close()
                #print("Generated ID is:" + str(generatedid))
                
                #ScheduleUtils.fillSchedule(roomName,activityName,day,hour,duration)
                
                conn.sendall(b"HTTP/1.1 200 OK\n"+b"Content-Type: text/html\n"+b"\n")
               
            elif funcType == "/checkavailability":
                #/checkavailability?name=roomname&day=x
                query_string = url.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))
                if qparams.get("name")==None or qparams.get("day")==None:
                    print("The queries are missing or invalid.\n")
                    conn.sendall(b"HTTP/1.1 400 Bad Request\n"+b"Content-Type: text/html\n"+b"\n")

                roomName = qparams["name"]
                day = qparams["day"]

                if ScheduleUtils.isValidDay(day)==False:
                    print("The queries are missing or invalid.\n") 
                    conn.sendall(b"HTTP/1.1 400 Bad Request\n"+b"Content-Type: text/html\n"+b"\n")
                    continue
                


                
            else:
                print("Requested URL is not found in Room Server.")
                conn.sendall(b"HTTP/1.1 404 Not Found\n"+b"Content-Type: text/html\n"+b"\n")
                
    #         conn.sendall(b"HTTP/1.1 200 OK\n"
    #  +b"Content-Type: text/html\n"
    #  +b"\n" # Important!
    #  +b"<html><body>Hello World<p>naber</p></body></html>\n")
            if not data:
                break
            #send 200 OK
    
                
            

                