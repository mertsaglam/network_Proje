import socket

HOST = "localhost"  
PORT = 8082

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            utfdata = data.decode("utf-8")
            method = utfdata.split(" ")[0]
            url = utfdata.split(" ")[1]
            url = url.split("/")[1]

            if method!="GET" and method!="POST":
                print("[INFO]: " +"The requested query contains methods that are not yet implemented in the server.\n")
                response = 'HTTP/1.1 501 Not Implemented\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The requested query contains methods that are not yet implemented in the server.</h1>\r\n'
                conn.sendall(response.encode())
                continue






            if url.startswith("add?"): # WORKING FINE.
                query_string = url.split('?')[1]
                qparams = dict(param.split('=') for param in query_string.split('&'))
                
                if qparams.get("name")==None:
                    print("[INFO]: " +"The queries are missing or invalid.\n")
                    response = 'HTTP/1.1 400 Bad Request\r\n' + \
                               'Content-Type: text/html\r\n\r\n' + \
                               '<h1>The queries are missing or invalid.</h1>\r\n'
                    conn.sendall(response.encode())
                    continue

                activityName = qparams["name"]
                with open("activities.txt", "r") as f:
                    if activityName +"\n" not in f.read():
                        with open("activities.txt", "a") as f:
                            f.write(activityName + "\n")
                            print("[INFO]: " +'The activity,' + activityName + ' is successfully added.')
                            
                            response = 'HTTP/1.1 200 OK\r\n' + \
                                    'Content-Type: text/html\r\n\r\n' + \
                                    '<h1>The activity,' + activityName + ' is successfully added.</h1>\r\n'
                            conn.sendall(response.encode())
                    else:
                        print("[INFO]: " +"The requested activity already exists.")
                        response = 'HTTP/1.1 403 Forbidden\r\n' + \
                                    'Content-Type: text/html\r\n\r\n' + \
                                    '<h1>The requested activity already exists.</h1>\r\n'
                        conn.sendall(response.encode())







            elif url.startswith("remove?"): # WORKING FINE.
                query_string = url.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))
                if qparams.get("name")==None:
                    print("[INFO]: " +"The queries are missing or invalid.\n")
                    response = 'HTTP/1.1 400 Bad Request\r\n' + \
                               'Content-Type: text/html\r\n\r\n' + \
                               '<h1>The queries are missing or invalid.</h1>\r\n'
                    conn.sendall(response.encode())
                    continue

                activityName = qparams["name"]

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
                                    '<h1>The activity,' + activityName + ' is successfully removed.</h1>\r\n'
                        conn.sendall(response.encode())
                    else:
                        print("[INFO]: " +"The requested activity does not exist.")
                        response = 'HTTP/1.1 403 Forbidden\r\n' + \
                                    'Content-Type: text/html\r\n\r\n' + \
                                    '<h1>The requested activity does not exist.</h1>\r\n'
                        conn.sendall(response.encode())





            elif url.startswith("check?"): # WORKING FINE.
                query_string = url.split('?')[1]
                qparams  = dict(param.split('=') for param in query_string.split('&'))
                if qparams.get("name")==None:
                    print("[INFO]: " +"The queries are missing or invalid.\n")
                    response = 'HTTP/1.1 400 Bad Request\r\n' + \
                               'Content-Type: text/html\r\n\r\n' + \
                               '<h1>The queries are missing or invalid.</h1>\r\n'
                    conn.sendall(response.encode())
                    continue

                activityName = qparams["name"]

                with open("activities.txt", "r") as f:
                    if activityName in f.read():
                        print("[INFO]: " +"The requested activity exists.")
                        response = 'HTTP/1.1 200 OK\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The requested activity exists.</h1>\r\n'
                        conn.sendall(response.encode())
                    else:
                        print("[INFO]: " +"The requested activity does not exist.")
                        response = 'HTTP/1.1 404 Not Found\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The requested activity does not exist.</h1>\r\n'
                        conn.sendall(response.encode())



            else: # WORKING FINE.
                print("[INFO]: " +"Requested URL not found in Activity Server.")
                response = 'HTTP/1.1 404 Not Found\r\n' + \
                            'Content-Type: text/html\r\n\r\n' + \
                            '<h1>The requested URL is not found in Activity Server.</h1>\r\n'
                conn.sendall(response.encode())
        
        