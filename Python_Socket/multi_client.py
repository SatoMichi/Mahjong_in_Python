import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # IP address
    localhost = "127.0.0.1"
    # Enable Port number 50000 or 50001
    port = int(input("Please input Port 50000 or 50001\n"))
    # connect to server
    s.connect((localhost,port))
    end = False

    while not end:
        # send data
        data = input("Please enter the Word\n").encode("utf-8")
        s.sendall(data)
        # recieve data(1024byte)
        data = s.recv(1024)
        if data == "Good Team Work".encode("utf-8"):
            end = True
        print(data)
    
    print("Server closed")