import socket

def startClient():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            # if "FINISH GAME" is sent from server, finish client
            if data and data.decode("utf-8") == "FINISH GAME":
                GameEnd = True
            # if server need input, then send the input data
            elif data and data.decode("utf-8")[-1] == "Q":
                send = input(data.decode("utf-8")[:-1]) #send = "13"
                s.sendall(send.encode("utf-8"))
            # else, print the game info sent from server
            elif data:
                print(data.decode("utf-8"))
            else:
                pass
        
        print("Server closed")
        s.close()

if __name__ == "__main__":
    startClient()