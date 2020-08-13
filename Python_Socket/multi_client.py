import socket

def startClient(ip="127.0.0.1", port=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Enable Port number 60000 or 60001
        if not port:
            port = int(input("Please input Port 50000 or 50001\n"))
        # connect to server
        s.connect((ip,port))
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

if __name__ == "__main__":
    startClient()