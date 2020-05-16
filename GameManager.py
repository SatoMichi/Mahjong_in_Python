import Pai

# this class is Finite State Machine
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
            # call player's method
            player.giveHand(hand)
        self.cutPai = None
        self.state = "SET_PLAYER"
        print("Prepared")

    # check yama is empty or not
    def zeroYama():
        if len(self.yama) <= 0:
            return True
        return False

    # show information for player playing his turn   
    def printPlayerTurn(player):
        content += ""
        # print each players River (already cut Pais)
        for p in self.players:
            # player.river is Pais player already cut
            content += "Player "+p.name+"'s River is "+Pai.showHand(p.cut)+"\n"
        for p in self.players:
            # player.min is player's min Pai already got
            if p == player:
                content += "----------------------------------------------------\n"
                content += "Main Player :"+player.name+"\n"
                content += "Min Pai :"+Pai.showHand(Pai.array2Hand(player.openHand))+"\n"
                content += "Player's Hand: "+Pai.showHand(Pai.array2Hand(player.hand))+"\n"
                content += "----------------------------------------------------\n"
                continue
            content += "Player "+p.name+"'s Hand is "+"SECRET"+"\n"
            content += "Player "+p.name+"'s Min Pai is "+Pai.showHand(Pai.array2Hand(p.openHand))+"\n"
        print(content)

    # set state, cutPai and nextPlayer
    def playerCutPai(player, cutPai):
        self.cutPai = cutPai
        content += "Player "+player.name+" cut "+str(self.cutPai)+"\n"
        print(content)


    # print winner's information
    def printWinner(player,yaku):
        content = ""
        content += "###############################################################################################\n"
        content += "Player "+player.name+" Win!!\n"
        content += "Points: "+str(player.score)+"\n"
        content += "役: "+yaku+"\n"
        player.hand.sort()
        content += str(Pai.showHand(Pai.array2Hand(player.hand)))+"\n"
        content += "################################################################################################\n"
        content += "WINNER is "+player.name+"\n＼(・ω・＼)"+player.name+"!(/・ω・)/恭喜你!"
        print(content)


    # these functions will print the info and call the corresponding method in Player class
    def playerChi(player):
        minSet = player.chi()
        content = ""
        content += "################################################################################################\n"
        content += "Player "+player.name+" did 吃 \n"
        content += "Set is "+str(Pai.showHand(minSet))+"\n"
        content += "#################################################################################################\n"
        print(content)
    
    def playerPon(player):
        minSet = player.pon()
        content = ""
        content += "################################################################################################\n"
        content += "Player "+player.name+" did PON \n"
        content += "Set is "+str(Pai.showHand(minSet))+"\n"
        content += "#################################################################################################\n"
        print(content)

    def playerKan(player):
        minSet = player.kan()
        content = ""
        content += "################################################################################################\n"
        content += "Player "+player.name+" did KAN \n"
        content += "Set is "+str(Pai.showHand(minSet))+"\n"
        content += "#################################################################################################\n"
        print(content)

    # select player with highest priority Min
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


    # Game modeled by FSM
    def GameFSM():

        self.startGame()
        player = self.players[-1]

        while not self.zeroYama():

            # STATE "SET_NEXT_PLAYER"
            if self.state == "SET_PLAYER":
                player = self.players[(self.players.index(player)+1) % 4]
                print("----------------------MAIN PLAYER: ",player.name,"----------------------")
                self.state = "GIVE_PAI"

            # STATE "GIVE_PAI_TO_PLAYER"
            else if self.state == "GIVE_PAI" or self.state == "KAN":
                pai = self.yama[0]
                self.yama = self.yama[1:]
                player.givePai(pai)
                # check Tumo
                win, yaku = player.checkTumo()
                if win:
                    self.state = "WIN"
                    self.printWinner(player,yaku)
                    break
                self.state = "CUT"

            # STATE "PLAYER_CUT_PAI"
            else if self.state == "CUT" or self.state == "CHI/PON"
                self.printPlayerTurn(player)

                cut = player.cut()
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
            else if self.state == "MIN":
                # check the players who want to Min and select player who could Min
                minPlayers = []
                for p in self.players:
                    # player who want to Kan shoule return ("Kan",minSet)
                    # player who do not Min should return (None,None)
                    minType, minSet = p.askMin()
                    minPlayers.append([p, minType, minSet])
                
                if not len(minPlayers) == 0:
                    # select player with highest priority
                    minPlayer = self.selectMinPlayers(minPlayers)
                    # player change to MinPlayer
                    player = minPlayer[0]

                    if minPlayer[1] == "Kan":
                        self.playerKan(player)
                        self.state = "Kan"

                    else if minPlayer[1] == "Pon":
                        self.playerPon(player)
                        self.state = "CHI/PON"

                    else:
                        self.playerChi(player)
                        self.state = "CHI/PON"
                else:
                    # add cutPai to the player's river
                    player.cut.append(self.cutPai)
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

