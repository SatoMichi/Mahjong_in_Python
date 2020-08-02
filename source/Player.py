import Pai
import numpy as np
from collections import Counter

class Player:
    
    def __init__(self,name,cut,hand,score,draw):
        """
        river : [(t,n)] All Pai cut
        
        hand: [(t,n)] t is the index for pai type, n distinguish pai of the same type
        
        openHand: [[(Pai,Int)]] Pai shown on the table because of Min or Riichi. Use 1 for self,
        2 for others, 3 for kakan
        
        draw: Pai the one Pai drawn
        """
        self.name = name
        self.river = []
        self.hand = hand
        self.score = score
        self.draw = draw
        self.openHand = {}

    # name reference:
    # https://www.wikiwand.com/en/Japanese_Mahjong#/General_mahjong_rules
    # array reference: 
    # 0-8: 一萬 - 九萬
    # 9-17: 一筒 - 九筒
    # 18-26: 一索 - 九索
    # 27，28，29: 中，發，白
    # 30-33: 东西南北
    def draw(self,p):
        self.draw = p
        self.hand.append(p)
        self.hand.sort()
        
    def cut(self,target):
        """
        cut a Pai given the position
        """
        p = self.hand.pop(target)
        river.append(p)
        return p

    def chi(self,paiCut,order):
        """Perform chi. Add with hand and show in openHand
    
        Args:
            paiCut (int): index of Pai cut by other Players.
            order {-1,1}: -1 gets 2 smaller pai. 1 gets 2 bigger pai
        """
        pass
    
    def pon(self,paiCut):
        """
        Perform pon.
        
        Args:
            paiCut (int): index of Pai cut by other Players.
        
        """
        pass
    def kan():
        pass
    def riichi():
        pass
    def checkWin():
        pass
    def tenpai():
        pass
        