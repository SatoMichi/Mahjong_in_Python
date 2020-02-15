import numpy as np

class numPai:
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

    def __init__(self,num,suit):
        self.num = num-1
        self.suit = suit-1

    def __str__(self):
        return self.i[self.num]+self.s[self.suit]

    def __lt__(self, other):
        if self.suit != other.suit:
            return self.suit < other.suit
        elif self.num == None and other.num == None:
            return True
        else:
            return self.num < other.num

    def imgPathU(self):
        path = self.img[self.suit][self.num]
        return "img/imgUp/" + path
    def imgPathD(self):
        path = self.img[self.suit][self.num][:-5] +"2"+".gif"
        return "img/imgDown/" + path
    def imgPathL(self):
        path = self.img[self.suit][self.num][:-5] +"3"+".gif"
        return "img/imgLeft/" + path
    def imgPathR(self):
        path = self.img[self.suit][self.num][:-5] +"4"+".gif"
        return "img/imgRight/" + path

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


allPai = [numPai(num,suit) for num in range(1,10) for suit in range(1,4)] + [charPai(suit) for suit in range(4,10)]
originalYama = np.random.permutation(allPai*4)

def getFirstHand(yama):
    return yama[0:13], yama[13:26], yama[26:39], yama[39:52], yama[52:]

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
