import numpy as np
from collections import Counter

class Pai:
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

    def __lt__(self, other):
        if self.suit != other.suit:
            return self.suit < other.suit
        elif self.num == None and other.num == None:
            return True
        else:
            return self.num < other.num

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

allPai = [Pai(suit,num) for suit in range(0,3) for num in range(0,9)] + [Pai(suit) for suit in range(3,10)]
originalYama = np.random.permutation(allPai*4)

Hand = [Pai]

# [Pai] -> np.array(4x34)
def hand2Array(hand):
    ref = dict(zip(map(str,allPai),range(34)))
    handArr = np.zeros([4,34])
    
    place = list(map(lambda pai: ref[str(pai)], hand))
    place = dict(Counter(place))

    for pai in place:
        for i in range(place[pai]):
            handArr[i,pai] = 1
    
    return handArr

# np.array(4x34) -> [Pai]
def array2Hand(array):
    ref = dict(zip(range(34),allPai))
    handPai = []
    array = array.sum(axis=0)

    for pai,num in enumerate(array):
        for i in range(int(num)):
            handPai.append(ref[pai])
    
    return handPai


# Helper function for debug
def showHand(hand):
    return list(map(str,hand))

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
