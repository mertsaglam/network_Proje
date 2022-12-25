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

HOST = "localhost"  
PORT = 8082

#################################################
#                                               #
#              SERVING FUNCTION                 #
# (The code running this funcion is at the end) #
#                                               #
#################################################
def serveRequest(conn):
    # This function will handle the incoming requests.
    with conn:
        data = conn.recv(1024)
        # Receive the contents of the request.
        utfdata = data.decode("utf-8")
        # Decode it into UTF-8
        method = utfdata.split(" ")[0]
        # In %99.999 of the cases, first word will be the request method.
        url = utfdata.split(" ")[1]
        # In %99.999 of the cases, second word will be the requested URL.
        url = url.split("/")[1]

        # Check if the requested method is either POST or GET. Otherwise, return code:501.
        # This issue was not stated in the homework document but we implemented as extra idea.
        if method!="GET" and method!="POST":
            print("[INFO]: " +"The requested query contains methods that are not yet implemented in the server.\n")
            response = 'HTTP/1.1 501 Not Implemented\r\n' + \
                        'Content-Type: text/html\r\n\r\n' + \
                        '<h1>The requested query contains methods that are not yet implemented in the server. [501 Not Implemented]</h1>\r\n'
            conn.sendall(response.encode())
            return





        # Requested URL wants to add an activity.
        if url.startswith("add?"): # WORKING FINE.
            query_string = url.split('?')[1]
            # query_string will be /add?name=Webinar
            qparams = dict(param.split('=') for param in query_string.split('&'))
            # Parse params with the help of the dictionaries in Python.
            # We use dictionary because the order of these queries may change.
            # It was not explicitly stated in the document but we have added as an extra idea.
            
            # If the query does not have 'name' parameter return error code 400.
            if qparams.get("name")==None:
                print("[INFO]: " +"The queries are missing or invalid.\n")
                response = 'HTTP/1.1 400 Bad Request\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The queries are missing or invalid. [400 Bad Request]</h1>\r\n'
                conn.sendall(response.encode())
                return

            # If name parameter is exists, then we are ready to insert it.
            # But, first, we have to make sure that there is no activity with that name.
            # If exists, then return 403 Forbidden as stated in the homework document.
            activityName = qparams["name"]
            with open("activities.txt", "r") as f:
                if activityName +"\n" not in f.read():
                    with open("activities.txt", "a") as f:
                        f.write(activityName + "\n")
                        print("[INFO]: " +'The activity, ' + activityName + ' is successfully added.')
                        
                        response = 'HTTP/1.1 200 OK\r\n' + \
                                'Content-Type: text/html\r\n\r\n' + \
                                '<h1>The activity, ' + activityName + ' is successfully added. [200 OK]</h1>\r\n'
                        conn.sendall(response.encode())
                else:
                    print("[INFO]: " +"The requested activity already exists.")
                    response = 'HTTP/1.1 403 Forbidden\r\n' + \
                                'Content-Type: text/html\r\n\r\n' + \
                                '<h1>The requested activity already exists. [403 Forbidden]</h1>\r\n'
                    conn.sendall(response.encode())






        # The reqested URL wants to remove an activity.
        elif url.startswith("remove?"): # WORKING FINE.
            query_string = url.split('?')[1]
            qparams  = dict(param.split('=') for param in query_string.split('&'))
            # Check if name parameter exists.
            if qparams.get("name")==None:
                print("[INFO]: " +"The queries are missing or invalid.\n")
                response = 'HTTP/1.1 400 Bad Request\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The queries are missing or invalid. [400 Bad Request]</h1>\r\n'
                conn.sendall(response.encode())
                return

            activityName = qparams["name"]
            # Before we remove it we have to make sure there actually an activity with that name.
            # If there is no activity with that name, return error code 403.
            with open("activities.txt", "r") as f:
                if activityName + "\n" in f.read():
                    with open("activities.txt", "r") as f:
                        lines = f.readlines()
                    with open("activities.txt", "w") as f:
                        for line in lines:
                            if line.strip("\n") != activityName:
                                f.write(line)
                    print("[INFO]: " +'The activity,' + activityName + ' is successfully removed.')
                    response = 'HTTP/1.1 200 OK\r\n' + \
                                'Content-Type: text/html\r\n\r\n' + \
                                '<h1>The activity, ' + activityName + ' is successfully removed. [200 OK]</h1>\r\n'
                    conn.sendall(response.encode())
                else:
                    print("[INFO]: " +"The requested activity does not exist.")
                    response = 'HTTP/1.1 403 Forbidden\r\n' + \
                                'Content-Type: text/html\r\n\r\n' + \
                                '<h1>The requested activity does not exist. [403 Forbidden]</h1>\r\n'
                    conn.sendall(response.encode())




        # Requested URL wants to check existence of some activity.
        elif url.startswith("check?"): # WORKING FINE.
            # Parse the activity name by using dictionary in Python.
            query_string = url.split('?')[1]
            qparams  = dict(param.split('=') for param in query_string.split('&'))
            # No activity name parameter is passed so return error code 400.
            if qparams.get("name")==None:
                print("[INFO]: " +"The queries are missing or invalid.\n")
                response = 'HTTP/1.1 400 Bad Request\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The queries are missing or invalid. [400 Bad Request]</h1>\r\n'
                conn.sendall(response.encode())
                return

            activityName = qparams["name"]
            # Check if the passed activity name exists. If so return 200, else 404.
            with open("activities.txt", "r") as f:
                if activityName in f.read():
                    print("[INFO]: " +"The requested activity exists.")
                    response = 'HTTP/1.1 200 OK\r\n' + \
                        'Content-Type: text/html\r\n\r\n' + \
                        '<h1>The requested activity exists. [200 OK]</h1>\r\n'
                    conn.sendall(response.encode())
                else:
                    print("[INFO]: " +"The requested activity does not exist.")
                    response = 'HTTP/1.1 404 Not Found\r\n' + \
                        'Content-Type: text/html\r\n\r\n' + \
                        '<h1>The requested activity does not exist. [404 Not Found]</h1>\r\n'
                    conn.sendall(response.encode())



        else: # WORKING FINE.
            # The requested URL did not match any of our end points. Return 404.
            print("[INFO]: " +"Requested URL not found in Activity Server.")
            response = 'HTTP/1.1 404 Not Found\r\n' + \
                        'Content-Type: text/html\r\n\r\n' + \
                        '<h1>The requested URL is not found in Activity Server. [404 Not Found]</h1>\r\n'
            conn.sendall(response.encode())








#################################################
#                                               #
#                 RUNNER CODE                   #
#                                               #
#################################################

# This part is to create a thread for each request to provide concurrency among in many requests.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[INFO]: Activity Server is started to listening to the address, " + socket.gethostbyname(HOST) + ":" + str(PORT))
    # LOG the address of the server run.
    while True:
        conn, addr = s.accept()
        threading.Thread(target=serveRequest, args=(conn,)).start()
        print("[INFO]: The number of active connections in Activity Server at the moment: "+str(threading.active_count()-1))
        # Printing the number of threads. -1 due to the parent thread running this program.
        



        

