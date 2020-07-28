import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super(App,self).__init__()
        self.title("日本麻雀")
        width,height = 1000, 820
        self.geometry("{}x{}".format(width, height))
        self.resizable(False,False)
        self.iconbitmap("mahjong.ico")
        self.set_widgets()
    
    def run(self):
        self.mainloop()
        
    def set_widgets(self):
        self.board = tk.Canvas(self,width=1000,height=820,bg="black")
        self.board.pack()

class GameInfo:
    def __init__(self,GM):
        self.GM = GM
        self.gamecount = sum(GM.playerCounter)
        self.playerTurn = GM.player.name
        self.yama = GM.yama
        self.baopai = GM.baopai
        self.libaopai = GM.libaopai
        self.redbaopai = GM.redbaopai
        for p in GM.players:
            self.playerInfos.append(PlayerInfo(p))
    
    def update(self):
        self.__init__(self.GM)
    
    def draw(self):
        pass

class PlayerInfo:
    def __init__(self,player):
        self.player = player
        self.name = player.name
        self.wind = player.wind
        self.drawCard = player.draw
        self.hand = player.hand
        self.ophand = player.openhand
        self.river = palyer.river

    def update(self):
        self.__init__(self.player)

    def draw(self):
        pass


if __name__ == "__main__":
    app = App()
    app.run()
    
