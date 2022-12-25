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

HOST = "localhost"
PORT = 8080

#################################################
#                                               #
#              SERVING FUNCTION                 #
# (The code running this funcion is at the end) #
#                                               #
#################################################

def serveRequest(conn):
    # Serve the incoming Requests.
    with conn:
        data = conn.recv(1024) # Receive the contents of the request.
        utfdata = data.decode("utf-8") # Convert it into UTF-8 format.
        method = utfdata.split(" ")[0] # In most cases first word will be request method.
        urlstring = utfdata.split("/")[1].split(" ")[0] # Get the end point of the URL
        # urlsting will be for example, /reserve?room=M2Z103&day=2&hour=10&duration=6&activity=webinar
        funcType = urlstring.split("?")[0]
        # Retrieve the function type.

        # If method is not GET or POST return error code 501.
        # This iddea was not stated explicity in the homework ducument.
        if method!="GET" and method!="POST":
            print("[INFO]: " +"The requested query contains methods that are not yet implemented in the server.\n")
            response = 'HTTP/1.1 501 Not Implemented\r\n' + \
                        'Content-Type: text/html\r\n\r\n' + \
                        '<h1>The requested query contains methods that are not yet implemented in the server. [501 Not Implemented]</h1>\r\n'
            conn.sendall(response.encode())
            return






        # The requested URL wants to reserve a room.
        if funcType == "reserve": # WORKING FINE.
            #/reserve?room=roomname&activity=activityname&day=x&hour=y&duration=z
            query_string = urlstring.split('?')[1]
            qparams  = dict(param.split('=') for param in query_string.split('&'))
            

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
            # We retrieved many query parameters. Now we have to make sure all are valid.
            # scheduleUtils contains some useful functions for this pupose.
            # You may want to review the functions we have implemented inside.
            

            
            if ScheduleUtils.isValidDay(day)==False or ScheduleUtils.isValidHour(hour)==False or ScheduleUtils.isValidDuration(duration)==False:
                print("[INFO]: " + "The queries are missing or invalid.\n") 
                response = 'HTTP/1.1 400 Bad Request\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The queries are missing or invalid. [400 Bad Request]</h1>\r\n'
                conn.sendall(response.encode())
                return
            # We learned all passed parameters are valid. Now it is time to perform our task.

            # First we connect to activity server to check if the passed activity name really exists.
            # If not, then send error.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
                a.connect((HOST,8082))
                headers = "GET " + f"/check?name={activityName}" + " HTTP/1.1\r\n" + "Host: localhost:8082\r\n" + "Accept: text/html\r\n\rn"
                a.sendall(headers.encode('utf-8'))
                response = a.recv(1024).decode("utf-8")
                status = response.split(" ")[1]
                if status!="200":
                    # If the status code of activity server is not 200 then requested activity is not found.
                    conn.sendall(response.encode())
                    return


            # We saw the activity exists. Now, it is time to reserve the room.
            # Remember that we are reserving to the room with the help of Room Server.
            # In this case, many response bodys etc. will be implemented in Room Server.
            # You may want to review reserve function in Room Server.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
                a.connect((HOST,8081))
                headers = "GET " + f"/reserve?room={roomName}&activity={activityName}&day={day}&hour={hour}&duration={duration}" + " HTTP/1.1\r\n" + "Host: localhost:8081\r\n" + "Accept: text/html\r\n\rn"
                a.sendall(headers.encode('utf-8'))
                response = a.recv(1024).decode("utf-8")
                conn.sendall(response.encode())





        # The requested URL wants to check availablitiy of a room in some day.
        elif funcType=="listavailability": # WORKING FINE.
            query_string = urlstring.split('?')[1]
            qparams  = dict(param.split('=') for param in query_string.split('&'))
            # Retrieve the query parameters with the help of dictionaries as we always do.
            
            if qparams.get("room")==None:
                print("[INFO]: " + "The queries are missing or invalid.\n")
                response = 'HTTP/1.1 400 Bad Request\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The queries are missing or invalid. [400 Bad Request]</h1>\r\n'
                conn.sendall(response.encode())
                return
            
            roomName = qparams["room"]
            # There is a 'room' parameters passed. So, we are fine.
            # Now we check other parameters.
            # We may return errors if any these missing.
            if qparams.get("day"):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
                    day = qparams["day"]
                    a.connect((HOST,8081))
                    headers = "GET " + f"/checkavailability?name={roomName}&day={day}" + " HTTP/1.1\r\n" + "Host: localhost:8081\r\n" + "Accept: text/html\r\n\rn"
                    a.sendall(headers.encode('utf-8'))
                    response = a.recv(1024).decode("utf-8")
                    conn.sendall(response.encode())
            else:
                # All required parameters exist. Now it is time to perform our real task.
                availableTimes = "\r\n" 
                # availableTimes variable will hold the day names and hours that the room is available.
                for day in range(1,8): # We check for all week days.
                    availableTimes = availableTimes + "<h1>" # We need to have HTML form.
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
                        # Connect to Room Server and learn availability.
                        # We then write the relevant information for each day.
                        a.connect((HOST,8081))
                        headers = "GET " + f"/checkavailability?name={roomName}&day={day}" + " HTTP/1.1\r\n" + "Host: localhost:8081\r\n" + "Accept: text/html\r\n\rn"
                        a.sendall(headers.encode('utf-8'))
                        response = a.recv(1024).decode("utf-8")
                        status = response.split(" ")[1]
                        if status!="200":
                            # Some error occurred. Most probably the something went wrong with IO operations.
                            conn.sendall(response.encode())
                        else:
                            responsehours = response.split("[")[1].split("]")[0].split(" ")
                            availableHours = []
                            for hour in responsehours:
                                if len(hour)>0:
                                    availableHours.append(hour)
                            availableTimes = availableTimes + ScheduleUtils.getDayName(day) + ":" + str(availableHours)
                            # Insert the available hours and the weekday with the help of scheduleUtils.getDayName funcion.
                            # getDayName returns Monday for 1, Tuesday for 2 etc.

                    availableTimes = availableTimes + "<h1>\r\n" # Ready to read the next day.

                response = 'HTTP/1.1 200 OK\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The room, ' + roomName + ', is available in times: [200 OK]</h1>\r\n' + \
                            availableTimes
                conn.sendall(response.encode())
                # We have retrieved the schedule for the requested room. Now return it.
                # Remember availableTimes variable contains the whole schedule info.





        # The requested URL wants to review information of some reservation.
        elif funcType=="display": # WORKING FINE.
            query_string = urlstring.split('?')[1]
            qparams  = dict(param.split('=') for param in query_string.split('&'))
            # Retrieve the parameters passed.

            if qparams.get("id")==None:
                print("[INFO]: " + "The queries are missing or invalid.\n")
                response = 'HTTP/1.1 400 Bad Request\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The queries are missing or invalid. [400 Bad Request]</h1>\r\n'
                conn.sendall(response.encode())
                return
            
            
            resid = qparams["id"]
            # Now it is time to use the ID of the reservation.
            # First we check if it is valid. It should be an number.
            # Also IDs are generated by counting the existing reservations.
            # So, it should not be greater than the number of reservations exist.
            # Relevant code for this check can be found in scheduleUtils.isValidReservationId()
            if ScheduleUtils.isValidReservationId(resid):
                response = 'HTTP/1.1 200 OK\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            ScheduleUtils.getReservationDetails(resid)
                conn.sendall(response.encode())
            else:
                print("[INFO]: " + "The reservation with id " + resid + " is not found.\n")
                response = 'HTTP/1.1 404 Not Found\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The reservation with id ' + resid + ' is not found. [404 Not Found]</h1>\r\n'
                conn.sendall(response.encode())




        else: # WORKING FINE.
            # Requested URL did not match with any of our end points. So, return 404.
            print("[INFO]: " + "The requested URL is not found in Reservation Server.\n")
            response = 'HTTP/1.1 404 Not Found\r\n' + \
                        'Content-Type: text/html\r\n\r\n' + \
                        '<h1>The requested URL is not found in Reservation Server. [404 Not Found]</h1>\r\n'
            conn.sendall(response.encode())







#################################################
#                                               #
#                 RUNNER CODE                   #
#                                               #
#################################################

# We create a thread for each request arriving at our server.
# That way, we will be providing concurrency.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[INFO]: Reservation Server is started to listening to the address, " + socket.gethostbyname(HOST) + ":" + str(PORT))
    while True:
        conn, addr = s.accept()
        threading.Thread(target=serveRequest, args=(conn,)).start()
        # Print the number of threads running in the Reservation Server.
        print("[INFO]: The number of active connections in Reservation Server at the moment: "+str(threading.active_count()-1))

