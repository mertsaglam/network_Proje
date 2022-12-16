import socket
import requests
HOST = "localhost"  # The server's hostname or IP address
PORT = 8087 # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"GET /remove?name=CSE4197Seminar HTTP/1.1\r\nHost: localhost:8086\r\nAccept: text/html\r\n\r\n")
    data = s.recv(1024)
print(f"Received {data!r}")
