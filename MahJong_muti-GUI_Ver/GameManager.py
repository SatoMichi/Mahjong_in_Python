import Pai
from Player import Player
import numpy as np
import socket
import logging
import json

# this class is Finite State Machine
class GameManager:
    # prepared all the Pai and 4 players
    def __init__(self,players):
        #logging.basicConfig(handlers=[logging.FileHandler("gamelog.log",'w','utf-8')], level=logging.DEBUG)
        self.players = []
        # add players
        for p in players:
            self.players.append(p)
        # set idx to each player
        for i in range(self.players):
            self.players[i].setIdx(i)
        # set yama
        self.yama = Pai.originalYama
    
    # convert game state to dict
    def state2dict(self):
        state = {}
        state["who"] = None
        state["mainPlayer"] = self.player.idx
        winner = self.winner.idx if self.winner else None
        state["winner"] = winner
        state["type"] = None
        state["action"] = self.state
        state["baopai"] = self.baopai
        state["cutPai"] = self.cutPai
        state["players"] = []
        for p in self.players:
            pstate = p.state2dict()
            state["players"].append(pstate)
        state["print"] = ""
        return state

    # set sockets connection to each player
    def setSockets(self):
        # create sockets
        self.sockets = []
        for i in range(len(self.players)):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sockets.append(s)
        # IP address
        localhost = "127.0.0.1"
        # Enable Port numbers
        self.ports = [50000,50001,50002,50003]
        # bind sockets
        for i in range(len(self.players)):
            self.sockets[i].bind((localhost,self.ports[i]))
        # only accept one connection for each sockets
        for i in range(len(self.players)):
            self.sockets[i].listen(1)
        # accept clients
        self.conns = []
        self.addrs = []
        for i in range(len(self.players)):
            conn,addr = self.sockets[i].accept()
            self.conns.append(conn)
            self.addrs.append(addr)
            #logging.info(addr," Accepted\n")
        # connect connection with players
        for i in range(len(self.players)):
            self.players[i].setConnection(self.conns[i])
    
    # give 13 pai to each players
    def startGame(self):
        self.players[0].iszhuang = True
        self.baopaiCount = -1
        self.baopai = [self.yama[self.baopaiCount]]
        self.baopaiCount -= 1
        self.libaopai = [self.yama[self.baopaiCount]]
        self.baopaiCount -= 1
        self.redbaopai = [(4,0),(13,0),(13,1),(22,0)]
        for wind, player in zip(["東","南","西","北"], self.players):
            hand = self.yama[:13]
            self.yama = self.yama[13:]
            # call player's method
            player.setWind(wind)
            # player.setHand(hand)
            player.setHand([(p,0) for p in Pai.parsedPai("222444m333555s2p")])
            player.baopai = self.baopai
            player.libaopai = self.libaopai
            player.redbaopai = self.redbaopai
        
        self.cutPai = None
        self.state = "SET_PLAYER"
        self.winner = None
        self.playerCounter = np.zeros([4])
        self.minCounter = np.zeros([4,4])
        self.riichiTurn = [(0,False)]*4
        self.playerTumo = [False,False,False,False]
        self.playerYaku = [""]*4
        self.rinxian = False

        self.player = self.players[-1]

        #self.printEveryOne("Prepared\nLet's Start the GAME !!\n")

    # check yama is empty or not
    def zeroYama(self):
        if len(self.yama) <= 14:
            return True
        return False

    # (CUI only) print the String to this CommandLine and each Clients
    def printEveryOne(self,s):
        logging.info(s)
        for i in range(len(self.players)):
            self.conns[i].sendall(s.encode("utf-8"))
    
    # (GUI only) send game state to each Clients
    def sendEveryOne(self,s):
        state = self.state2dict()
        state["type"] = "print"
        state["print"] = s
        for i in range(len(self.players)):
            state["who"] = i
            data = json.dumps(state)
            self.conns[i].sendall(data.encode("utf-8"))

    # (GUI only) send game state to specific player
    def sendPlayer(self,player,s,require):
        state = self.state2dict()
        state["type"] = require
        state["print"] = s
        state["who"] = player.idx
        data = json.dumps(state)
        player.conns.sendall(data.encode("utf-8"))

    # (CUI only) show information for player playing his turn   
    def printPlayerTurn(self,player):
        content = ""
        content += "宝牌: "+Pai.showHand(self.baopai)+"\n"
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
        return content

    # send winner's information to every player
    def printWinner(self):
        if self.winner == None:
            self.sendEveryOne("NO ONE WIN\n")
        else:
            player = self.winner
            yaku = self.playerYaku[player.idx]
            content = ""
            content += "Player "+player.name+" Win!!\n"
            content += "Scores: "+str(player.score)+"\n"
            content += "役: "+yaku.judgeRon+"\n"
            player.hand.sort()
            player.hand.append(self.lastPai)
            content += str(Pai.showHand(player.hand))+"\n"
            content += "\n＼(・ω・＼)"+player.name+"!(/・ω・)/恭喜你!\n"
        self.sendEveryOne(content)

    # send cut info to every player
    def playerCutPai(self,player):
        content = ""
        content += "Player "+player.name+" cut "+str(Pai.paiSet[self.cutPai])+"\n"
        self.sendEveryOne(content)

    # these functions will print the info to every player
    # and call the corresponding method in Player class
    def playerChi(self,player):
        minSet = player.chi()
        content = ""
        content += "Player "+player.name+" did 吃 \n"
        content += "Set is "+str(Pai.showHand(minSet))+"\n"
        self.sendEveryOne(content)
    
    def playerPon(self,player):
        minSet = player.pon()
        content = ""
        content += "Player "+player.name+" did PON \n"
        content += "Set is "+str(Pai.showHand(minSet))+"\n"
        self.sendEveryOne(content)

    def playerKan(self,player):
        minSet = player.kan(self.cutPai)
        self.baopai.append(self.yama[self.baopaiCount])
        self.baopaiCount -= 1
        self.libaopai.append(self.yama[self.baopaiCount])
        self.baopaiCount -= 1
        for p in self.players:
            p.baopai = self.baopai
            p.libaopai = self.libaopai
        content = ""
        content += "Player "+player.name+" did KAN \n"
        content += "Set is "+str(Pai.showHand(minSet))+"\n"
        self.sendEveryOne(content)

    def playerKakan(self,player):
        minSet = player.jiagang()
        self.baopai.append(self.yama[self.baopaiCount])
        self.baopaiCount -= 1
        self.libaopai.append(self.yama[self.baopaiCount])
        self.baopaiCount -= 1
        for p in self.players:
            p.baopai = self.baopai
            p.libaopai = self.libaopai
        content = ""
        content += "Player "+player.name+" did JIAKAN \n"
        content += "Set is "+str(Pai.showHand(minSet))+"\n"
        self.sendEveryOne(content)

    def playerRiichi(self,player):
        player.riichi()
        content = ""
        content += "Player "+player.name+" did RIICHI \n"
        self.sendEveryOne(content)

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
        self.setSockets()
        self.startGame()
        
        while not self.zeroYama() and len(self.baopai)<5:

            # STATE "SET_NEXT_PLAYER"
            if self.state == "SET_PLAYER":
                self.player = self.players[(self.player.idx+1) % 4]
                self.playerCounter[self.player.idx] += 1
                self.sendEveryOne("MAIN PLAYER: "+self.player.name+" | WIND: "+self.player.wind+" | Turn:"+str(int(sum(self.playerCounter))))
                self.state = "GIVE_PAI"

            # STATE "GIVE_PAI_TO_PLAYER"
            elif self.state == "GIVE_PAI" or self.state == "KAN":
                if self.state == "KAN":
                    self.rinxian = True
                pai = self.yama[0]
                self.yama = self.yama[1:]
                self.player.givePai(pai)
                # check Tumo
                win, yaku = self.player.checkTumo()
                if win:
                    self.state = "WIN"
                    self.winner = self.player
                    self.playerYaku[self.player.idx] = yaku
                    self.playerTumo[self.player.idx] = True
                    self.lastPai = pai
                    break
                self.rinxian = False
                # check Riici
                riichi = self.player.askRiichi()
                if riichi:
                    self.playerRiichi(self.player)
                    noMin = self.minCounter.sum() == 0
                    self.riichiTurn[self.player.idx] = (self.playerCounter[self.player.idx],noMin)
                    self.state = "CUT"
                else:
                    jiaGang = self.player.askJiaGang()
                    if jiaGang:
                        self.cutPai = pai
                        self.state = "KAKAN"
                    else:
                        self.state = "CUT"
            
            # STATE "PLAYER KAKAN"
            elif self.state == "KAKAN":
                self.playerKakan(self.player)
                # check Ron of other player (槍槓)
                for p in self.players:
                    if p == self.player:
                        continue 
                    win, yaku = p.checkRon(self.cutPai)
                    if win:
                        self.state = "WIN"
                        self.winner = p
                        yaku.setJudgeRon("槍槓")
                        yaku.addfan(1)
                        self.playerYaku[p.idx] = yaku
                        self.lastPai = self.cutPai
                if self.state == "WIN":
                    break
                else:
                    self.state = "KAN"

            # STATE "PLAYER_CUT_PAI"
            elif self.state == "CUT" or self.state == "CHI/PON":
                # send current information to every player 
                self.sendEveryOne("")
                #logging.info(self.printPlayerTurn(player))

                if self.player.isRiichi:
                    self.cutPai = self.player.autoCut()
                else:
                    self.sendPlayer(self.player,"Please SELECT the Pai to CUT\n","input")
                    target = int(self.player.conn.recv(1024).decode("utf-8")) -1
                    self.cutPai = self.player.cut(target)
                # print cut info
                self.playerCutPai(self.player)

                # check Ron
                for p in self.players:
                    if p == self.player:
                        continue
                    win, yaku = p.checkRon(self.cutPai)
                    #print(win,self.cutPai,p.hand)
                    if win:
                        self.state = "WIN"
                        self.winner = p
                        self.playerYaku[p.idx] = yaku
                        self.lastPai = self.cutPai
                if self.state == "WIN":
                    #print("breaking")
                    break
                self.state = "MIN"
            
            # STATE "PLAYER_MIN"
            elif self.state == "MIN":
                # check the players who want to Min and select player who could Min
                minPlayers = []
                for p in self.players:
                    # player who want to Kan shoule return ("Kan",minSet)
                    # player who do not Min should return (None,None)
                    if p == self.player:
                        continue
                    minType = p.askMin(self.cutPai)
                    if not minType==None:
                        minPlayers.append([p, minType])
                
                if not len(minPlayers) == 0:
                    # select player with highest priority
                    minPlayer = self.selectMinPlayers(minPlayers)
                    self.minCounter[minPlayer[0].idx,self.player.idx] += 1
                    # player change to MinPlayer
                    self.player = minPlayer[0]

                    if minPlayer[1] == "Kan":
                        self.playerKan(self.player)
                        self.state = "Kan"

                    elif minPlayer[1] == "Pon":
                        self.playerPon(self.player)
                        self.state = "CHI/PON"

                    else:
                        self.playerChi(self.player)
                        self.state = "CHI/PON"
                else:
                    # add cutPai to the player's river
                    self.player.river.append(self.cutPai)
                    # Go to Next turn
                    self.state = "SET_PLAYER"
            
            # STATE "BLACK_HALL"
            else:
                self.state = "BLACK_HALL"

        # GameEnd
        if not self.state == "WIN":
            self.sendEveryOne("流局\n")
            self.winner = self.checkNagashiMangan()
            if self.winner:
                ronInfo = self.playerYaku[self.winner.idx]
                ronInfo.setJudgeRon(",流局満貫")
                ronInfo.addfan(5)
                ronInfo.setallup()
        else:
            self.checkSpecialYaku(self.winner.idx)
        # move score to the winner
        if self.state == "WIN" and self.winner.idx == 0:
            # winner is EAST
            ronInfo = self.playerYaku[self.winner.idx]
            self.winner.score += ronInfo.zj
            for i in range(1,4):
                self.players[i].score -= ronInfo.xj
        elif self.state == "WIN":
            # winner is Not EAST
            ronInfo = self.playerYaku[self.winner.idx]
            self.winner.score += ronInfo.zj
            for i in range(4):
                if i == 0:
                    self.players[i].score -= ronInfo.dj
                elif i == self.winner.idx:
                    continue
                else:
                    self.players[i].score -= ronInfo.xj
        else:
            pass

        self.printWinner()    
        self.sendEveryOne("FINISH GAME")

        # close each socket
        for i in range(len(self.players)):
            self.sockets[i].close()
    
    # check "流し満貫"
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
    
    # these functions are for checking special score
    def checkSpecialYaku(self,p):
        ronInfo = self.playerYaku[p]
        if self.isYifa(p):
            ronInfo.setJudgeRon("一發")
            ronInfo.addfan(1)
        if self.isTianHe(p):
            ronInfo.setJudgeRon("天和")
            ronInfo.addfan(7)
        if self.isDiHe(p):
            ronInfo.setJudgeRon("地和")
            ronInfo.addfan(7)
        if self.isRenHe(p):
            ronInfo.setJudgeRon("人和")
            ronInfo.addfan(7)
        if self.isDoubleRiici(p):
            ronInfo.setJudgeRon("双倍立直")
            ronInfo.addfan(2)
        if self.isHaitei(p):
            ronInfo.setJudgeRon("海底撈月")
            ronInfo.addfan(1)
        if self.isHoTei(p):
            ronInfo.setJudgeRon("河底撈魚")
            ronInfo.addfan(1)
        if self.isRinXiang(p):
            ronInfo.setJudgeRon("嶺上開花")
            ronInfo.addfan(1)
        ronInfo.setallup()

    def isYifa(self, p):
        isRiichi = self.winner.isRiichi
        tumo = self.playerTumo[p] and (self.playerCounter[p]-self.riichiTurn[p][0]) <= 1
        ron = (self.playerCounter[p]-self.riichiTurn[p][0]) < 1
        return isRiichi and (tumo or ron)

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
        return notDong and isFirstRound and noMin and tumo

    def isRenHe(self,p):
        isFirstRound = self.playerCounter[p]==0
        noMin = self.minCounter.sum() == 0
        ron = not self.playerTumo[p]
        return isFirstRound and noMin and ron

    def isDoubleRiici(self,p):
        isFirstRound = self.riichiTurn[p][0]==1
        wasNoMin = self.riichiTurn[p][1]
        riichi = self.winner.isRiichi
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