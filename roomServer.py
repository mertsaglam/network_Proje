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
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            #get the URL
            url = data.decode("utf-8").split(" ")[1]
            print(url)
            funcType = url.split("?")[0]
            print(funcType)
            #check for the function type if it is add
            if funcType == "/add":
                query_string = url.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))

                if qparams.get("name")==None:
                    print("The query parameters are missing or invalid.\n")
                    conn.sendall(b"HTTP/1.1 400 Bad Request \n")

                roomName = qparams["name"]
                #open the rooms.txt file to check if the room is already added
                f = open("rooms.txt", "r")
                if roomName in f.read():
                    print("Room already exists")
                    conn.sendall(b"HTTP/1.1 433 Forbidden \n")
                else:
                    f = open("rooms.txt", "a")
                    f.write(roomName+"\n")
                    f.close()

                    # CREATE A NEW ROOM WITH EMPTY SCHEDULE.
                    ScheduleUtils.createNewRoom(roomName)                    

                    print(roomName + "added to the rooms.txt file")
                    conn.sendall(b"HTTP/1.1 200 OK\n"
                    +b"Content-Type: text/html\n"
                    +b"\n" # Important!
                    +b""+roomName.encode("utf-8")+b" added to the rooms.txt file\n")
            #check for the function type if it is remove
            elif funcType == "/remove":
                query_string = url.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))

                if qparams.get("name")==None:
                    print("The query parameters are missing or invalid.\n")
                    conn.sendall(b"HTTP/1.1 400 Bad Request \n")
                    
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
                    conn.sendall(b"HTTP/1.1 200 OK\n"
                    +b"Content-Type: text/html\n"
                    +b"\n" # Important!
                    +b""+roomName.encode("utf-8")+b" removed from the rooms.txt file\n")
                else:
                    print("No room with that name.")
                    conn.sendall(b"HTTP/1.1 403 Forbidden \n")


            elif funcType == "/reserve":
                #/reserve?name=roomname&day=x&hour=y&duration=z:
                query_string = url.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))

                if qparams.get("name")==None or qparams.get("day")==None or qparams.get("hour") or qparams.get("duration")==None:
                    print("The queries are missing or invalid.\n")
                    conn.sendall(b"HTTP/1.1 400 Bad Request \n")

                roomName = qparams["name"]
                day = qparams["day"]
                hour = qparams["hour"]
                duration = qparams["activity"]

                #print(roomName + " is the room name to be reserved")
                #print(day + " is the day to be reserved")
                #print(hour + " is the hour to be reserved")
                #print(duration + " is the duration to be reserved")

                #ScheduleUtils.fillSchedule(roomName,activity)

                conn.sendall(b"HTTP/1.1 200 OK\n"
                +b"Content-Type: text/html\n"
                +b"\n" # Important!
                +b""+roomName.encode("utf-8")+b" is the room name to be reserved\n")
               
            elif funcType == "/checkavailability":
                #/checkavailability?name=roomname&day=x
                query_string = url.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))
                if qparams.get("name")==None or qparams.get("day")==None:
                    print("The queries are missing or invalid.\n")
                    conn.sendall(b"HTTP/1.1 400 Bad Request \n")
                    
                roomName = qparams["name"]
                day = qparams["day"]
                
                if ScheduleUtils.isValidDay(day)==False:
                    print("Day input is not valid. \n")
                    conn.sendall(b"HTTP/1.1 400 Bad Request \n")

                f = open("rooms.txt", "r")
                if roomName in f.read():
                    availableHours = ScheduleUtils.getAvailableHours(roomName,day)
                    # TO DO: PUT AVALIABLE HOURS INSIDE OF THE RESPONSE BODY AND RETURN BACK.
                else:
                    print("No room with that name.")
                    conn.sendall(b"HTTP/1.1 404 Not Found \n")
                
            else:
                print("Requested URL is not found in Room Server.")
                conn.sendall(b"HTTP/1.1 404 Not Found \n")
                
    #         conn.sendall(b"HTTP/1.1 200 OK\n"
    #  +b"Content-Type: text/html\n"
    #  +b"\n" # Important!
    #  +b"<html><body>Hello World<p>naber</p></body></html>\n")
            if not data:
                break
            #send 200 OK
    
                
            

                