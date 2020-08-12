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
        # recieve data(1024byte)
        data = s.recv(2048)
        # if "GAMEEND" is sent from server, finish client
        if data and data == "GAMEEND".encode("utf-8"):
            GameEnd = True
        # if server need input, then send the input data
        elif data and data.decode("utf-8")[-1] == "Q":
            send = input(data.decode("utf-8")[:-1])
            s.sendall(send.encode("utf-8"))
        # else, print the game info sent from server
        elif data:
            print(data.decode("utf-8"))
        else:
            pass
    
    print("Server closed")
    s.close()