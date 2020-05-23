from Pai import originalYama,allPai,showHand
import numpy as np


#十三幺//国士无双Ron hand and openHand are list[list[(int,int)]]
#十三幺分牌规则有待商榷****
#def kokusi13machi(hand,openHand):
#    yao13 = [0,8,9,17,18,26,27,28,29,30,31,32,33]
#    ron = (len(hand) == 14) and (len(openHand)==0)
#    for p in yao13:
#        ron = ron and p in [str(h) for h in hand]
#    return ron


#飘Ron hand and openHand are list[list[(int,int)]]
#检测规则:手牌与副露中均为刻子
def piao(hand,openHand):
    ron = True
    #检查展开的手牌是否均为碰牌
    for oph in openHand:
        #[(28,0),(28,2),(28,3)]
        if(not (oph[0][0]==oph[1][0] and oph[1][0]==oph[2][0])):
            ron = ron and False
    #检查手中的牌是否满足飘的条件
    #如果手中是一个雀头则一定满足条件
    if(len(openHand)==1 and len(openHand[0])==2):
        ron = ron and True
    #如果手中是一个雀头加任意数量的刻子则也满足条件,但需要注意可能出现一杯口或七对子误判的情况
    else:
        quetou = 0
        for h in hand:
            #刻子
            if(len(h)==3):
                if(not (h[0][0]==h[1][0] and h[1][0]==h[2][0])):
                    ron = ron and False
            #雀头
            if(len(h)==2):
                quetou = quetou + 1
        if(not quetou == 1):
            ron = ron and False
    return ron

#大三元Ron hand and openHand are list[list[(int,int)]]
def dasanyuan(hand,openHand):
    ron = [False,False,False]
    for h in hand:
        if(len(h)==3 and h[0][0]==27):
            ron[0]=True
        if(len(h)==3 and h[0][0]==28):
            ron[1]=True
        if(len(h)==3 and h[0][0]==29):
            ron[2]=True
    for oph in openHand:
        if(len(oph)==3 and oph[0][0]==27):
            ron[0]=True
        if(len(oph)==3 and oph[0][0]==28):
            ron[1]=True
        if(len(oph)==3 and oph[0][0]==29):
            ron[2]=True
    if(not False in ron):
        return True
    else:
        return False


#役牌 自风 hand and openHand are list[list[(int,int)]]
def zifeng(hand,openHand,zifeng):
    ron = False
    for oph in openHand:
        if(oph[0][0]==zifeng):
            ron = True
    for h in hand:
        if(len(h)==3 and h[0][0]==zifeng):
            ron = True
    return ron

#役牌 场风 hand and openHand are list[list[(int,int)]]
def zifeng(hand,openHand,changfeng):
    ron = False
    for oph in openHand:
        if(oph[0][0]==changfeng):
            ron = True
    for h in hand:
        if(len(h)==3 and h[0][0]==changfeng):
            ron = True
    return ron

#役牌 中 hand and openHand are list[list[(int,int)]]
def sanyuan_zhong(hand,openHand):
    ron = False
    for oph in openHand:
        if(oph[0][0]==27):
            ron = True
    for h in hand:
        if(len(h)==3 and h[0][0]==27):
            ron = True
    return ron

#役牌 发 hand and openHand are list[list[(int,int)]]
def sanyuan_fa(hand,openHand):
    ron = False
    for oph in openHand:
        if(oph[0][0]==28):
            ron = True
    for h in hand:
        if(len(h)==3 and h[0][0]==28):
            ron = True
    return ron

#役牌 白 hand and openHand are list[list[(int,int)]]
def sanyuan_bai(hand,openHand):
    ron = False
    for oph in openHand:
        if(oph[0][0]==29):
            ron = True
    for h in hand:
        if(len(h)==3 and h[0][0]==29):
            ron = True
    return ron

#门前役(指在门前清听牌为条件下，和牌才成立的役种)

#一番役
#役牌 一杯口 hand and openHand are list[list[(int,int)]]
#判断方法:判断要将其与二杯口区分开(若是二杯口则不和一杯口)
def yibeikou(hand):
    ron = False
    hand_num = pai2onlyno(hand)
    kou_num = 0
    for h in hand_num:
        if(hand_num.count(h)==2):
            kou_num = kou_num + 1
    if(kou_num==2):
        ron = True
    return ron

#役牌 断幺九 hand and openHand are list[list[(int,int)]]
def noyaojiu(hand):
    ron = True
    yao13 = [0,8,9,17,18,26,27,28,29,30,31,32,33]
    for i in yao13:
        for h in hand:
            for s_h in h:
                if(i==s_h[0]):
                    ron = ron and False
    return ron

#二番役

#役牌 七对子 hand and openHand are list[list[(int,int)]]
def chitoi(hand):
    ron = True
    for h in hand:
        if(not len(h)==2):
            ron = False
    return ron

#三番役

#役牌 二杯口 hand and openHand are list[list[(int,int)]]
#判断方法:判断要将其与一杯口区分开来(若是二杯口则不和一杯口)
def erbeikou(hand):
    ron = False
    hand_num = pai2onlyno(hand)
    kou_num = 0
    for h in hand_num:
        if(hand_num.count(h)==2):
            kou_num = kou_num + 1
    if(kou_num==4):
        ron = True
    return ron

#门前清役满机会

#役牌 四暗刻 hand and openHand are list[list[(int,int)]]
def sianke(hand):
    k = 0
    for h in hand:
        if(len(h)==3):
            if(h[0][0]==h[1][0] and h[1][0]==h[2][0]):
                k = k + 1
    if(k==4):
        return True
    return False

#役牌 九莲宝灯 hand and openHand are list[list[(int,int)]]
def jiulianbaodeng(hand):
    return True





#helper function

#change list[list[(int,int)]] into list[list[int]]
def pai2onlyno(hand):
    honlyno = []
    for h in hand:
        if(len(h)==3):
            new_h = [h[0][0],h[1][0],h[2][0]]
        if(len(h)==2):
            new_h = [h[0][0],h[1][0]]
        honlyno.append(new_h)
    return honlyno


#def num2array(hand):
#    nums = np.zeros([9])
#    label = {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}
#    for p in hand:
#        nums[label[str(p)[0]]] += 1
#    return nums

#def pai2array(hand):
#    nums = np.zeros([34])
#    label = {'一萬': 0, '二萬': 1, '三萬': 2, '四萬': 3, '五萬': 4, '六萬': 5, '七萬': 6, '八萬': 7, '九萬': 8,
#             '一筒': 9, '二筒': 10, '三筒': 11, '四筒': 12, '五筒': 13, '六筒': 14, '七筒': 15, '八筒': 16, '九筒': 17,
#             '一索': 18, '二索': 19, '三索': 20, '四索': 21, '五索': 22, '六索': 23, '七索': 24, '八索': 25, '九索': 26,
#             '中': 27, '發': 28, '白': 29, '東': 30, '西': 31, '南': 32, '北': 33}
#    for p in hand:
#        nums[label[str(p)]] += 1
#    return nums

#def existMians(num):
#    if not sum(num)%3 == 0: # Mians couldnot be constructed
#        return False
#    a = num[0]         # Pai currentry concerend
#    b = num[1]         # next pai tobe concerned
#    for i in range(7):
#        r = a % 3      # number of Pai not becoming Mians
#        if(b>=r and num[i+2]>=r):
#            a = b - r
#            b = num[i+2] - r
#        else:
#            return False
#    if(a%3==0 and b%3==0): # last check
#        return True
#    else:
#        return False

#def qinwho(num):
#    handsum = 0
#    for i in range(9):
#        handsum += i*num[i]
#    i = int(handsum *2 %3)
#    return backtrack(i,num)

#def backtrack(i,num):
#    if not i<9:
#        return False
#    num[i] -= 2       # try this as head
#    if num[i] >= 0:
#        if existMians(num):
#            num[i] += 2
#            return True
#    num[i] += 2
#    return backtrack(i+3,num)

#def who(hand):
#    nums = pai2array(hand)
#    head = -1               # head is not decided yet
#    # judge each numPais
#    for i in range(3):
#        case = sum(nums[i*9:i*9+10])%3
#        if case == 1:
#            return False
#        elif case == 2:
#            if(head==-1):
#                head = i
#            else:
#                return False
#
#    # judge for charPais
#    for i in range(27,34):
#        if nums[i]%3 == 1:
#            return False
#        elif nums[i]%3 == 2:
#            if head == -1:
#                head = i
#            else:
#                return False
#        else:
#            pass # charPai forms 刻子
#
#    # final judge with head check
#    for i in range(3):
#        if i==head: # head is nmPai
#            if not qinwho(nums[9*i:9*i+10]):
#                return False
#        else:
#            if not existMians(nums[9*i:9*i+10]):
#                return False
#    return True


#日本麻将胡牌函数
#hand 为 list[list[(int,int)]],openHand 为 list[list[(int,int)]]
#lichi为booolean,为了判断Player是否立直
#zifeng和changfeng均为int,[30--33](表示本场游戏的自风与场风)
def JapanRon(hand,openHand,lichi,zifeng,changfeng):
    kokusi = kokusi13machi(hand,openHand)
    chitois = chitoi(hand,openHand)
    piao = piao(hand,openHand,hand_num)
    return (kokusi + chitois + normal_who)
