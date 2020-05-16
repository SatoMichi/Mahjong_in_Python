import Pai
import numpy as np
from collections import Counter

class Player:
    
    def __init__(self,name,cut,hand,score,draw):
        self.name = name
        self.cut = cut
        self.hand = hand
        self.score = score
        self.draw = draw
        self.openHand = np.zeros((4,34))

    # name reference:
    # https://www.wikiwand.com/en/Japanese_Mahjong#/General_mahjong_rules
    # array reference: 
    # 0-8: 一萬 - 九萬
    # 9-17: 一筒 - 九筒
    # 18-26: 一索 - 九索
    # 27，28，29: 中，發，白
    # 30-33: 东西南北
    def cut(self,target):
        hand[0,target] = 0
        clean_col = np.trim_zeros(hand[:,target])
        hand[:,target] = clean_col.resize((1,4))
        return Pai.fromIndex(target)

    def chi(self,paiCut,):
        pass
    def pon(self,paiCut):
        hand[0:2,paiCut] = 0
        # adjust hand so columns start with 1
        clean_col = np.trim_zeros(hand[:,paiCut])
        hand[:,paiCut] = clean_col.resize((1,4))
        # record in openHand
        openHand[0:3,paiCut] = 1
    def kan():
        pass
    def richi():
        pass
    def win():
        pass