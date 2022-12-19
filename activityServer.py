import socket
HOST = "localhost"  
PORT = 8082
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            # conn.sendall(b"HTTP/1.1 200 OK\r\n"
            # + b"Content-Type: text/html\r\n\n"
            # + b"<p>Hello, world!</p>\r\n")
            data = conn.recv(1024)
            url = data.decode("utf-8").split(" ")[1]
            url = url.split("/")[1]
            print(url)
            #/add?name=activityname 
            if url.startswith("add?"):
                activityName = url.split("?")[1].split("=")[1]
                #open the activity file and add the activity if it is not already there
                with open("activities.txt", "r") as f:
                    if activityName +"\n" not in f.read():
                        with open("activities.txt", "a") as f:
                            f.write(activityName + "\n")
                            print("Added activity: " + activityName)
                            
                            conn.sendall(b"HTTP/1.1 200 OK\n"
                                        +b"Content-Type: text/html\n"
                                        +b"\n" # Important!
                                        +b"Added activity: " + activityName.encode("utf-8"))
                    else:
                        print("Activity already exists")
                        conn.sendall(b"HTTP/1.1 403 Forbidden \n")
            elif url.startswith("remove?"):
                activityName = url.split("?")[1].split("=")[1]
                with open("activities.txt", "r") as f:
                    if activityName + "\n" in f.read():
                        with open("activities.txt", "r") as f:
                            lines = f.readlines()
                        with open("activities.txt", "w") as f:
                            for line in lines:
                                if line.strip("\n") != activityName:
                                    f.write(line)
                        print("Removed activity: " + activityName)
                        conn.sendall(b"HTTP/1.1 200 OK\n"
                                    +b"Content-Type: text/html\n"
                                    +b"\n" # Important!
                                    +b"Removed activity: " + activityName.encode("utf-8"))
                    else:
                        print("Activity does not exist")
                        conn.sendall(b"HTTP/1.1 403 Forbidden \n")
            elif url.startswith("check?"):
                activityName = url.split("?")[1].split("=")[1]
                with open("activities.txt", "r") as f:
                    if activityName in f.read():
                        print("Activity exists")
                        conn.sendall(b"HTTP/1.1 200 OK\n"
                                    +b"Content-Type: text/html\n"
                                    +b"\n" # Important!
                                    +b"Activity exists "
                                    +activityName.encode("utf-8"))
                    else:
                        print("Activity does not exist")
                        conn.sendall(b"HTTP/1.1 404 Not Found \n")
            else:
                print("Invalid URL")
                conn.sendall(b"HTTP/1.1 404 Not Found \n")