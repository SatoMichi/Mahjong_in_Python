import numpy as np
from collections import Counter 
from random import shuffle
import re

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

def showHand(hand):
    return str([ str(paiSet[p]) for p in hand])

def previous(pai):
    """
    take in a tuple, return a position before if 数牌
    
    >>> previous((0,0))
    
    >>> previous((1,0))
    0
    """
    # 0-8: 一萬 - 九萬
    # 9-17: 一筒 - 九筒
    # 18-26: 一索 - 九索
    n,_ = pai
    if  1 <= n <= 8 or 10 <= n <= 17 or 19 <= n <= 26:
        return n-1
    else: 
        return None

def next(pai):
    """
    >>> next((8,0))
    >>> 9
    """
    n,_ = pai
    if 0 <= n <= 7 or 9 <= n <= 16 or 18 <= n <= 25:
        return n+1
    else:
        return None
    
def same(pai):
    return pai[0]

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

def parsedPai(shorthand):
    """
    String -> [Int]
    change shorthand to list of Pai index. 
    
    Note: 
    - Use C(centre) for 中，B(blank) for 白, F(fortune) for 发. Also in accordance with pronounciation.
    - Also can use tenhou representation: 567z for 白发中
    - m,p,s for 万，筒，索
    - 1234z for 东，南，西，北
    
    >>> parsedPai("1234zbfc")
    [30, 31, 32, 33, 29, 28, 27]
    >>> parsedPai("1234567z")
    [30, 31, 32, 33, 29, 28, 27]
    
    >>> parsedPai("123m123p123s")
    [0, 1, 2, 9, 10, 11, 18, 19, 20]
    
    >>> parsedPai("111222m333p")
    [0, 0, 0, 1, 1, 1, 11, 11, 11]
    
    """
    word_map = {
        "c":27,
        "f":28,
        "b":29,
    }
    result = []
    number_pattern = re.compile(r'[1-9]+[mpsz]')
    number_tiles = number_pattern.findall(shorthand)
    for split in number_tiles:
        if split[-1] is "m":
            result += [int(p)-1 for p in split[:-1]]
        if split[-1] is "p":
            result += [int(p)+8 for p in split[:-1]]
        if split[-1] is "s":
            result += [int(p)+17 for p in split[:-1]]
        if split[-1] is "z":
            result += [int(p)+29 if int(p) <=4 else 34 - int(p)  for p in split[:-1]]
              
    word_pattern = re.compile(r'[cfb]')
    word_tiles = word_pattern.findall(shorthand)
    for split in word_tiles:
        result.append(word_map[split])
    return result

def shorthand(list_pai):
    """
    [Int] -> String
    the opposite of parsedPai. Turn list of pai into shorthand.
    
    >>> shorthand([30, 31, 32, 33, 29, 28, 27])
    '1234zbfc'
    
    >>> shorthand([0, 1, 2, 9, 10, 11, 18, 19, 20])
    '123m123p123s'
    """
    mapping = {
        27: "c",
        28: "f",
        29: "b"
    }
    m,p,s,z = [],[],[],[]
    result = ""
    for pai in list_pai:
        if pai <= 8:
            m.append(str(pai+1))
        if 8 < pai <= 17:
            p.append(str(pai-8))
        if 17 < pai <= 26:
            s.append(str(pai-17))
        if 29 < pai:
            z.append(str(pai-29))
    if m != [] :
        result += "".join(m) + "m"
    if p != []:
        result += "".join(p) + "p"
    if s != []:
        result += "".join(s) + "s"
    if z != []:
        result += "".join(z) + "z"
    for pai in list_pai:    
        if 27 <= pai <= 29:
            result += mapping[pai]
    return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()