import socket

def startServer():
    end = False

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # IP address
    localhost = "127.0.0.1"
    # Enable Port number
    port1 = 50000
    port2 = 50001
    # create socket
    s1.bind((localhost, port1))
    s2.bind((localhost, port2))

    # only accept one connection
    s1.listen(1)
    s2.listen(1)

    while not end:
        # accept two client
        connection1, addr1 = s1.accept()
        print(addr1," Accepted\n")
        connection2, addr2 = s2.accept()
        print(addr2," Accepted\n")

        while True:
            # in the loop, take the data(1024 bit)
            data1 = connection1.recv(1024)
            data2 = connection2.recv(1024)
            print("Data : ",data1," Addr : ",addr1,"\n")
            print("Data : ",data2," Addr : ",addr2,"\n")
            # if both data is same then finish server
            if data1 == data2:
                end = True
                break
            # send data back
            connection1.sendall("Recieved: ".encode("utf-8")+data2+" from others".encode("utf-8"))
            connection2.sendall("Recieved: ".encode("utf-8")+data1+" from others".encode("utf-8"))
            
        print("Both data is same.\n")

    connection1.sendall("Good Team Work".encode("utf-8"))
    connection2.sendall("Good Team Work".encode("utf-8"))

    s1.close()
    s2.close()

if __name__ == "__main__":
    startServer()