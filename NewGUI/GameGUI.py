class GameInfo:
    self.GM = None
    self.gameCount = 0
    self.playerTurn = 0
    self.yama = []
    self.baopai = []
    self.libaopai = []
    self.redbaopai = []
    self.playerInfos = []

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
    self.name = ""
    self.wind = ""
    self.drawCard = None
    self.hand = []
    self.ophand = []
    self.river = []

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

