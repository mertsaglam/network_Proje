import socket
from scheduleUtils import ScheduleUtils

HOST = "localhost"
PORT = 8080
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            data = conn.recv(1024)
            urlstring = data.decode("utf-8")
            #print(data)
            #print("URL:" + urlstring)
            urlstring = urlstring.split("/")[1].split(" ")[0]
            print(urlstring + " requested\n")
            funcType = urlstring.split("?")[0]





            if funcType == "reserve":
                #/reserve?room=roomname&activity=activityname&day=x&hour=y&duration=z
                query_string = urlstring.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))
                # print(qparams)

                if qparams.get("room")==None or qparams.get("activity")==None or qparams.get("day")==None or qparams.get("hour")==None or qparams.get("duration")==None:
                    print("The queries are missing or invalid.\n") 
                    conn.sendall(b"HTTP/1.1 400 Bad Request\n"+b"Content-Type: text/html\n"+b"\n")
                    continue

                roomName = qparams["room"]
                activityName = qparams["activity"]
                day = qparams["day"]
                hour = qparams["hour"]
                duration = qparams["activity"]
                print("Reservation Server - Room: " + roomName)
                print("Reservation Server - Activity: " + activityName)
                print("Reservation Server - Day: " + day)
                print("Reservation Server - Hour: " + hour)
                print("Reservation Server - Duration: " + duration)

                
                if ScheduleUtils.isValidDay(day)==False or ScheduleUtils.isValidHour(hour)==False:
                    print("The queries are missing or invalid.\n") 
                    conn.sendall(b"HTTP/1.1 400 Bad Request \n")
                    continue

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
                    a.connect((HOST,8081))
                    headers = "GET " + f"/reserve?room={roomName}&activity={activityName}&day={day}&hour={hour}&duration={duration}" + " HTTP/1.1\r\n" + "Host: localhost:8081\r\n" + "Accept: text/html\r\n\rn"
                    a.sendall(headers.encode('utf-8'))
                    response = a.recv(1024).decode("utf-8")
                    response = response.split(" ")[1]
                    if response == 200:
                        print("Reservation is completed.")
                    else:
                        print("Reservation is failed.")
                
                conn.sendall(b"HTTP/1.1 200 OK\n"+b"Content-Type: text/html\n"+b"\n")






            elif funcType=="listavailability":
                query_string = urlstring.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))
                print(qparams)

                if qparams.get("room")==None:
                    print("The queries are missing or invalid.\n")
                    conn.sendall(b"HTTP/1.1 400 Bad Request\n"+b"Content-Type: text/html\n"+b"\n")
                
                roomName = qparams["room"]
                #...






            elif funcType=="display":
                query_string = urlstring.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))
                print(qparams)

                if qparams.get("id")==None:
                    print("The queries are missing or invalid.\n")
                    conn.sendall(b"HTTP/1.1 400 Bad Request\n"+b"Content-Type: text/html\n"+b"\n")
                
                resid = qparams["id"]
                #...



                
            else:
                print("Requested URL not found in Reservation Server.\n")
                conn.sendall(b"HTTP/1.1 400 Bad Request\n"+b"Content-Type: text/html\n"+b"\n")