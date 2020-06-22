import Pai
import numpy as np
from collections import Counter

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
        self.wind = None
        self.river = []
        self.hand = None
        self.score = score
        self.draw = None
        self.openHand = {}
        self.isRiichi = False

    # name reference:
    # https://www.wikiwand.com/en/Japanese_Mahjong#/General_mahjong_rules
    # array reference: 
    # 0-8: 一萬 - 九萬
    # 9-17: 一筒 - 九筒
    # 18-26: 一索 - 九索
    # 27，28，29: 中，發，白
    # 30-33: 东西南北

    # these function will be called by GameManager, Player do not need to call them
    
    def setHand(self,hand):
        self.hand = hand

    def setWind(self,wind):
        self.wind = wind
    
    def givePai(self,pai):
        # This function is already implemented, but feel free to change
        self.hand.sort()
        self.draw = pai
        #self.hand.append(p)
        
    def cut(self, target):
        """
        cut a Pai given the position
        Args: int
        Return: Pai
        """
        p = self.hand.pop(target)
        return p

    def autoCut(self):
        """
        cut a Pai given
        """
        p = self.hand.pop(-1)
        return p

    def checkTumo(self):
        """
        check Tumo from self.hand and self.draw
        Args:
        Return: (Boolean, Rondong or Ronxian object in RonWayJapan.py)
        """
        # if can tumo:
        num = int(input("Do you want to Tumo? 1:yes/0:no\n"))
        if num == 1:
            return True, "Nothing"
        else:
            return False, "Nothing"
        # else:
        return False, "Nothing"

    def checkRon(self,cutPai):
        """
        check Player's Ron with cutPai. if Ron then add cutPai to self.hand
        Args: Pai
        Return: (Boolean, Rondong or Ronxian object in RonWayJapan.py)
        """
        # if can Ron:
        num = int(input("Do you want to Ron? 1:yes/0:no\n"))
        if num == 1:
            return True, "Nothing"
        else:
            return False, "Nothing"
        # else:
        return False, "Nothing"

    def askRiichi(self):
        """
        Riichi will be asked from GameMaster. If you already 听牌, you can Riichi. self.riichi donot have to be called
        Args:
        Return: Boolean 
        """
        # if 听牌:
        num = int(input("Do you want to Riichi? 1:yes/0:no\n"))
        if num == 1:
            return True
        else:
            return False

        # else:
        return False

    def askJiaGang(self):
        """
        check Player's 加杠 if player can. self.jiaGang donot have to be called.
        Args:
        Return: Boolean
        """
        # if can 加杠:
        num = int(input("Do you want to JiaGang? 1:yes/0:no\n"))
        if num == 1:
            return True
        else:
            return False
        # else:
        return False

    def askMin(self,cutPai):
        """
        check Player's 鸣 with cutPai if player can. self.chi, self.pon, self.kan donot have to be called
        Args: Pai
        Return: String ("Kan" or "Pon" or "Chi")
        """
        return None, []

    def chi(self,cutPai):
        """
        Perform chi. Add with hand and show in openHand
        Args: Pai
        Return: [Pai] 鸣的set
        """
        return []
    
    def pon(self,cutPai):
        """
        Perform pon.
        Args: Pai
        Return: [Pai]
        """
        return []
    
    def kan(self,cutPai):
        """
        Perform Kan.
        Args: Pai
        Return: [Pai]
        """
        return []

    def jiagang(self):
        """
        do 加杠 with self.draw.
        Args:
        Return: [Pai]
        """
        return []

    def riichi(self):
        """
        Perform Riichi
        Args:
        Return:
        """
        self.isRiichi = True
        #为了self.autoCut()把不需要的牌放在self.hand的最后
    