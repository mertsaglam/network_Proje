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
            url = data.decode("utf-8")
            print(data)
            print(url)
            url = url.split("/")[1].split(" ")[0]
            print(url + " requested\n")
            funcType = url.split("=")[0]
            if funcType == "reserve?room":
                #/reserve?room=roomname&activity=activityname&day=x&hour=y&duration=z
                roomName = url.split("=")[1].split("&")[0]
                activityName = url.split("=")[2].split("&")[0]
                day = url.split("=")[3].split("&")[0]
                hour = url.split("=")[4].split("&")[0]
                duration = url.split("=")[5].split("&")[0]
                print("Room: " + roomName)
                print("Activity: " + activityName)
                print("Day: " + day)
                print("Hour: " + hour)
                print("Duration: " + duration)
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