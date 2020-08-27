import json
import socket

import kivy
kivy.require("1.11.1")
from kivy.app import App
from kivy.lang import Builder
import kivy.properties as kyprops
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager
from kivy.uix.textinput import TextInput


class MainScreen(Screen):
    pass

class Login_Screen(Screen):
    port = kyprops.ObjectProperty(None)
    host = kyprops.ObjectProperty(None)


    def btn(self): 
        #s.settimeout(3)
        if_show = True
        try:
            port_no = int(port.text)
            s.connect((host.text, port_no))    
        except:
            if_show = False
            self.port.text = ""
            self.host.text = ""
            show = Login_Failure()
            popupWindow = Popup(title="Login Result", content=show, size_hint=(0.4,0.4), pos_hint={"x":0.3,"y":0.3})
            popupWindow.open()
        if if_show:
            self.port.text = ""
            self.host.text = ""
            show = Login_Success()
            popupWindow = Popup(title="Login Result", content=show, size_hint=(0.8,0.8), pos_hint={"x":0.1,"y":0.1})
            popupWindow.open()
                


class GameScreen(Screen):
    # pai_1 = kyprops.StringProperty(None)
    # pai_2 = kyprops.StringProperty(None)
    # pai_3 = kyprops.StringProperty(None)
    # pai_4 = kyprops.StringProperty(None)
    # pai_5 = kyprops.StringProperty(None)
    # pai_6 = kyprops.StringProperty(None)
    # pai_7 = kyprops.StringProperty(None)
    # pai_8 = kyprops.StringProperty(None)
    # pai_9 = kyprops.StringProperty(None)
    # pai_10 = kyprops.StringProperty(None)
    # pai_11 = kyprops.StringProperty(None)
    # pai_12 = kyprops.StringProperty(None)
    # pai_13 = kyprops.StringProperty(None)
    pais = [kyprops.StringProperty(None)] * 14
    # pai_14 = kyprops.StringProperty(None)

    def setup(self):
        data = s.recv(2048)
        data = data.decode("utf-8")
        data = json.loads(data)
        list_of_pai = data["hand"]
        pai_str = "../img/imgUp/p_"
        for i,pai in enumerate(list_of_pai):
            self.pais[i] = pai_str + str(pai[0]) + ".png"
        

class ScreenManagement(ScreenManager):
    pass

class Login_Success(FloatLayout):
    pass

class Login_Failure(FloatLayout):
    pass


class MainApp(App):
    def build(self):
        presentation = Builder.load_file("main.kv")
        return presentation

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == "__main__":
    MainApp().run()
