import Pai
import numpy as np
from collections import Counter
from functools import reduce
from util import has_sequence, breakdown, has_seq2, has_pair
from JudgeRon import JapanRon

class Player:
    
    def __init__(self,name,score):
        """
        river : [(t,n)] All Pai cut
        
        hand: [(t,n)] t is the index for pai type, n distinguish pai of the same type
        
        openHand: [[(Pai,Int)]] Pai shown on the table because of Min or Riichi. Use 1 for self,
        2 for others, 3 for kakan
        
        draw: Pai the one Pai drawn
        """
        self.name = name
        self.score = score
        self.changfeng = 30 # 東
        self.ifzhuang = False
        self.zifeng = None
        self.isRiichi = False
        
        self.baopai = None
        self.libaopai = None
        self.redbaopai = None
        
        self.river = []
        self.hand = None
        self.draw = None
        self.openHand = {"chi":[], "pon":[], "anKang":[], "minKang":[]}
        self.tenpai = None
        
    # name reference:
    # https://www.wikiwand.com/en/Japanese_Mahjong#/General_mahjong_rules
    # array reference: 
    # 0-8: 一萬 - 九萬
    # 9-17: 一筒 - 九筒
    # 18-26: 一索 - 九索
    # 27，28，29: 中，發，白
    # 30-33: 东西南北
    
# functin for set fields
    def setConnection(self,conn):
        self.conn = conn

    def setHand(self,hand):
        self.hand = hand
        
    def setWind(self,wind):
        self.wind = wind
        if self.wind == "東":
            self.ifzhuang = True
        ref = {"東":30,"西":31,"南":32,"北":33}
        self.zifeng = ref[self.wind]

    def givePai(self,p):
        self.hand.sort()
        self.draw = p
        self.hand.append(p)

# function for get formatted information
    def strOpenHand(self):
        ophand = {}
        for k,msets in self.openHand.items():
            ophand[k] = [Pai.showHand(mset) for mset in msets]
        return str(ophand)

    def getOpenHand(self):
        """
        return list of list of Pai, omit empty list
        """
        r = []
        for _,value in self.openHand.items():
            if value != []:
                r += value
        return r

    def getAllHand(self):
        """
        combine hand and openHand, return sorted list
        """
        all_hand = self.hand[:]
        for sublist in self.getOpenHand():
            all_hand += sublist
        return sorted(all_hand)

# function for cut
    def cut(self, target):
        """
        cut a Pai given the position
        """
        p = self.hand.pop(target)
        return p

    def autoCut(self):
        """
        cut a Pai given
        """
        p = self.hand.pop(-1)
        return p

# function for check 和
    def checkTumo(self,pai):
        """
        return Bool, Ron class
        """
        self.draw = pai
        t = self.checkWait()
        for i,wait in enumerate(t):
            if self.draw[0] in wait:
                self.tumo = True
                self.setRonHand(self.draw,i)
                #self.hand.append(self.draw)
                return True, JapanRon(self)
        return False, None
    
    def checkWait(self):
        """
        [[Int]]
        return a list of list of tenpai
        """
        b = breakdown(self.hand,self.getOpenHand())
        ten = [[] for i in range(len(b))]
        seq2_count = 0
        # find all ten
        for i, possibility in enumerate(b):
            for form in possibility:
                if len(form) == 2:
                    if has_seq2(form):
                        seq2_count += 1
                        a = Pai.previous(form[0]) 
                        if a is not None: ten[i].append(a)
                        b = Pai.next(form[1])
                        if b is not None: ten[i].append(b)
                    if has_pair(form) and seq2_count == 0:
                        ten[i].append(Pai.same(form[0]))
                if len(form) == 1:
                    ten[i].append(Pai.same(form[0]))
        return ten
    
    def setRonHand(self,ronPai,i):
        """
        (int,int) int -> [[(int,int)]]
        i: which form does the ronPai fit
        return breakdown of Ron hand
        """
        b = breakdown(self.hand,self.getOpenHand())
        target_form = b[i][:]
        # 孤张
        for mianzi in target_form:
            if len(mianzi) == 1:
                mianzi.append(ronPai)
                self.ronHand = target_form
                return
            # is_seq
            if len(mianzi) == 2 and has_seq2(mianzi):
                mianzi.append(ronPai)
                mianzi.sort()
                self.ronHand = target_form
                return
            else:
                continue
        # both are pairs
        for mianzi in target_form:
            if len(mianzi) == 2 and has_pair(mianzi):
                if mianzi[0][0] == ronPai[0]:
                    mianzi.append(ronPai)
                    self.ronHand = target_form
                    return 
        
    def checkRon(self,cutPai):
        """
        check hand, openHand and cutPai -> Boolean, Ron Class
        """
        #print("from palyer", cutPai)
        t = self.checkWait()
        for i, wait in enumerate(t):
            if cutPai[0] in wait:
                self.tumo = False
                self.setRonHand(cutPai,i)
                return True, JapanRon(self)
        return False, None
    

# function for ask actions to player
    def askRiichi(self):
        if self.isRiichi:
            return False
        if self.openHand["chi"] or self.openHand["pon"] or self.openHand["minKang"]:
            return False
        cutpais = []
        for pai in self.hand:
            hand = self.hand.copy()
            hand.remove(pai)
            if breakdown(hand,self.getOpenHand()) != [] :
                cutpais.append(pai)

        if cutpais != [] :
            # interaction 
            i = int(input("You can 立直! If you Do not want to 立直 Please press '0'\n Which Pai do you want to cut? (1~) \n"+Pai.showHand(cutpais)+": "))
            if i == 0:
                self.isRiichi = False
            else:
                self.isRiichi = True
                self.riichipai = cutpais[i-1]
            return self.isRiichi

    def askAnKang(self):
        posibleMinset = self.canAnKang()
        #print(posibleMinset)
        if len(posibleMinset)==0:
            return False
        elif len(posibleMinset) == 1:
            ankang = input("Do you want to 暗槓"+Pai.showHand(posibleMinset[0])+"? y/n: ")
            if ankang == "y":
                self.minset = posibleMinset[0]
                print("You selected {}".format(Pai.showHand(self.minset)))
                return True
            else:
                return False
        else:
            ankang = input("Do you want to 暗槓? y/n: ")
            if ankang == "y":
                idx = int(input("Which set do you want to 暗槓? Please input the number(1~) \n"
                                +str([Pai.showHand(minset) for minset in posibleMinset])
                                +": ")) -1
                self.minset = posibleMinset[idx]
                print("You selected {}".format(Pai.showHand(self.minset)))
                return True
            else:
                return False
                
    def canAnKang(self):
        posibility = []
        nums = list(map(lambda t: t[0], self.hand))
        numset = dict(Counter(nums))
        kanPais = [k for k,v in numset.items() if v==4]
        if kanPais != []:
           posibility = [[pai for pai in self.hand if pai[0]==i] for i in kanPais]
        return posibility

    def askJiaGang(self):
        """
        check Player's 加杠 if player can. self.jiaGang donot have to be called.
        Args:
        Return: Boolean
        """
        canjia = self.canjiagang()
        if canjia:
            num = input("Do you want to 加槓? 1:yes/0:no\n")
            if num == "1":
                return True
        return False
    
    def canjiagang(self):
        ponsets = self.openHand["pon"]
        ponnums = [ponset[0][0] for ponset in ponsets]
        if self.draw[0] in ponnums:
            return True
        else:
            return False

    def askMin(self,cutPai):
        if self.isRiichi:
            return None
        chisets = self.canChi(cutPai)
        ponset = self.canPon(cutPai)
        kangset = self.canMinKang(cutPai)
        hasMin = chisets or ponset or kangset
        if hasMin:
            content = self.name + "\n"
            min = reduce(lambda x,y: x+y,[m for m,b in zip(["吃 ","碰 ","槓 "],[chisets,ponset,kangset]) if b])
            content += "You can "+min+"If you Do not want to Min the press 0.\n"
            dontmin = input(content) ==  "0"
        # put hasMin to first not to evaluate dontmin if hasMin is False
        if hasMin and dontmin:
            return None
        else:
            if kangset:
                kaned = self.askMinKang(kangset)
                if kaned: return "Kan"
            if ponset:
                poned = self.askPon(ponset)
                if poned: return "Pon"
            if chisets:
                chied = self.askChi(chisets)
                if chied: return "Chi"
            return None

    def canChi(self,cutPai):
        posibility = []
        i, n = cutPai
        isnumpai = i in list(range(27))
        numhand = [p[0] for p in self.hand]+[i]
        if i in [0,9,18]:
            pattern = [i,i+1,i+2]
            exist = all([pai in numhand for pai in pattern])
            if exist:
                snd = self.hand[numhand.index(i+1)]
                third = self.hand[numhand.index(i+2)]
                posibility = [[cutPai,snd,third]]
        elif i in [8,17,26]:
            pattern = [[i-2,i-1,i]]
            exist = all([pai in numhand for pai in pattern])
            if exist:
                fst = self.hand[numhand.index(i-2)]
                snd = self.hand[numhand.index(i-1)]
                posibility = [[fst,snd,cutPai]]
        elif isnumpai:
            patterns = [[i,i+1,i+2],[i-1,i,i+1],[i-2,i-1,i]]
            exists = [all([pai in numhand for pai in pattern]) for pattern in patterns]
            chisets = [pattern for i,pattern in enumerate(patterns) if exists[i]]
            hand = self.hand + [cutPai]
            if chisets:
                for pattern in chisets:
                    fst = hand[numhand.index(pattern[0])]
                    snd = hand[numhand.index(pattern[1])]
                    third = hand[numhand.index(pattern[2])]
                    posibility.append([fst,snd,third])
        else:
            pass

        return posibility

    def canPon(self,cutPai):
        posibility = []
        nums = list(map(lambda t: t[0], self.hand))
        numset = dict(Counter(nums))
        ponPais = [k for k,v in numset.items() if v==2 and k==cutPai[0]]
        if ponPais:
           posibility = [pai for pai in self.hand if pai[0]==cutPai[0]] + [cutPai]
        return posibility

    def canMinKang(self,cutPai):
        posibility = []
        nums = list(map(lambda t: t[0], self.hand))
        numset = dict(Counter(nums))
        kanPais = [k for k,v in numset.items() if v==3 and k==cutPai[0]]
        if kanPais:
           posibility = [pai for pai in self.hand if pai[0]==cutPai[0]] + [cutPai]
        return posibility
    
    def askChi(self,posibleMinset):
        minchi = input("Do you want to 吃? y/n: ")
        if minchi ==  "y":
            chi_prompt = "Select from: \n"
            for i, option in enumerate(posibleMinset):
                chi_prompt += "{}. {} ".format(i+1, Pai.showHand(option))
            select = input(chi_prompt)
            print("You selected {}".format(Pai.showHand(posibleMinset[int(select)-1])))
            self.minset = posibleMinset[int(select)-1]
            return True
        else:
            self.minset = []
            return False

    def askPon(self,posibleMinset):
        minpon = input("Do you want to 碰"+Pai.showHand(posibleMinset)+"? y/n: ")
        if minpon == "y":
            self.minset = posibleMinset
            return True
        else:
            self.minset = []
            return False

    def askMinKang(self,posibleMinset):
        #print(posibleMinset)
        if len(posibleMinset)==0:
            return False
        else:
            minkang = input("Do you want to 槓"+Pai.showHand(posibleMinset)+"? y/n: ")
            if minkang == "y":
                self.minset = posibleMinset
                return True
            else:
                return False

# function for execute actions

    def jiagang(self,cutpai):
        jiaPai = self.hand.pop(-1)
        ponset = [ponset for ponset in self.openHand["pon"] if ponset[0][0]==jiaPai[0]][0]
        self.openHand["pon"].remove(ponset)
        ponset.append(jiaPai)
        self.openHand["minKang"].append(ponset)
        return ponset

    def chi(self,paiCut):
        self.openHand["chi"].append(self.minset)
        self.minset.remove(paiCut)
        for pai in self.minset:
            self.hand.remove(pai)
        self.minset.append(paiCut)
        return self.minset
            
    def pon(self,paiCut):
        self.openHand['pon'].append(self.minset)
        self.minset.remove(paiCut)
        for pai in self.minset:
            self.hand.remove(pai)
        self.minset.append(paiCut)
        return self.minset
    
    def kan(self,cutpai,anKang=False):
        #print(self.hand)
        #print(self.minset)
        if anKang:
            for pai in self.minset:
                self.hand.remove(pai)
            self.openHand["anKang"].append(self.minset)
        else:
            self.openHand["minKang"].append(self.minset)
            self.minset.remove(cutpai)
            for pai in self.minset:
                self.hand.remove(pai)
            self.minset.append(cutpai)
        return self.minset

    def riichi(self):
        self.hand.remove(self.riichipai)
        self.hand.append(self.riichipai)

    
if __name__ == '__main__':
    import doctest