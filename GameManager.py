import Pai

class GameManager:
    # prepared all the Pai and 4 players
    def __init__(self,players):
        self.players = []
        for p in players:
            self.players.append(p)
        self.yama = Pai.originalYama
    
    # give 13 pai to each players
    def startGame():
        for player in self.players:
            hand = self.yama[:13]
            self.yama = self.yama[13:]
            player.giveHand(hand)
        self.nextPlayer = 0
        self.cutPai = None
        print("Prepared")

    def zeroYama():
        if len(self.yama) <= 0:
            print("Yama is empty")
            print("Finish game")
            return True
        return False
    
    # player class will call this function when they Ron.
    # then this function will prit the result
    def playerWin(player):
        content = ""
        content += "###############################################################################################\n"
        content += "Player "+player.name+" Win!!\n"
        content += "Points: "+str(player.point)+"\n"
        content += "役: "+player.yaku+"\n"  # player.yaku : str = players hand type name 平和 etc.
        player.hand.sort()
        content += str(Pai.showHand(player.hand))+"\n"
        content += "################################################################################################\n"
        print(content)

    # expect palyer will return MinType and minSet and cutPai
    # player : player class
    # minType : str representing "chi" "pon" or "kan"
    # minSet : [Pai] which represent 3 or 4 Pais with "chi" "pon" or "kan"
    # cutPai: Pai which player will cut
    def playerMin(player,minType,minSet,cutPai):
        content = ""
        content += "################################################################################################\n"
        content += "Player "+player.name+" did "+minType+"\n"
        content += "Set is "+str(Pai.showHand(minSet))+"\n"
        content += "#################################################################################################\n"
        self.cutPai = cutPai
        self.nextPlayer = (self.players.index(player)+1) % 4
        content += "Player "+player.name+"cut "+str(self.cutPai)+"\n"
        content += "next Player: "+self.nextPlayer.name+"\n"
        print(content)
    
    # player will call this function when cut the pai
    def cutPai(player, cutPai):
        self.cutPai = cutPai
        self.nextPlayer = (self.players.index(player)+1) % 4
        content += "Player "+player.name+"cut "+str(self.cutPai)+"\n"
        content += "next Player: "+self.nextPlayer.name+"\n"
        print(content)
    
    # show information for player   
    def playerShow(player):
        content += ""
        # print each players River (already cut Pais)
        for p in self.players:
            # player.river is Pais player already cut
            content += "Player "+p.name+"'s River is "+Pai.showHand(p.river)+"\n"
            content += "Player "+p.name+"'s hand is secret"
        for p in self.players:
            # player.min is player's min Pai already got
            # player.gotPai is the Pai Player got now 
            if p == player:
                content += "----------------------------------------------------\n"
                content += "Main Player :"+player.name+"\n"
                content += "Min Pai :"+Pai.showHand(player.min)+"\n"
                content += "Player's Hand: "+Pai.showHand(player.hand)+"\n"
                content += "Player get "+str(player.gotPai)+"\n"
                content += "----------------------------------------------------\n"
                continue
            content += "Player "+p.name+"'s Hand is "+"SECRET"+"\n"
            content += "Player "+p.name+"'s Min Pai is "+Pai.showHand(p.min)+"\n"
        print(content)
            
    def mainGame():
        # prepare game
        self.startGame()
        
        # check whether yama is empty or not 
        while self.zeroYama()
            # give Pai to the player and check win
            player = self.players[self.nextPlayer]
            print("----------------------MAIN PLAYER: ",player.name,"----------------------")
            pai = self.yama[0]
            self.yama = self.yama[1:]
            
            player.givePai(pai)
            # player.checkWin() should call GameMaster.playerWin(player) if Roned
            player.checkWin()
            
            # show info and get cut pai from player
            self.playerShow(player)
            # player should call GameMaster.cutPai for set self.cutPai
            player.askCut()
            
            # check the player who want to Min and select player who could Min
            minPlayers = []
            for p in self.players:
                # player who want to Min have to declear in this stage
                minType, MinSet, cutPai = p.askMin()
                minPlayers.append([p, minType, minSet, cutPai])
            
            if not len(minPlayers) == 0:
                minPlayer = self.selectMinPlayers(minPlayers)
                # excecute Min
                self.playerMin(minPlayer)
            print("To Next Turn >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    def selectMinPlayers(minPlayers):
        player = None
        for args in minPlayers:
            if "Kan" in args:
                player = args
                break
            else if "Pon" in args:
                player = args
                break
            else if "Chi" in args:
                player = args
                break
            else:
                pass
        return player



