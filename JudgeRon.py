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

#非门前役(下列和牌方式不需要门前清,只要满足和牌规则即可加番)

#一番役(非门前清限定！！！)

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
def changfeng(hand,openHand,changfeng):
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

#役牌 断幺九 hand and openHand are list[list[(int,int)]]
def noyaojiu(hand,openHand):
    ron = True
    yao13 = [0,8,9,17,18,26,27,28,29,30,31,32,33]
    for i in yao13:
        for h in hand:
            for s_h in h:
                if(i==s_h[0]):
                    ron = ron and False
        for oph in openHand:
            for s_oph in oph:
                if(i==s_oph[0]):
                    ron = ron and False
    return ron

#二番役(非门前清限定！！！)

#役牌 三色同刻 万,筒,索都有相同的数字刻子(E.g. 三万刻子,三索刻子,三筒刻子) hand and openHand are list[list[(int,int)]]
def sansetk(hand,openHand):
    ron = False
    for oph in openHand:
        if(oph[0][0]==oph[1][0] and oph[1][0]==oph[2][0] and oph[0][0]<27):
            rons=[False,False]
            if(oph[0][0]<9):
                s1 = oph[0][0] + 9
                s2 = oph[0][0] + 18
            elif(oph[0][0]<18):
                s1 = oph[0][0] - 9
                s2 = oph[0][0] + 9
            else:
                s1 = oph[0][0] - 18
                s2 = oph[0][0] - 9
            for oph in openHand:
                if(oph[0][0]==s1 and oph[1][0]==s1 and oph[2][0]==s1):
                    rons[0] = True
                if(oph[0][0]==s2 and oph[1][0]==s2 and oph[2][0]==s2):
                    rons[1] = True
            for h in hand:
                if(len(h)==3):
                    if(h[0][0]==s1 and h[1][0]==s1 and h[2][0]==s1):
                        rons[0] = True
                    if(h[0][0]==s2 and h[1][0]==s2 and h[2][0]==s2):
                        rons[1] = True
            if(not (False in rons)):
                ron = True
        if(ron):
            break
    if(not ron):
        for h in hand:
            if(len(h)==3):
                if(h[0][0]==h[1][0] and h[1][0]==h[2][0] and h[0][0]<27):
                    rons=[False,False]
                    if(h[0][0]<9):
                        s1 = h[0][0] + 9
                        s2 = h[0][0] + 18
                    elif(h[0][0]<18):
                        s1 = h[0][0] - 9
                        s2 = h[0][0] + 9
                    else:
                        s1 = h[0][0] - 18
                        s2 = h[0][0] - 9
                    for h in hand:
                        if(len(h)==3):
                            if(h[0][0]==s1 and h[1][0]==s1 and h[2][0]==s1):
                                rons[0] = True
                            if(h[0][0]==s2 and h[1][0]==s2 and h[2][0]==s2):
                                rons[1] = True
                    if(not (False in rons)):
                        ron = True
            if(ron):
                break
    return ron

#役牌 三杠子 一人开杠三次 hand and openHand are list[list[(int,int)]]
def sangangzi(hand,openHand):
    gang = 0
    for oph in openHand:
        if(len(oph)==4):
            gang = gang + 1
    if(gang == 3):
        return True
    return False

#役牌 三暗刻 拥有三组没有碰的刻子 hand and openHand are list[list[(int,int)]]
def sananke(hand,openHand):
    k = 0
    for h in hand:
        if(len(h)==3):
            if(h[0][0]==h[1][0] and h[1][0]==h[2][0]):
                k = k + 1
    if(k==3):
        return True
    return False

#役牌 飘(対々和) hand and openHand are list[list[(int,int)]]
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

#役牌 小三元 包含中发白其中两种的刻子以及其中一种的雀头 hand and openHand are list[list[(int,int)]]
def xiaosanyuan(hand,openHand):
    ron = [False,False,False]
    for oph in openHand:
        if(oph[0][0]==27 or oph[0][0]==28 or oph[0][0]==29):
            if(not ron[0]):
                ron[0]=True
            elif(not ron[1]):
                ron[1]=True
    for h in hand:
        if(len(h)==2):
            if(h[0][0]==27 or h[0][0]==28 or h[0][0]==29):
                ron[2]=True
        if(len(h)==3):
            if(oph[0][0]==27 or oph[0][0]==28 or oph[0][0]==29):
                if(not ron[0]):
                    ron[0]=True
                elif(not ron[1]):
                    ron[1]=True
    if(not False in ron):
        return True
    return False

#役牌 混老头 胡牌时只包含老头牌和字牌 hand and openHand are list[list[(int,int)]]
def hunlaotou(hand,openHand):
    ron = True
    laotou = [0,8,9,17,18,26,27,28,29,30,31,32,33]
    for oph in openHand:
        if( not (oph[0][0]==oph[1][0] and oph[1][0]==oph[2][0] and (oph[0][0] in laotou))):
            ron = ron and False
    for h in hand:
        if(len(h)==2):
            if(not h[0][0] in laotou):
                ron = ron and False
        else:
            if( not (h[0][0]==h[1][0] and h[1][0]==h[2][0] and (h[0][0] in laotou))):
                ron = ron and False
    return ron

#役牌 混全带幺九 包含老头牌加上字牌的4组顺子和刻子+幺九牌的雀头 hand and openHand are list[list[(int,int)]]
def hqdyj(hand,openHand):
    ron = True
    yao13 = [0,8,9,17,18,26,27,28,29,30,31,32,33]
    for h in hand:
        if(len(h)==2):
            if(not (h[0][0] in yao13 or h[1][0] in yao13)):
                ron = ron and False
        if(len(h)==3):
            if(not (h[0][0] in yao13 or h[1][0] in yao13 or h[2][0] in yao13)):
                ron = ron and False
    for oph in openHand:
        if(not (oph[0][0] in yao13 or oph[1][0] in yao13 or oph[2][0] in yao13)):
            ron = ron and False
    return ron

#役牌 一气贯通 同种数牌组成123,456,789的顺子 hand and openHand are list[list[(int,int)]]
def yiqiguantong(hand,openHand):
    hand_no = pai2onlyno(hand)
    openHand_no = pai2onlyno(openHand)
    for i in range(3):
        ron_judge = [[0+i*9,1+i*9,2+i*9],[3+i*9,4+i*9,5+i*9],[6+i*9,7+i*9,8+i*9]]
        ron = [False,False,False]
        for j,r in enumerate(ron_judge):
            if(r in hand_no or r in openHand_no):
                ron[j] = True
        if(not False in ron):
            return True
    return False

#役牌 三色同顺 万,筒,索都有相同数字的顺子 hand and openHand are list[list[(int,int)]]
def sansets(hand,openHand):
    hand_no = pai2onlyno(hand)
    openHand_no = pai2onlyno(openHand)
    for i in range(7):
        ron_judge = [[0+i,1+i,2+i],[9+i,10+i,11+i],[18+i,19+i,20+i]]
        ron = [False,False,False]
        for j,r in enumerate(ron_judge):
            if(r in hand_no or r in openHand_no):
                ron[j] = True
        if(not False in ron):
            return True
    return False

#三番役(非门前清限定！！！)

#役牌 混一色 只包含一种数牌,并且含有字牌的刻子或者雀头 hand and openHand are list[list[(int,int)]]
def hunyise(hand,openHand):
    hand_no = pai2onlyno(hand)
    openHand_no = pai2onlyno(openHand)
    ron = [False,False,False]
    qingyise = [0,1,2,3,4,5,6,7,8]
    for i in range(3):
        qingyisepai = [qys + 9*i for qys in qingyise]
        hunyisepai = qingyisepai + [27,28,29,30,31,32,33]
        if_ron = True
        for oph in openHand_no:
            for op in oph:
                if(not op in hunyisepai):
                    if_ron = False
        for ha in hand_no:
            for h in ha:
                if(not h in hunyisepai):
                    if_ron = False
        if(if_ron):
            ron[i]= True
    if(True in ron):
        return True
    return False

#役牌 纯全带幺九 只包含老头牌的四组顺子和刻子+老头牌的雀头
def cqdyj(hand,openHand):
    ron = True
    laotou = [0,8,9,17,18,26]
    for h in hand:
        if(len(h)==2):
            if(not (h[0][0] in laotou or h[1][0] in laotou)):
                ron = ron and False
        if(len(h)==3):
            if(not (h[0][0] in laotou or h[1][0] in laotou or h[2][0] in laotou)):
                ron = ron and False
    for oph in openHand:
        if(not (oph[0][0] in laotou or oph[1][0] in laotou or oph[2][0] in laotou)):
            ron = ron and False
    return ron

#六番役(非门前清限定！！！)

#役牌 清一色 只包含一种数牌,不能包含字牌  hand and openHand are list[list[(int,int)]]
def qingyise(hand,openHand):
    hand_no = pai2onlyno(hand)
    openHand_no = pai2onlyno(openHand)
    ron = [False,False,False]
    qingyise = [0,1,2,3,4,5,6,7,8]
    for i in range(3):
        qingyisepai = [qys + 9*i for qys in qingyise]
        if_ron = True
        for oph in openHand_no:
            for op in oph:
                if(not op in qingyisepai):
                    if_ron = False
        for ha in hand_no:
            for h in ha:
                if(not h in qingyisepai):
                    if_ron = False
        if(if_ron):
            ron[i]= True
    if(True in ron):
        return True
    return False

#役满机会(非门前清限定！！！)

#役牌 大三元 包含中发白三组刻子 hand and openHand are list[list[(int,int)]]
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
        if(oph[0][0]==27):
            ron[0]=True
        if(oph[0][0]==28):
            ron[1]=True
        if(oph[0][0]==29):
            ron[2]=True
    if(not False in ron):
        return True
    else:
        return False

#役牌 字一色 只包含字牌 hand and openHand are list[list[(int,int)]]
def ziyise(hand,openHand):
    hand_no = pai2onlyno(hand)
    openHand_no = pai2onlyno(openHand)
    zipai = [27,28,29,30,31,32,33]
    for oph in openHand_no:
        for op in oph:
            if(not op in zipai):
                return False
    for hand in hand_no:
        for h in hand:
            if(not h in zipai):
                return False
    return True

#役牌 绿一色 只包含索子的23468以及发 hand and openHand are list[list[(int,int)]]
def lvyise(hand,openHand):
    hand_no = pai2onlyno(hand)
    openHand_no = pai2onlyno(openHand)
    lvpai = [19,20,21,23,25,28]
    for oph in openHand_no:
        for op in oph:
            if(not op in lvpai):
                return False
    for hand in hand_no:
        for h in hand:
            if(not h in lvpai):
                return False
    return True

#役牌 清老头 手牌中只有老头牌 hand and openHand are list[list[(int,int)]]
def qinglaotou(hand,openHand):
    hand_no = pai2onlyno(hand)
    openHand_no = pai2onlyno(openHand)
    laotou = [0,8,9,17,18,26]
    for oph in openHand_no:
        for op in oph:
            if(not op in laotou):
                return False
    for hand in hand_no:
        for h in hand:
            if(not h in laotou):
                return False
    return True

#役牌 小四喜 包含三种风牌的刻子+剩下一种风牌的雀头 hand and openHand are list[list[(int,int)]]
def xiaosixi(hand,openHand):
    hand_no = pai2onlyno(hand)
    openHand_no = pai2onlyno(openHand)
    fengpai = [30,31,32,33]
    xiaosixi = [0,0]
    for oph in openHand_no:
        if(oph[0] in fengpai):
            xiaosixi[0] = xiaosixi[0] + 1
    for hand in hand_no:
        if(len(hand)==3):
            if(hand[0] in fengpai):
                xiaosixi[0] = xiaosixi[0] + 1
        if(len(hand)==2):
            if(hand[0] in fengpai):
                xiaosixi[1] = xiaosixi[1] + 1
    if(xiaosixi[0]==3 and xiaosixi[1]==1):
        return True
    return False

#役牌 四杠子 hand and openHand are list[list[(int,int)]]
def sigangzi(hang,openHand):
    gz = 0 
    for oph in openHand:
        if(len(oph)==4):
            gz = gz + 1
    if(gz == 4):
        return True
    return False

#双倍役满机会(非门前清限定！！！)

#役牌 大四喜 包含四种风牌的刻子 hand and openHand are list[list[(int,int)]]
def dasixi(hand,openHand):
    hand_no = pai2onlyno(hand)
    openHand_no = pai2onlyno(openHand)
    fengpai = [30,31,32,33]
    dsx = 0
    for oph in openHand_no:
        if(oph[0] in fengpai):
            dsx = dsx + 1
    for hand in hand_no:
        if(len(hand)==3):
            if(hand[0] in fengpai):
                dsx = dsx + 1
    if(dsx == 4):
        return True
    return False


#门前役(指在门前清听牌为条件下，和牌才成立的役种)

#一番役(门前清限定！！！)
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

#二番役(门前清限定！！！)

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
#unfinished
def jiulianbaodeng(hand):
    return True



#helper function

#change list[list[(int,int)]] into list[list[int]]
def pai2onlyno(hand):
    honlyno = []
    for h in hand:
        if(len(h)==4):
            new_h = [h[0][0],h[1][0],h[2][0],h[3][0]]
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
   # kokusi = kokusi13machi(hand,openHand)
   # chitois = chitoi(hand,openHand)
   # piao = piao(hand,openHand,hand_num)
    return True
