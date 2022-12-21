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
            data = conn.recv(1024)
            urlstring = data.decode("utf-8")
            urlstring = urlstring.split("/")[1].split(" ")[0]
            funcType = urlstring.split("?")[0]





            if funcType == "reserve": # WORKING FINE.
                #/reserve?room=roomname&activity=activityname&day=x&hour=y&duration=z
                query_string = urlstring.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))

                if qparams.get("room")==None or qparams.get("activity")==None or qparams.get("day")==None or qparams.get("hour")==None or qparams.get("duration")==None:
                    print("[INFO]: " + "The queries are missing or invalid.\n") 
                    response = 'HTTP/1.1 400 Bad Request\r\n' + \
                               'Content-Type: text/html\r\n\r\n' + \
                               '<h1>The queries are missing or invalid.</h1>\r\n'
                    conn.sendall(response.encode())
                    continue

                roomName = qparams["room"]
                activityName = qparams["activity"]
                day = qparams["day"]
                hour = qparams["hour"]
                duration = qparams["duration"]

                
                if ScheduleUtils.isValidDay(day)==False or ScheduleUtils.isValidHour(hour)==False or ScheduleUtils.isValidDuration(duration)==False:
                    print("[INFO]: " + "The queries are missing or invalid.\n") 
                    response = 'HTTP/1.1 400 Bad Request\r\n' + \
                               'Content-Type: text/html\r\n\r\n' + \
                               '<h1>The queries are missing or invalid.</h1>\r\n'
                    conn.sendall(response.encode())
                    continue
                
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
                    a.connect((HOST,8082))
                    headers = "GET " + f"/check?name={activityName}" + " HTTP/1.1\r\n" + "Host: localhost:8082\r\n" + "Accept: text/html\r\n\rn"
                    a.sendall(headers.encode('utf-8'))
                    response = a.recv(1024).decode("utf-8")
                    status = response.split(" ")[1]
                    if status!="200":
                        conn.sendall(response.encode())
                        continue

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
                    a.connect((HOST,8081))
                    headers = "GET " + f"/reserve?room={roomName}&activity={activityName}&day={day}&hour={hour}&duration={duration}" + " HTTP/1.1\r\n" + "Host: localhost:8081\r\n" + "Accept: text/html\r\n\rn"
                    a.sendall(headers.encode('utf-8'))
                    response = a.recv(1024).decode("utf-8")
                    conn.sendall(response.encode())






            elif funcType=="listavailability":
                query_string = urlstring.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))
                
                if qparams.get("room")==None:
                    print("[INFO]: " + "The queries are missing or invalid.\n")
                    response = 'HTTP/1.1 400 Bad Request\r\n' + \
                               'Content-Type: text/html\r\n\r\n' + \
                               '<h1>The queries are missing or invalid.</h1>\r\n'
                    conn.sendall(response.encode())
                    continue
                
                roomName = qparams["room"]

                if qparams.get("day"):
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
                        day = qparams["day"]
                        a.connect((HOST,8081))
                        headers = "GET " + f"/checkavailability?name={roomName}&day={day}" + " HTTP/1.1\r\n" + "Host: localhost:8081\r\n" + "Accept: text/html\r\n\rn"
                        a.sendall(headers.encode('utf-8'))
                        response = a.recv(1024).decode("utf-8")
                        conn.sendall(response.encode())
                else:
                    availableTimes = "\r\n"
                    for day in range(1,8):
                        availableTimes = availableTimes + "<h1>"
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
                            a.connect((HOST,8081))
                            headers = "GET " + f"/checkavailability?name={roomName}&day={day}" + " HTTP/1.1\r\n" + "Host: localhost:8081\r\n" + "Accept: text/html\r\n\rn"
                            a.sendall(headers.encode('utf-8'))
                            response = a.recv(1024).decode("utf-8")
                            status = response.split(" ")[1]
                            if status!="200":
                                conn.sendall(response.encode())
                            else:
                                responsehours = response.split("[")[1].split("]")[0].split(" ")
                                availableHours = []
                                for hour in responsehours:
                                    if len(hour)>0:
                                        availableHours.append(hour)
                                availableTimes = availableTimes + ScheduleUtils.getDayName(day) + ":" + str(availableHours)

                        availableTimes = availableTimes + "<h1>\r\n"

                    response = 'HTTP/1.1 200 OK\r\n' + \
                                'Content-Type: text/html\r\n\r\n' + \
                                '<h1>The room, ' + roomName + ', is available in times:</h1>\r\n' + \
                                availableTimes
                    conn.sendall(response.encode())






            elif funcType=="display":
                query_string = urlstring.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))

                if qparams.get("id")==None:
                    print("[INFO]: " + "The queries are missing or invalid.\n")
                    response = 'HTTP/1.1 400 Bad Request\r\n' + \
                               'Content-Type: text/html\r\n\r\n' + \
                               '<h1>The queries are missing or invalid.</h1>\r\n'
                    conn.sendall(response.encode())
                    continue
                
                resid = qparams["id"]

                if ScheduleUtils.isValidReservationId(resid):
                    response = 'HTTP/1.1 200 OK\r\n' + \
                                'Content-Type: text/html\r\n\r\n' + \
                                ScheduleUtils.getReservationDetails(resid)
                    conn.sendall(response.encode())
                else:
                    print("[INFO]: " + "The reservation with id " + resid + " is not found.\n")
                    response = 'HTTP/1.1 404 Not Found\r\n' + \
                                'Content-Type: text/html\r\n\r\n' + \
                                '<h1>The reservation with id ' + resid + ' is not found.</h1>\r\n'
                    conn.sendall(response.encode())




            else:
                print("[INFO]: " + "The requested URL is not found in Reservation Server.\n")
                response = 'HTTP/1.1 404 Not Found\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The requested URL is not found in Reservation Server.</h1>\r\n'
                conn.sendall(response.encode())