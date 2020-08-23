import socket
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget

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
            if data and data == "FINISH GAME".encode("utf-8"):
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

class MainScreen(Screen):
    pass

class AnotherScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        return presentation

if __name__ == "__main__":
    MainApp().run()
    #startClient()