import socket

end = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # IP address
    localhost = "127.0.0.1"
    # Enable Port number
    port = 50000
    # create socket
    s.bind((localhost, port))
    # only accept one connection
    s.listen(1)

    while not end:
        connection, addr = s.accept()
        while True:
            # in the infinity loop, take the data(1024 bit)
            data = connection.recv(1024)
            # if data is not sended, break
            if not data:
                print("Data is not found")
                break
            # if data is END then finish server
            if data:
                end = True
                print("Data : ",data," Addr : ",addr)
                break