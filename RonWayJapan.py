import yaml
import math
from JudgeRon import pai2onlyno,chitoi,pinghe

def calcultatefu(hand,openHand,beforeHand,tumo,hepai,zifeng,changfeng):
    yaojiu = [0,8,9,17,18,26,27,28,29,30,31,32,33]
    sanyuan = [27,28,29]
    #符底一定会有二十符
    fu = 20
    hand_no = pai2onlyno(hand)
    openHand_no = pai2onlyno(openHand)
    for oph in openHand_no:
        if(len(oph)==4):
            if(oph[2]==oph[3]):
                if(oph[0] in yaojiu):
                    fu = fu + 16
                else:
                    fu = fu + 8
            else:
                if(oph[0] in yaojiu):
                    fu = fu + 32
                else:
                    fu = fu + 16
        if(len(oph)==3 and oph[0]==oph[1] and oph[1]==oph[2]):
            if(oph[0] in yaojiu):
                fu = fu + 4
            else:
                fu = fu + 2
    for hand in hand_no:
        if(len(hand)==3):
            if(hand[0]==hand[1] and hand[1]==hand[2]):
                if(hand[0] in yaojiu):
                    fu = fu + 8
                else:
                    fu = fu + 4
        if(len(hand)==2):
            if(hand[0] in sanyuan):
                fu = fu + 2
            if(hand[0] == zifeng or hand[0] == changfeng):
                fu = fu + 2
                if(zifeng == changfeng):
                    fu = fu + 2
    #自摸加2两符,七对子不加
    if(tumo):
        if(not chitoi(hand)):
            fu = fu + 2
    #门前荣和加10符
    if(not tumo):
        if(openHand == None):
            fu = fu + 10
    #单钓听牌加2符
    if(1 in [len(bH) for bH in beforeHand]):
        fu = fu + 2
    else:
        pentyan = [[0,1],[7,8],[9,10],[16,17],[18,19],[25,26]]
        shunzi = takeShunzi([paiset for paiset in beforeHand if len(paiset)==2])
        #边张加2符
        if([pai[0] for pai in shunzi[0]] in pentyan):
            fu = fu + 2
        #嵌张加2符
        elif(sum([pai[0] for pai in shunzi[0]])%2==0):
            fu = fu + 2
    fus = fu / 10
    fus = math.ceil(fus)
    fu = fus * 10
    #七对子的符数一定是25符
    if(chitoi(hand)):
        fu = 25
    #平和自摸的牌一定是20符
    if(pinghe(beforeHand,hand,hepai,zifeng,changfeng) and tumo):
        fu = 20
    return fu

def takeShunzi(paisets):
        paisetsCopy = paisets.copy()
        for paiset in paisets:
            if paiset[0][0] == paiset[1][0]:
                paisetsCopy.remove(paiset)
        return paisetsCopy

class Rondong:
    def __init__(self):
        self.zj = 0     #自家得到的分数
        self.xj = 0     #闲家得到的分数
        self.judgeRon = ""      #和牌包含的役
        self.fan = 0    #和牌的翻数
        self.fu = 0     #和牌的符数
        self.levelrep = ""  #和牌的翻数 string形式
    def addfan(self,n):
        self.fan = self.fan + n
    def setJudgeRon(self,stri):
        self.judgeRon = self.judgeRon + " " + stri
    #为了应对因为副露而出现的减番情况
    def minusfan(self):
        self.fan = self.fan - 1
    def calcultateFu(self,hand,openHand,beforeHand,tumo,hepai,zifeng,changfeng):
        self.fu = calcultatefu(hand,openHand,beforeHand,tumo,hepai,zifeng,changfeng)
    def setallup(self):
        file = open("roncalculatedong.yml",'r',encoding="utf-8")
        file_data = file.read()
        file.close()
        data = yaml.load(file_data,Loader=yaml.FullLoader)
        if(self.fan == 5 or (self.fan == 4 and self.fu>30) or (self.fan == 3 and self.fu>60)):
            self.zj = 12000
            self.xj = 4000
            self.levelrep = "满贯"
        elif(self.fan == 6 or self.fan == 7):
            self.zj = 18000
            self.xj = 6000
            self.levelrep = "跳满" 
        elif(self.fan == 8 or self.fan == 9 or self.fan == 10):
            self.zj = 24000
            self.xj = 8000
            self.levelrep = "倍满"
        elif(self.fan == 11 or self.fan == 12):
            self.zj = 36000
            self.xj = 12000
            self.levelrep = "三倍满"
        #累计役满即为Player单次所能获得的最大的牌
        elif(self.fan >= 13):
            self.zj = 48000
            self.xj = 16000
            self.levelrep = "累计役满"
        else:
            fanshu = 'fanshu' + str(self.fan)
            fushu = 'fushu' + str(self.fu)
            self.zj = data['point'][0][fanshu][0][fushu][0]['defen']
            self.xj = data['point'][0][fanshu][0][fushu][0]['shifen']
            self.levelrep = str(self.fan) + "翻"

class Ronxian:
    def __init__(self):
        self.zj = 0     #自家得到的分数
        self.dj = 0     #东家丢失的分数
        self.xj = 0     #闲家丢失的分数
        self.judgeRon = ""      #和牌中包含的役
        self.fan = 0    #和牌的番数
        self.fu = 0     #和牌的符数
        self.levelrep = ""      #和牌的翻数 string形式
    def addfan(self,n):
        self.fan = self.fan + n
    def setJudgeRon(self,stri):
        self.judgeRon = self.judgeRon + " " + stri
    #为了应对因为副露而出现的减番情况
    def minusfan(self):
        self.fan = self.fan - 1
    def calcultateFu(self,hand,openHand,beforeHand,tumo,hepai,zifeng,changfeng):
        self.fu = calcultatefu(hand,openHand,beforeHand,tumo,hepai,zifeng,changfeng)
    def setallup(self):
        file = open("roncalculatedong.yml",'r',encoding="utf-8")
        file_data = file.read()
        file.close()
        data = yaml.load(file_data,Loader=yaml.FullLoader)
        if(self.fan == 5 or (self.fan == 4 and self.fu>30) or (self.fan == 3 and self.fu>60)):
            self.zj = 8000
            self.xj = 2000
            self.dj = 4000
            self.levelrep = "满贯"
        elif(self.fan == 6 or self.fan == 7):
            self.zj = 12000
            self.xj = 3000
            self.dj = 6000
            self.levelrep = "跳满" 
        elif(self.fan == 8 or self.fan == 9 or self.fan == 10):
            self.zj = 16000
            self.xj = 4000
            self.dj = 8000
            self.levelrep = "倍满"
        elif(self.fan == 11 or self.fan == 12):
            self.zj = 24000
            self.xj = 6000
            self.dj = 12000
            self.levelrep = "三倍满"
        elif(self.fan >= 13):
            self.zj = 32000
            self.xj = 8000
            self.dj = 16000
            self.levelrep = "累计役满"
        else:
            fanshu = 'fanshu' + str(self.fan)
            fushu = 'fushu' + str(self.fu)
            self.zj = data['point'][0][fanshu][0][fushu][0]['defen']
            self.dj = data['point'][0][fanshu][0][fushu][0]['dongshifen']
            self.xj =  data['point'][0][fanshu][0][fushu][0]['xianshifen']
            self.levelrep = str(self.fan) + "翻"