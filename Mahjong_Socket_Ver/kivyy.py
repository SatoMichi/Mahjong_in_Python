from kivy.app import App
#kivy.require("1.8.0")
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.lang import Builder
import kivy.resources


Builder.load_string('''
<Label>:
    font_name: 'AdobeGothicStd-Bold.otf'

<Widgets>:
    Label:
        text: "ABC ÄäÜüß にほんご 中文 ру́сский язы́к ÉéÈèÊêËë Españolالعَرَبِيَّة‎ ‎français"
        size: root.width, 75
        pos: root.x, root.top - 150
        font_size: 50
        height: 75
''')

class Widgets(Widget):
    def build(self):
        return Widgets()

class MyApp(App):
    def build(self):
        return Widgets()

if __name__ == "__main__":
    MyApp().run()