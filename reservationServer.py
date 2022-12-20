import socket
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
                print(qparams)

                if qparams.get("room")==None or qparams.get("activity")==None or qparams.get("day")==None or qparams.get("hour") or qparams.get("duration")==None:
                    print("The queries are missing or invalid.\n")
                    conn.sendall(b"HTTP/1.1 400 Bad Request \n")
                
                roomName = qparams["room"]
                activityName = qparams["activity"]
                day = qparams["day"]
                hour = qparams["hour"]
                duration = qparams["activity"]
                print("Room: " + roomName)
                print("Activity: " + activityName)
                print("Day: " + day)
                print("Hour: " + hour)
                print("Duration: " + duration)

                
                """
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
                    a.connect((HOST, 8081))
                    a.sendall(b"GET /check?name="
                    + activityName.encode("utf-8")
                    + b" HTTP/1.1\r\nHost: localhost:8086\r\nAccept: text/html\r\n\r\n")
                    response = a.recv(1024).decode("utf-8")
                    response = response.split(" ")[1]
                    if response == 200:
                        print("Activity exists")
                    else:
                        print("Activity does not exist") 
                """
            elif funcType=="listavailability":
                pass
            elif funcType=="display":
                pass
            else:
                print("Requested URL not found in Reservation Server.\n")
                conn.sendall(b"HTTP/1.1 400 Bad Request \n")