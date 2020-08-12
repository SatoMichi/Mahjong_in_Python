import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # IP address
    localhost = "127.0.0.1"
    # Enable Port number 50000 or 50001
    port = int(input("Please input Port 50000 ~ 50003\n"))
    # connect to server
    s.connect((localhost,port))
    GameEnd = False

    while not GameEnd:
        # send data
        #data = input("Please enter the Word\n").encode("utf-8")
        #s.sendall(data)
        # recieve data(1024byte)
        data = s.recv(2048)
        if data == "GAMEEND".encode("utf-8"):
            GameEnd = True
        print(data.decode("utf-8"))
    
    print("Server closed")
    s.close()