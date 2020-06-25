import Pai
from TestPlayer import Player
import numpy as np

# this class is Finite State Machine
class GameManager:
    # prepared all the Pai and 4 players
    def __init__(self,players):
        self.players = []
        for p in players:
            self.players.append(p)
        self.yama = Pai.originalYama
    
    # give 13 pai to each players
    def startGame(self):
        for wind, player in zip(["東","南","西","北"], self.players):
            hand = self.yama[:13]
            self.yama = self.yama[13:]
            # call player's method
            player.setWind(wind)
            player.setHand(hand)
        self.cutPai = None
        self.state = "SET_PLAYER"
        self.winner = None
        self.playerCounter = np.zeros([4])
        self.minCounter = np.zeros([4,4])
        self.riichiTurn = [(0,False)]*4
        self.playerTumo = [False,False,False,False]
        self.playerYaku = [""]*4
        self.rinxian = False
        print("Prepared\nLet's Start the GAME !!\n")

    # check yama is empty or not
    def zeroYama(self):
        if len(self.yama) <= 14:
            return True
        return False

    # show information for player playing his turn   
    def printPlayerTurn(self,player):
        content = ""
        # print each players River (already cut Pais)
        for p in self.players:
            # player.river is Pais player already cut
            content += "Player "+p.name+"'s River is "+Pai.showHand(p.river)+"\n"
        for p in self.players:
            # player.min is player's min Pai already got
            if p == player:
                content += "----------------------------------------------------\n"
                content += "Main Player :"+player.name+"\n"
                content += "Min Pai :"+Pai.showHand(Pai.array2Hand(player.openHand))+"\n"
                content += "Player's Hand: "+Pai.showHand(player.hand)+"\n"
                content += "----------------------------------------------------\n"
                continue
            content += "Player "+p.name+"'s Hand is "+"SECRET"+"\n"
            content += "Player "+p.name+"'s Min Pai is "+Pai.showHand(Pai.array2Hand(p.openHand))+"\n"
        print(content)

    # set state, cutPai and nextPlayer
    def playerCutPai(self,player,cutPai):
        self.cutPai = cutPai
        content = ""
        content += "Player "+player.name+" cut "+str(Pai.paiSet[self.cutPai])+"\n"
        print(content)

    # print winner's information
    def printWinner(self):
        if self.winner == None:
            print("---------------------------NO ONE WIN-------------------------\n")
        else:
            player = self.winner
            yaku = self.playerYaku[self.players.index(player)]
            content = ""
            if player == None:
                content += "No One Wined" + "\n"
            else:
                content += "###############################################################################################\n"
                content += "Player "+player.name+" Win!!\n"
                content += "Points: "+str(player.score)+"\n"
                content += "役: "+yaku+"\n"
                player.hand.sort()
                content += str(Pai.showHand(player.hand))+"\n"
                content += "################################################################################################\n"
                content += "WINNER is "+player.name+"\n＼(・ω・＼)"+player.name+"!(/・ω・)/恭喜你!\n"
            print(content)

    # these functions will print the info and call the corresponding method in Player class
    def playerChi(self,player):
        minSet = player.chi()
        content = ""
        content += "################################################################################################\n"
        content += "Player "+player.name+" did 吃 \n"
        content += "Set is "+str(Pai.showHand(minSet))+"\n"
        content += "#################################################################################################\n"
        print(content)
    
    def playerPon(self,player):
        minSet = player.pon()
        content = ""
        content += "################################################################################################\n"
        content += "Player "+player.name+" did PON \n"
        content += "Set is "+str(Pai.showHand(minSet))+"\n"
        content += "#################################################################################################\n"
        print(content)

    def playerKan(self,player):
        minSet = player.kan(self.cutPai)
        content = ""
        content += "################################################################################################\n"
        content += "Player "+player.name+" did KAN \n"
        content += "Set is "+str(Pai.showHand(minSet))+"\n"
        content += "#################################################################################################\n"
        print(content)

    def playerKakan(self,player):
        minSet = player.jiagang()
        content = ""
        content += "################################################################################################\n"
        content += "Player "+player.name+" did JIAKAN \n"
        content += "Set is "+str(Pai.showHand(minSet))+"\n"
        content += "#################################################################################################\n"
        print(content)

    def playerRiichi(self,player):
        player.riichi()
        content = ""
        content += "################################################################################################\n"
        content += "Player "+player.name+" did RIICHI \n"
        content += "#################################################################################################\n"
        print(content)

    # select player with highest priority Min
    def selectMinPlayers(self,minPlayers):
            player = None
            for args in minPlayers:
                if "Kan" in args:
                    player = args
                    break
                elif "Pon" in args:
                    player = args
                    break
                elif "Chi" in args:
                    player = args
                    break
                else:
                    pass
            return player


    # Game modeled by FSM
    def GameFSM(self):

        self.startGame()
        player = self.players[-1]

        while not self.zeroYama():

            # STATE "SET_NEXT_PLAYER"
            if self.state == "SET_PLAYER":
                player = self.players[(self.players.index(player)+1) % 4]
                self.playerCounter[self.players.index(player)] += 1
                print("--------------MAIN PLAYER: ",player.name," | WIND: ",player.wind," | Turn:",int(sum(self.playerCounter))," --------------")
                self.state = "GIVE_PAI"

            # STATE "GIVE_PAI_TO_PLAYER"
            elif self.state == "GIVE_PAI" or self.state == "KAN":
                if self.state == "KAN":
                    self.rinxian = True
                pai = self.yama[0]
                self.yama = self.yama[1:]
                player.givePai(pai)
                # check Tumo
                win, yaku = player.checkTumo()
                if win:
                    self.state = "WIN"
                    self.winner = player
                    self.playerYaku[self.players.index(player)] = yaku
                    self.playerTumo[self.players.index(player)] = True
                    #self.printWinner(player,yaku)
                    break
                self.rinxian = False
                # check Riici
                riichi = player.askRiichi()
                if riichi:
                    self.playerRiichi(player)
                    noMin = self.minCounter.sum() == 0
                    self.riichiTurn[self.players.index(player)] = (self.playerCounter[player],noMin)
                    self.state = "CUT"
                else:
                    jiaGang = player.askJiaGang()
                    if jiaGang:
                        self.cutPai = pai
                        self.state = "KAKAN"
                    else:
                        self.state = "CUT"
            
            # STATE "PLAYER KAKAN"
            elif self.state == "KAKAN":
                self.playerKakan(player)
                # check Ron of other player (槍槓)
                for p in self.players:
                    win, yaku = p.checkRon(self.cutPai)
                    if win:
                        self.state = "WIN"
                        self.winner = p
                        self.playerYaku[self.players.index(p)] = yaku+",槍槓"
                        #self.printWinner(p,yaku)
                if self.state == "WIN":
                    break
                else:
                    self.state = "KAN"

            # STATE "PLAYER_CUT_PAI"
            elif self.state == "CUT" or self.state == "CHI/PON":
                self.printPlayerTurn(player)

                if player.isRiichi:
                    self.cutPai = player.autoCut()
                else:
                    target = int(input("Please SELECT the Pai to CUT\n")) -1
                    self.cutPai = player.cut(target)
                
                # check Ron
                for p in self.players:
                    win, yaku = p.checkRon(self.cutPai)
                    if win:
                        self.state = "WIN"
                        self.winner = p
                        self.playerYaku[self.players.index(p)] = yaku
                        #self.printWinner(p,yaku)
                if self.state == "WIN":
                    break
                self.state = "MIN"
            
            # STATE "PLAYER_MIN"
            elif self.state == "MIN":
                # check the players who want to Min and select player who could Min
                minPlayers = []
                for p in self.players:
                    # player who want to Kan shoule return ("Kan",minSet)
                    # player who do not Min should return (None,None)
                    minType = p.askMin(self.cutPai)
                    if not minType==None:
                        minPlayers.append([p, minType])
                
                if not len(minPlayers) == 0:
                    # select player with highest priority
                    minPlayer = self.selectMinPlayers(minPlayers)
                    self.minCounter[self.players.index(minPlayer[0]),self.players.index(player)] += 1
                    # player change to MinPlayer
                    player = minPlayer[0]

                    if minPlayer[1] == "Kan":
                        self.playerKan(player)
                        self.state = "Kan"

                    elif minPlayer[1] == "Pon":
                        self.playerPon(player)
                        self.state = "CHI/PON"

                    else:
                        self.playerChi(player)
                        self.state = "CHI/PON"
                else:
                    # add cutPai to the player's river
                    player.river.append(self.cutPai)
                    # Go to Next turn
                    self.state = "SET_PLAYER"
            
            # STATE "BLACK_HALL"
            else:
                self.state = "BLACK_HALL"

        # GameEnd
        if not self.state == "WIN":
            print("\n******************************流局******************************\n")
            self.winner = self.checkNagashiMangan()
            if not self.winner == None:
                self.playerYaku[self.players.index(self.winner)] += ",流局満貫"
        else:
            self.checkSpecialYaku(self.players.index(self.winner))
        
        self.printWinner()    
        print("FINISH GAME")
    
    def checkNagashiMangan(self):
        player = None
        for p in self.players:
            if self.allYaoJiu(p.river) and self.noMined(self.players.index(p)):
                player = p
        return player
    
    def allYaoJiu(self,river):
        yaojiu = [0,8,9,17,18,26,27,28,29,30,31,32,33]
        result = True
        for pai in river:
            result = result and (pai in yaojiu)
        return result

    def noMined(self,player):
        return sum(self.minCounter[:,player]) == 0
    
    def checkSpecialYaku(self,p):
        if self.isYifa(p):
            self.playerYaku[p] += ",一發"
        if self.isTianHe(p):
            self.playerYaku[p] += ",天和"
        if self.isDiHe(p):
            self.playerYaku[p] += ",地和"
        if self.isRenHe(p):
            self.playerYaku[p] += ",人和"
        if self.isDoubleRiici(p):
            self.playerYaku[p] += ",双倍立直"
        if self.isHaitei(p):
            self.playerYaku[p] += ",海底撈月"
        if self.isHoTei(p):
            self.playerYaku[p] += ",河底撈魚"
        if self.isRinXiang(p):
            self.playerYaku[p] += ",嶺上開花"

    def isYifa(self, p):
        tumo = self.playerTumo[p] and (self.playerCounter[p]-self.riichiTurn[p][0]) <= 1
        ron = (self.playerCounter[p]-self.riichiTurn[p][0]) < 1
        return tumo or ron

    def isTianHe(self,p):
        isDong = p==0   # is 东家
        isFirstRound = self.playerCounter[p]==1
        tumo = self.playerTumo[p]
        return isDong and isFirstRound and tumo

    def isDiHe(self,p):
        notDong = not p==0
        isFirstRound = self.playerCounter[p]==1
        noMin = self.minCounter.sum() == 0
        tumo = self.playerTumo[p]
        return isDong and isFirstRound and noMin and tumo

    def isRenHe(self,p):
        isFirstRound = self.playerCounter[p]==1
        noMin = self.minCounter.sum() == 0
        ron = not self.playerTumo[p]
        return isDong and isFirstRound and ron

    def isDoubleRiici(self,p):
        isFirstRound = self.riichiTurn[p][0]==1
        wasNoMin = self.riichiTurn[p][1]
        riichi = p.riichi
        return isFirstRound and wasNoMin and riichi

    def isHaitei(self,p):
        tumo = self.playerTumo[p]
        haitei = self.zeroYama()
        return haitei and tumo

    def isHoTei(self,p):
        ron = not self.playerTumo[p]
        haitei = self.zeroYama()
        return haitei and ron

    def isRinXiang(self,p):
        rinxian = self.rinxian
        tumo = self.playerTumo[p]
        return rinxian and tumo

if __name__ == "__main__":
    p1 = Player("Gundam Exia",25000)
    p2 = Player("Gundam Dynames",25000) 
    p3 = Player("Gundam Kyrios",25000)
    p4 = Player("Gundam Virtue",25000)
    game = GameManager([p1,p2,p3,p4])
    game.GameFSM()