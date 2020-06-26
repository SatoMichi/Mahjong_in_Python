import Pai
import numpy as np
from collections import Counter
from util import is_sequence

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
        self.river = []
        self.hand = None
        self.score = score
        self.draw = None
        self.openHand = {"chi":[], "pon":[], "anKang":[], "minKang":[]}

    # name reference:
    # https://www.wikiwand.com/en/Japanese_Mahjong#/General_mahjong_rules
    # array reference: 
    # 0-8: 一萬 - 九萬
    # 9-17: 一筒 - 九筒
    # 18-26: 一索 - 九索
    # 27，28，29: 中，發，白
    # 30-33: 东西南北
    def setHand(self,hand):
        self.hand = hand
        
    def setWind(self,wind):
        self.wind = wind
    
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
        return False, "Nothing"

    def checkRon(self):
        return False, "Nothing"

    def askRiichi(self):
        self.riichi = False
        return False

    def autoCut(self):
        """
        cut a Pai given
        """
        p = self.hand.pop(-1)
        return p    
    
    def askMin(self):
        return None, []

    
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
        if is_sequence([(i-1,0),(i,0),(i+1,0)]) and i >= 1:
            try:
                fst = reduced_hand.index(i-1) 
                thrd = reduced_hand.index(i+1)
                options.append([fst,thrd])
            except ValueError:
                pass
        # 大二张
        if is_sequence([(i,0),(i+1,0),(i+2,0)]):
            try:
                snd = reduced_hand.index(i+1)
                thrd = reduced_hand.index(i+2)
                options.append([snd,thrd])
            except ValueError:
                pass
        # 小二张
        if i-2 >= 0 and is_sequence([(i-2,0),(i-1,0),(i,0)]):
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
        return "chi"
            
            

    
    def pon(self,paiCut):
        """
        Perform pon.
        
        Args:
            paiCut (int): index of Pai cut by other Players.
        
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
        openHand['pon'].append(tile)
        self.hand = Pai.array2Hand(a)
        return 'pon'
    def kan():
        pass
    def riichi():
        pass
    def checkWin():
        pass
    
    