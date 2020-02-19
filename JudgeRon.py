from Pai import originalYama,allPai,showHand
import numpy as np

testcase = np.random.permutation(allPai[:27]*4)

def kokusi13machi(hand):
    yao13 = ["一萬","九萬","一筒","九筒","一索","九索","中","發","白","東","西","南","北"]
    last = hand[-1]
    ron = len(hand) == 14
    for p in yao13:
        ron = ron and p in [str(h) for h in hand]
    ron = ron and str(last) in yao13
    return ron

def chitoi(hand):
    hand.sort()
    ron  = len(hand) == 14
    for i in range(0,14,2):
        ron = ron and (str(hand[i]) == str(hand[i+1]))
    return ron


def num2array(hand):
    nums = np.zeros([9])
    label = {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}
    for p in hand:
        nums[label[str(p)[0]]] += 1
    return nums

def pai2array(hand):
    nums = np.zeros([34])
    label = {'一萬': 0, '二萬': 1, '三萬': 2, '四萬': 3, '五萬': 4, '六萬': 5, '七萬': 6, '八萬': 7, '九萬': 8,
             '一筒': 9, '二筒': 10, '三筒': 11, '四筒': 12, '五筒': 13, '六筒': 14, '七筒': 15, '八筒': 16, '九筒': 17,
             '一索': 18, '二索': 19, '三索': 20, '四索': 21, '五索': 22, '六索': 23, '七索': 24, '八索': 25, '九索': 26,
             '中': 27, '發': 28, '白': 29, '東': 30, '西': 31, '南': 32, '北': 33}
    for p in hand:
        nums[label[str(p)]] += 1
    return nums

def existMians(num):
    if not sum(num)%3 == 0: # Mians couldnot be constructed
        return False
    a = num[0]         # Pai currentry concerend
    b = num[1]         # next pai tobe concerned
    for i in range(7):
        r = a % 3      # number of Pai not becoming Mians
        if(b>=r and num[i+2]>=r):
            a = b - r
            b = num[i+2] - r
        else:
            return False
    if(a%3==0 and b%3==0): # last check
        return True
    else:
        return False

def qinwho(num):
    handsum = 0
    for i in range(9):
        handsum += i*num[i]
    i = int(handsum *2 %3)
    return backtrack(i,num)

def backtrack(i,num):
    if not i<9:
        return False
    num[i] -= 2       # try this as head
    if num[i] >= 0:
        if existMians(num):
            num[i] += 2
            return True
    num[i] += 2
    return backtrack(i+3,num)

def who(hand):
    nums = pai2array(hand)
    head = -1               # head is not decided yet
    # judge each numPais
    for i in range(3):
        case = sum(nums[i*9:i*9+10])%3
        if case == 1:
            return False
        elif case == 2:
            if(head==-1):
                head = i
            else:
                return False
            
    # judge for charPais
    for i in range(27,34):
        if nums[i]%3 == 1:
            return False
        elif nums[i]%3 == 2:
            if head == -1:
                head = i
            else:
                return False
        else:
            pass # charPai forms 刻子
        
    # final judge with head check
    for i in range(3):
        if i==head: # head is nmPai
            if not qinwho(nums[9*i:9*i+10]):
                return False
        else:
            if not existMians(nums[9*i:9*i+10]):
                return False
    return True


def Ron(hand):
    kokusi = kokusi13machi(hand)
    chitois = chitoi(hand)
    normal_who = who(hand)
    return kokusi or chitois or normal_who
