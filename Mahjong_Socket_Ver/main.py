import multiprocessing
from multi_server import startServer
from multi_client import startClient

def main():
    server = multiprocessing.Process(target=startServer)
    server.start()
    print("Process1 started")
    startClient()
    server.join()

if __name__ == '__main__':
    main()