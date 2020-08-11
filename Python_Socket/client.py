import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # IP address
    localhost = "127.0.0.1"
    # Enable Port number
    port = 50000
    # connect to server
    s.connect((localhost,port))
    # send data
    data = input("Please enter the DATA\n").encode("utf-8")
    s.sendall(data)
    # recieve data(1024byte)
    data = s.recv(1024)
    print(data)