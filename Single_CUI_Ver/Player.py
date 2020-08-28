import Pai
import numpy as np
from collections import Counter
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
        self.changfeng = None
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

    def strOpenHand(self):
        ophand = {}
        for k,msets in self.openHand.items():
            ophand[k] = [Pai.showHand(mset) for mset in msets]
        return str(ophand)

    def givePai(self,p):
        self.hand.sort()
        self.draw = p
        self.hand.append(p)
        
    def cut(self, target):
        """
        cut a Pai given the position
        """
        p = self.hand.pop(target)
        return p

    def checkTumo(self):
        """
        return Bool, Ron class
        """
        t = self.checkWait()
        for i,wait in enumerate(t):
            if self.draw[0] in wait:
                self.tumo = True
                self.setRonHand(self.draw,i)
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

    
    def askAnKang(self):
        posibleMinset = self.canAnKang()
        #print(posibleMinset)
        if len(posibleMinset)==0:
            return False
        elif len(posibleMinset) == 1:
            ankang = input("Do you want to 暗槓"+Pai.showHand(posibleMinset[0])+"? y/n: ")
            if ankang == "y":
                self.minset = posibleMinset[0]
                return True
            else:
                return False
        else:
            ankang = input("Do you want to 暗槓? y/n: ")
            if ankang == "y":
                idx = int(input("Which set do you want to 暗槓? Please input the number(1~) \n"
                                +str([Pai.showHand(minset)+"\n" for minset in posibleMinset]))) -1
                self.minset = possibleMinset[idx]
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


    def askRiichi(self):
        self.isRiichi = False
        if breakdown(self.hand,self.getOpenHand()) != [] :
            # interaction 
            i = input("You can riichi! press space to riichi, other key to abort")
            if i == " ":
                self.isRiichi = True
                return True
        return False

    def askJiaGang(self):
        """
        check Player's 加杠 if player can. self.jiaGang donot have to be called.
        Args:
        Return: Boolean
        """
        jia = 0
        if jia:
            num = int(input("Do you want to JiaGang? 1:yes/0:no\n"))
            if num == 1:
                return True
            else:
                return False
        else:
            return False

    def autoCut(self):
        """
        cut a Pai given
        """
        p = self.hand.pop(-1)
        return p    
    
    def askMin(self,cutPai):
        # interaction
        selection = input("Do you want to Min? \n 0.chi 1.pon 2. kan \nPress no to select, other keys to abort\n")
        if selection == "0": return "Chi"
        if selection == "1": return "Pon"
        if selection == "2": return "Kan"
        return None

    
    def chi(self,paiCut):
        """Perform chi. Add with hand and show in openHand 
    
        Args:
            paiCut (int,int): 
        """
        # record position of possible 副露
        options = []
        i , _ = paiCut
        reduced_hand = [p[0] for p in self.hand]
        # 嵌张
        if has_sequence([(i-1,0),(i,0),(i+1,0)]) and i >= 1:
            try:
                fst = reduced_hand.index(i-1) 
                thrd = reduced_hand.index(i+1)
                options.append([fst,thrd])
            except ValueError:
                pass
        # 大二张
        if has_sequence([(i,0),(i+1,0),(i+2,0)]):
            try:
                snd = reduced_hand.index(i+1)
                thrd = reduced_hand.index(i+2)
                options.append([snd,thrd])
            except ValueError:
                pass
        # 小二张
        if i-2 >= 0 and has_sequence([(i-2,0),(i-1,0),(i,0)]):
            try:
                fst = reduced_hand.index(i-2)
                snd = reduced_hand.index(i-1)
                options.append([fst,snd])
            except ValueError:
                pass
        # Ask player
        if options is not []:
            chi_prompt = "the current Pai is {}. ".format(str(Pai.paiSet[paiCut]))+ "Select from: \n"
            for i, option in enumerate(options):
                a,b = option[0], option[1]
                chi_prompt += "{}. {} ".format(i, str(Pai.paiSet[self.hand[a]])+str(Pai.paiSet[self.hand[b]]))
        print(chi_prompt)
        select = input()
        print("You selected {}".format(select))
        # maintain hand
        a,b = options[int(select)]
        self.openHand["chi"].append([self.hand[a],self.hand[b],paiCut])
        self.hand.pop(b)
        self.hand.pop(a)
        self.hand.sort()
        return "chi"
            
            

    
    def pon(self,paiCut):
        """
        Perform pon.
        
        Args:
            paiCut (int,int): index of Pai cut by other Players.
        
        """
        t,n = paiCut
        a = Pai.hand2Array(self.hand)
        assert(np.sum(a[t]) >= 2)
        # search for tile in hand
        tile = []
        for i in range(4):
            if len(tile) >=2 :
                break

            if a[t,i] == 1:
                a[t,i] = 0
                tile.append((t,i))
        # add at the end to indicate the pai taken from others
        tile.append(paiCut)
        # record in openHand
        self.openHand['pon'].append(tile)
        self.hand = Pai.array2Hand(a)
        return 'pon'
    
    def kan(self,cutpai,anKang=False):
        #print(self.hand)
        #print(self.minset)
        for pai in self.minset:
            self.hand.remove(pai)
        self.openHand["anKang"].append(self.minset)
        return self.minset
    
    
if __name__ == '__main__':
    import doctest