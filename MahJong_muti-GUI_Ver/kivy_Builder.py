import socket
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

class MainScreen(Screen):
    pass

class Login_Screen(Screen):
    def btn(self): 
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if_show = True
        try:
            self.s.connect((self.ids.host.text,self.ids.port.text))
        except:
            if_show = False
            show = Login_Failure()
            popupWindow = Popup(title="Login Result", content=show, size_hint=(0.4,0.4), pos_hint={"x":0.3,"y":0.3})
            popupWindow.open()
        if if_show:
            show = Login_Success()
            popupWindow = Popup(title="Login Result", content=show, size_hint=(0.8,0.8), pos_hint={"x":0.1,"y":0.1})
            popupWindow.open()
                


class AnotherScreen_2(Screen):
    pass

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

if __name__ == "__main__":
    MainApp().run()