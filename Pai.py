import numpy as np
from collections import Counter 
from random import shuffle

""" 
All Pai are initialized once in this module.

hand and Yama are represented using [tuple(t,n)]. paiSet[t,n] gives the corresponding Pai object.
""" 

# Class representing Pais
# for example:
# p = Pai(0,0) -> p is 一萬
# p = Pai(3)   -> p is 中
class Pai:
    '''
    represent Pai using num and suit. Should not be intialized outside pai.py
    '''
    i = ["一","二","三","四","五","六","七","八","九"]
    s = ["萬","筒","索","中","發","白","東","西","南","北"]
    img = [['p_ms1_1.gif', 'p_ms2_1.gif', 'p_ms3_1.gif', 'p_ms4_1.gif',
            'p_ms5_1.gif', 'p_ms6_1.gif', 'p_ms7_1.gif', 'p_ms8_1.gif', 'p_ms9_1.gif'],
            ['p_ps1_1.gif', 'p_ps2_1.gif', 'p_ps3_1.gif', 'p_ps4_1.gif',
            'p_ps5_1.gif', 'p_ps6_1.gif', 'p_ps7_1.gif', 'p_ps8_1.gif', 'p_ps9_1.gif'],
            ['p_ss1_1.gif', 'p_ss2_1.gif', 'p_ss3_1.gif', 'p_ss4_1.gif',
            'p_ss5_1.gif', 'p_ss6_1.gif', 'p_ss7_1.gif', 'p_ss8_1.gif', 'p_ss9_1.gif'],
            ['p_ji_c_1.gif', 'p_ji_h_1.gif', 'p_no_1.gif', 'p_ji_e_1.gif', 'p_ji_w_1.gif',
            'p_ji_s_1.gif', 'p_ji_n_1.gif']]

        
    def __init__(self,suit,num=-1):
        # self.suit : (0,萬) (1,筒) (2,索) (3,中) (4,發) (5,白) (6,東) (7,西) (8,南) (9,北)
        self.suit = suit
        # self.num : (-1,字牌) (0..8, 数牌的数)
        self.num = num
        

    def __str__(self):
        if self.num == -1:
            return self.s[self.suit]
        else:
            return self.i[self.num]+self.s[self.suit]

    # due to this method, Pai can be sorted
    # [Pai].sort() is defined by this method
    def __lt__(self, other):
        if self.suit != other.suit:
            return self.suit < other.suit
        elif self.num == None and other.num == None:
            return True
        else:
            return self.num < other.num
    
    def distance(self,other):
        """
        三万，三万： 0
        三万，四万：1
        三万，五万：2
        otherwise: 3 (不可能成为对和牌有利的因素)
        比如 三万，六万，三万四索，等等
        """
        if self.suit != other.suit:
            return 3
        else:
            if self.num == other.num: return 0
            elif abs(other.num - self.num) == 1: return 1
            elif abs(other.num - self.num) == 2: return 2
            else : return 3
    
    # following methods are for Graphical User Interface (GUI)
    # please ignore for now
    def imgPathU(self):
        if self.num == -1:
            path = self.img[3][self.suit-3]
        else:
            path = self.img[self.suit][self.num]
        return "img/imgUp/" + path
    def imgPathD(self):
        if self.num == -1:
            path = self.img[3][self.suit-3][:-5] +"2"+".gif"
        else:
            path = self.img[self.suit][self.num][:-5] +"2"+".gif"
        return "img/imgDown/" + path
    def imgPathL(self):
        if self.num == -1:
            path = self.img[3][self.suit-3][:-5] +"3"+".gif"
        else:
            path = self.img[self.suit][self.num][:-5] +"3"+".gif"
        return "img/imgLeft/" + path
    def imgPathR(self):
        if self.num == -1:
            path = self.img[3][self.suit-3][:-5] +"4"+".gif"
        else:
            path = self.img[self.suit][self.num][:-5] +"4"+".gif"
        return "img/imgRight/" + path
    


"""
class charPai(numPai):
    def __init__(self,suit):
        self.num = None
        self.suit = suit-1
    def __str__(self):
        return self.s[self.suit]
    def imgPathU(self):
        path = self.img[3][self.suit-3]
        return "img/imgUp/" + path
    def imgPathD(self):
        path = self.img[3][self.suit-3][:-5] +"2"+".gif"
        return "img/imgDown/" + path
    def imgPathL(self):
        path = self.img[3][self.suit-3][:-5] +"3"+".gif"
        return "img/imgLeft/" + path
    def imgPathR(self):
        path = self.img[3][self.suit-3][:-5] +"4"+".gif"
        return "img/imgRight/" + path
"""
# all kind of Pai
allPai = [Pai(suit,num) for suit in range(0,3) for num in range(0,9)] + [Pai(suit) for suit in range(3,10)]
# create 4x34 matrix with all the Pai objects as a static reference
# in current version different rows refer to same objects
# ex. paiSet[0,0] is paiSet[1,0] returns True
paiSet = np.tile(allPai,(4,1)).T
# represent Pai as index, reference paiSet to show Pai
originalYama = [(t,n) for t in range(34) for n in range(4)]
shuffle(originalYama)

'''
old reference
# str -> num
ref = dict(zip(map(str,allPai),range(34)))
# num -> str
ref_str = {}
for key, value in ref.items():
    ref_str[value] = key
'''
# type definition for Hand type
# basically Hand is list of Pai
# Hand = [(t,n)]
testHand = originalYama[0:13]
testHand.sort()
# By usinng following function hand can be translated between [Pai] and np.array(4x34)

# [(t,n)] -> np.array(34x4)
def hand2Array(hand):
    a = np.zeros((34,4))
    for p in hand:
        a[p] = 1
    return a

# np.array(34x4) -> [(t,n)]
def array2Hand(array):
    index = np.argwhere(array == 1)
    return list(map(tuple,index))

def tuple2Object(tuple_hand):
    return [paiSet[i] for i in tuple_hand]


# Helper function for debug
def showHand(hand):
    return str([ str(paiSet[p]) for p in hand])

"""
def compPai(p1,p2):
    if p1.suit > p2.suit:
        return p2
    elif p1.suit < p2.suit:
        return p1
    else:
        if p1.num == None and p2.num == None:
            return p1
        elif p1.num > p2.num:
            return p1
        else:
            return p2
"""