import Pai
from TestPlayer import Player

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
    def printWinner(self,player,yaku):
        content = ""
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
        minSet = player.kan()
        content = ""
        content += "################################################################################################\n"
        content += "Player "+player.name+" did KAN \n"
        content += "Set is "+str(Pai.showHand(minSet))+"\n"
        content += "#################################################################################################\n"
        print(content)

    def printRiichi(self,player):
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
                print("----------------------MAIN PLAYER: ",player.name," | WIND: ",player.wind,"----------------------")
                self.state = "GIVE_PAI"

            # STATE "GIVE_PAI_TO_PLAYER"
            elif self.state == "GIVE_PAI" or self.state == "KAN":
                pai = self.yama[0]
                self.yama = self.yama[1:]
                player.givePai(pai)
                # check Tumo
                win, yaku = player.checkTumo()
                if win:
                    self.state = "WIN"
                    self.printWinner(player,yaku)
                    break
                # check Riici
                riichi = player.askRiichi()
                if riichi:
                    self.printRiichi(player)
                self.state = "CUT"

            # STATE "PLAYER_CUT_PAI"
            elif self.state == "CUT" or self.state == "CHI/PON":
                self.printPlayerTurn(player)

                if player.riichi:
                    cut = player.autoCut()
                else:
                    target = int(input("Please SELECT the Pai to CUT\n")) -1
                    cut = player.cut(target)
                
                self.playerCutPai(player,cut)
                
                # check Ron
                for p in self.players:
                    win, yaku = p.checkRon()
                    if win:
                        self.state = "WIN"
                        self.printWinner(p,yaku)
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
                    minType, minSet = p.askMin()
                    if not minType==None:
                        minPlayers.append([p, minType, minSet])
                
                if not len(minPlayers) == 0:
                    # select player with highest priority
                    minPlayer = self.selectMinPlayers(minPlayers)
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
            print("***************************流局***************************")
        else:
            print("FINISH GAME")


    """
    def mainGame():
        # prepare game
        self.startGame()
        
        # check whether yama is empty or not and winner exist or not
        while (not self.zeroYama()) and (not self.winner):
            
            # STATE SET_PLAYER
            if self.state == "SET_PLAYER":
                player = self.players[self.nextPlayer]
                print("----------------------MAIN PLAYER: ",player.name,"----------------------")
                self.state = "GIVE_PAI"
            
            # STATE GIVE_PAI
            if self.state == "GIVE_PAI" or self.state == "KAN":
                pai = self.yama[0]
                self.yama = self.yama[1:]
                player.givePai(pai)
                # check Tumo
                win, yaku = player.checkTumo()
                if win:
                    self.state = "WIN"
                    self.winner = player
                    self.printWinner(player,yaku)
                    break
                self.printPlayerTurn(player, pai)
                self.state = "CUT/MIN"
            
            # show info and get cut pai from player
            self.printPlayerTurn(player, pai)
            
            # STATE CUT/MIN
            if self.state == "CUT/MIN" or self.state == "CHI/PON"
                cut = player.cut()
                self.playerCutPai(player,cut)
                
                # check Ron
                for p in self.players:
                    win, yaku = p.checkRon()
                    if win:
                        self.state = "WIN"
                        self.winner = p
                        self.printWinner(p,yaku)
                if self.state == "WIN":
                    break

                # check the players who want to Min and select player who could Min
                minPlayers = []
                for p in self.players:
                    # player who want to Min have to declear in this stage
                    # player who want to Kan shoule return ("Kan",minSet)
                    # player who do not Min should return (None,None)
                    minType, minSet = p.askMin()
                    minPlayers.append([p, minType, minSet])
                
                # select player with highest priority
                if not len(minPlayers) == 0:
                    # player change to MinPlayer
                    minPlayer = self.selectMinPlayers(minPlayers)
                    player = minPlayer[0]
                    if minPlayer[1] == "Kan":
                        self.playerKan(minPlayer)
                        continue
                    else:
                        self.playerChiPon(minPlayer)
                        continue
            
            # STATE NEXT_TURN
            self.state = "SET_PLAYER"
            print("To Next Turn >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        # GameEnd
        if self.winner == None:
            print("***************************流局***************************")
        else:
            pass
    """

if __name__ == "__main__":
    p1 = Player("Gundam Exia",25000)
    p2 = Player("Gundam Dynames",25000) 
    p3 = Player("Gundam Kyrios",25000)
    p4 = Player("Gundam Virtue",25000)
    game = GameManager([p1,p2,p3,p4])
    game.GameFSM()