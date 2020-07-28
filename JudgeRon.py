from Pai import originalYama,allPai,showHand
import numpy as np
import yaml
import math


#    label = {'一萬': 0, '二萬': 1, '三萬': 2, '四萬': 3, '五萬': 4, '六萬': 5, '七萬': 6, '八萬': 7, '九萬': 8,
#             '一筒': 9, '二筒': 10, '三筒': 11, '四筒': 12, '五筒': 13, '六筒': 14, '七筒': 15, '八筒': 16, '九筒': 17,
#             '一索': 18, '二索': 19, '三索': 20, '四索': 21, '五索': 22, '六索': 23, '七索': 24, '八索': 25, '九索': 26,
#             '中': 27, '發': 28, '白': 29, '東': 30, '西': 31, '南': 32, '北': 33}


#十三幺//国士无双Ron hand and openHand are list[list[(int,int)]]
#十三幺分牌规则有待商榷****
def kokusi13machi(hand):
#    yao13 = [0,8,9,17,18,26,27,28,29,30,31,32,33]
#    ron = (len(hand) == 14) and (len(openHand)==0)
#    for p in yao13:
#        ron = ron and p in [str(h) for h in hand]
   return False

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
def sigangzi(hand,openHand):
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

#役牌 门前清自摸和 门前清的状态下自摸和牌

#役牌 平和 四组顺子+非役牌的雀头+最后是顺子的两面听牌 hand is list[list[(int,int)]] hepai is (int,int)
def pinghe(beforehand,hand,hepai,zifeng,changfeng):
    hand_no = pai2onlyno(hand)
    beforehand_no = pai2onlyno(beforehand)
    shunzi = 0
    liangmian = False
    yipai = True
    sanyuan = [27,28,29]
    bianzhangxiao = [0,9,18]
    bianzhangda = [8,17,26]
    for hand in hand_no:
        if(len(hand)==3):
            if(hand[0]==hand[1]-1):
                shunzi = shunzi + 1
        if(len(hand)==2):
            if(hand[0] == zifeng or hand[0] == changfeng or hand[0] in sanyuan):
                    yipai = False
    for beforehand in beforehand_no:
        if(len(beforehand)==2):
            if(beforehand[0]==beforehand[1]-1 and (not beforehand[0] in bianzhangxiao) and (not beforehand[1] in bianzhangda)):
                liangmian = True
    if(shunzi == 4 and liangmian and yipai):
        return True       
    return False

#役牌 一杯口 hand is list[list[(int,int)]]
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

#三番役(门前清限定！！！)

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
    hand_no = pai2onlyno(hand)
    all_hand = []
    for bh in hand_no:
        all_hand = all_hand + bh
    all_hand.sort()
    jiul = [[0,0,0,0,1,2,3,4,5,6,7,8,8,8],[0,0,0,1,1,2,3,4,5,6,7,8,8,8],[0,0,0,1,2,2,3,4,5,6,7,8,8,8],[0,0,0,1,2,3,3,4,5,6,7,8,8,8],
    [0,0,0,1,2,3,4,4,5,6,7,8,8,8],[0,0,0,1,2,3,4,5,5,6,7,8,8,8],[0,0,0,1,2,3,4,5,6,6,7,8,8,8],[0,0,0,1,2,3,4,5,6,7,7,8,8,8],
    [0,0,0,1,2,3,4,5,6,7,8,8,8,8]]
    for i in range(3):
        jiulian = [[j + 9 * i for j in jiu] for jiu in jiul]
        if(all_hand in jiulian):
            return True
    return False

#门前清双倍役满机会
#役牌 纯正九莲宝灯 hand and openHand are list[list[(int,int)]] 
def czjiulianbaodeng(beforehand):
    beforehand_no = pai2onlyno(beforehand)
    all_beforehand = []
    for bh in beforehand_no:
        all_beforehand = all_beforehand + bh
    for i in range(3):
        jiulian = [0+9*i,0+9*i,0+9*i,1+9*i,2+9*i,3+9*i,4+9*i,5+9*i,6+9*i,7+9*i,8+9*i,8+9*i,8+9*i]
        if(all_beforehand == jiulian):
            return True
    return False



#helper function

#change list[list[(int,int)]] into list[list[int]]
def pai2onlyno(hand):
    honlyno = []
    for h in hand:
        if(len(h)==4):
            new_h = [h[0][0],h[1][0],h[2][0],h[3][0]]
        elif(len(h)==3):
            new_h = [h[0][0],h[1][0],h[2][0]]
        elif(len(h)==2):
            new_h = [h[0][0],h[1][0]]
        else:
            new_h = [h[0][0]]
        honlyno.append(new_h)
    return honlyno

#take all the shunzi out of hand
def takeShunzi(paisets):
        paisetsCopy = paisets.copy()
        for paiset in paisets:
            if paiset[0][0] == paiset[1][0]:
                paisetsCopy.remove(paiset)
        return paisetsCopy

#calculate fu 
def calcultatefu(hand,openHand,beforeHand,tumo,hepai,zifeng,changfeng):
    yaojiu = [0,8,9,17,18,26,27,28,29,30,31,32,33]
    sanyuan = [27,28,29]
    #符底一定会有二十符
    fu = 20
    hand_no = pai2onlyno(hand)
    openHand_no = pai2onlyno(openHand)
    for oph in openHand_no:
        if(len(oph)==4):
            if(oph[2]==oph[3]):
                if(oph[0] in yaojiu):
                    fu = fu + 16
                else:
                    fu = fu + 8
            else:
                if(oph[0] in yaojiu):
                    fu = fu + 32
                else:
                    fu = fu + 16
        if(len(oph)==3 and oph[0]==oph[1] and oph[1]==oph[2]):
            if(oph[0] in yaojiu):
                fu = fu + 4
            else:
                fu = fu + 2
    for hand in hand_no:
        if(len(hand)==3):
            if(hand[0]==hand[1] and hand[1]==hand[2]):
                if(hand[0] in yaojiu):
                    fu = fu + 8
                else:
                    fu = fu + 4
        if(len(hand)==2):
            if(hand[0] in sanyuan):
                fu = fu + 2
            if(hand[0] == zifeng or hand[0] == changfeng):
                fu = fu + 2
                if(zifeng == changfeng):
                    fu = fu + 2
    #自摸加2两符,七对子不加
    if(tumo):
        if(not chitoi(hand)):
            fu = fu + 2
    #门前荣和加10符
    if(not tumo):
        if(openHand == None):
            fu = fu + 10
    #单钓听牌加2符
    if(1 in [len(bH) for bH in beforeHand]):
        fu = fu + 2
    else:
        pentyan = [[0,1],[7,8],[9,10],[16,17],[18,19],[25,26]]
        shunzi = takeShunzi([paiset for paiset in beforeHand if len(paiset)==2])
        if shunzi == []: # shunzi could be empty (双碰)
            pass
        #边张加2符
        elif([pai[0] for pai in shunzi[0]] in pentyan):
            fu = fu + 2
        #嵌张加2符
        elif(sum([pai[0] for pai in shunzi[0]])%2==0):
            fu = fu + 2
    fus = fu / 10
    fus = math.ceil(fus)
    fu = fus * 10
    #七对子的符数一定是25符
    if(chitoi(hand)):
        fu = 25
    #平和自摸的牌一定是20符
    if(pinghe(beforeHand,hand,hepai,zifeng,changfeng) and tumo):
        fu = 20
    return fu

class Rondong:
    def __init__(self):
        self.zj = 0     #自家得到的分数
        self.xj = 0     #闲家得到的分数
        self.judgeRon = ""      #和牌包含的役
        self.fan = 0    #和牌的翻数
        self.fu = 0     #和牌的符数
        self.levelrep = ""  #和牌的翻数 string形式
    def addfan(self,n):
        self.fan = self.fan + n
    def setJudgeRon(self,stri):
        self.judgeRon = self.judgeRon + " " + stri
    #为了应对因为副露而出现的减番情况
    def minusfan(self):
        self.fan = self.fan - 1
    def calcultateFu(self,hand,openHand,beforeHand,tumo,hepai,zifeng,changfeng):
        self.fu = calcultatefu(hand,openHand,beforeHand,tumo,hepai,zifeng,changfeng)
    def setallup(self):
        file = open("roncalculatedong.yml",'r',encoding="utf-8")
        file_data = file.read()
        file.close()
        data = yaml.load(file_data,Loader=yaml.FullLoader)
        if(self.fan == 5 or (self.fan == 4 and self.fu>30) or (self.fan == 3 and self.fu>60)):
            self.zj = 12000
            self.xj = 4000
            self.levelrep = "满贯"
        elif(self.fan == 6 or self.fan == 7):
            self.zj = 18000
            self.xj = 6000
            self.levelrep = "跳满" 
        elif(self.fan == 8 or self.fan == 9 or self.fan == 10):
            self.zj = 24000
            self.xj = 8000
            self.levelrep = "倍满"
        elif(self.fan == 11 or self.fan == 12):
            self.zj = 36000
            self.xj = 12000
            self.levelrep = "三倍满"
        #累计役满即为Player单次所能获得的最大的牌
        elif(self.fan >= 13):
            self.zj = 48000
            self.xj = 16000
            self.levelrep = "累计役满"
        else:
            fanshu = 'fanshu' + str(self.fan)
            fushu = 'fushu' + str(self.fu)
            self.zj = data['point'][0][fanshu][0][fushu][0]['defen']
            self.xj = data['point'][0][fanshu][0][fushu][0]['shifen']
            self.levelrep = str(self.fan) + "翻"

class Ronxian:
    def __init__(self):
        self.zj = 0     #自家得到的分数
        self.dj = 0     #东家丢失的分数
        self.xj = 0     #闲家丢失的分数
        self.judgeRon = ""      #和牌中包含的役
        self.fan = 0    #和牌的番数
        self.fu = 0     #和牌的符数
        self.levelrep = ""      #和牌的翻数 string形式
    def addfan(self,n):
        self.fan = self.fan + n
    def setJudgeRon(self,stri):
        self.judgeRon = self.judgeRon + " " + stri
    #为了应对因为副露而出现的减番情况
    def minusfan(self):
        self.fan = self.fan - 1
    def calcultateFu(self,hand,openHand,beforeHand,tumo,hepai,zifeng,changfeng):
        self.fu = calcultatefu(hand,openHand,beforeHand,tumo,hepai,zifeng,changfeng)
    def setallup(self):
        file = open("roncalculatedong.yml",'r',encoding="utf-8")
        file_data = file.read()
        file.close()
        data = yaml.load(file_data,Loader=yaml.FullLoader)
        if(self.fan == 5 or (self.fan == 4 and self.fu>30) or (self.fan == 3 and self.fu>60)):
            self.zj = 8000
            self.xj = 2000
            self.dj = 4000
            self.levelrep = "满贯"
        elif(self.fan == 6 or self.fan == 7):
            self.zj = 12000
            self.xj = 3000
            self.dj = 6000
            self.levelrep = "跳满" 
        elif(self.fan == 8 or self.fan == 9 or self.fan == 10):
            self.zj = 16000
            self.xj = 4000
            self.dj = 8000
            self.levelrep = "倍满"
        elif(self.fan == 11 or self.fan == 12):
            self.zj = 24000
            self.xj = 6000
            self.dj = 12000
            self.levelrep = "三倍满"
        elif(self.fan >= 13):
            self.zj = 32000
            self.xj = 8000
            self.dj = 16000
            self.levelrep = "累计役满"
        else:
            fanshu = 'fanshu' + str(self.fan)
            fushu = 'fushu' + str(self.fu)
            self.zj = data['point'][0][fanshu][0][fushu][0]['defen']
            self.dj = data['point'][0][fanshu][0][fushu][0]['dongshifen']
            self.xj =  data['point'][0][fanshu][0][fushu][0]['xianshifen']
            self.levelrep = str(self.fan) + "翻"

#日本麻将胡牌函数
#hand 为 list[list[(int,int)]],openHand 为 list[list[(int,int)]]
#lichi为booolean,为了判断Player是否立直
#zifeng和changfeng均为int,[30--33](表示本场游戏的自风与场风)
def JapanRon(player):
    ifzhuang = player.ifzhuang
    if(ifzhuang):
        ron = Rondong()
    else:
        ron = Ronxian()
    hand = player.hand
    openHand = player.openHand
    changfeng = player.changfeng
    lichi = player.lichi
    beforehand = player.beforehand
    hepai = player.hepai
    tumo = player.tumo
    if(openHand == None):
        #Player 先判断门前清番数
        #双倍役满机会(目前暂时认为役满即为最大分值,不支持双倍役满翻番)
        if(czjiulianbaodeng(beforehand)):
            ron.addfan(13)
            ron.setJudgeRon("纯正九莲宝灯")
            ron.setallup()
            return ron
        #直接役满机会 此时可以直接return
        if(sianke(hand)):
            ron.addfan(13)
            ron.setJudgeRon("四暗刻")
            ron.setallup()
            return ron
        if(kokusi13machi(hand)):
            ron.addfan(13)
            ron.setJudgeRon("国士无双")
            ron.setallup()
            return ron
        if(jiulianbaodeng(hand)):
            ron.addfan(13)
            ron.setJudgeRon("九莲宝灯")
            ron.setallup()
            return ron
        #三番役机会
        if(erbeikou(hand)):
            ron.addfan(3)
            ron.setJudgeRon("二杯口")
        #二番役机会
        if(chitoi(hand)):
            ron.addfan(2)
            ron.setJudgeRon("七对子")
        #一番役机会
        if(yibeikou(hand)):
            ron.addfan(1)
            ron.setJudgeRon("一杯口")
        if(pinghe(beforehand,hand,hepai,zifeng,changfeng)):
            ron.addfan(1)
            ron.setJudgeRon("平和")
        if(lichi):
            ron.addfan(1)
            ron.setJudgeRon("立直")
        if(tumo):
            ron.addfan(1)
            ron.setJudgeRon("门前清自摸和")
    #所有牌型均需要判断非门前清的情况
    #双倍役满机会(目前暂时认为役满即为最大分值,不支持双倍役满翻番)
    if(dasixi(hand,openHand)):
        ron.addfan(13)
        ron.setJudgeRon("大四喜")
        ron.setallup()
        return ron
    #役满机会
    if(dasanyuan(hand,openHand)):
        ron.addfan(13)
        ron.setJudgeRon("大三元")
        ron.setallup()
        return ron
    if(ziyise(hand,openHand)):
        ron.addfan(13)
        ron.setJudgeRon("字一色")
        ron.setallup()
        return ron
    if(lvyise(hand,openHand)):
        ron.addfan(13)
        ron.setJudgeRon("绿一色")
        ron.setallup()
        return ron
    if(qinglaotou(hand,openHand)):
        ron.addfan(13)
        ron.setJudgeRon("清老头")
        ron.setallup()
        return ron
    if(xiaosixi(hand,openHand)):
        ron.addfan(13)
        ron.setJudgeRon("小四喜")
        ron.setallup()
        return ron
    if(sigangzi(hand,openHand)):
        ron.addfan(13)
        ron.setJudgeRon("四杠子")
        ron.setallup()
        return ron
    #六番机会
    if(qingyise(hand,openHand)):
        ron.addfan(6)
        #副露减番
        if(not openHand == None):
            ron.minusfan()
        ron.setJudgeRon("清一色")
    #三番机会
    if(cqdyj(hand,openHand)):
        ron.addfan(3)
        #副露减番
        if(not openHand == None):
            ron.minusfan()
        ron.setJudgeRon("纯全带幺九")
    if(hunyise(hand,openHand)):
        ron.addfan(3)
        #副露减番
        if(not openHand == None):
            ron.minusfan()
        ron.setJudgeRon("混一色")
    #二番机会
    if(sansetk(hand,openHand)):
        ron.addfan(2)
        ron.setJudgeRon("三色同刻")
    if(sangangzi(hand,openHand)):
        ron.addfan(2)
        ron.setJudgeRon("三杠子")
    if(piao(hand,openHand)):
        ron.addfan(2)
        ron.setJudgeRon("对对和")
    if(sananke(hand,openHand)):
        ron.addfan(2)
        ron.setJudgeRon("三暗刻")
    if(xiaosanyuan(hand,openHand)):
        ron.addfan(2)
        ron.setJudgeRon("小三元")
    if(hunlaotou(hand,openHand)):
        ron.addfan(2)
        ron.setJudgeRon("混老头")
    if(hqdyj(hand,openHand)):
        ron.addfan(2)
        #副露减番
        if(not openHand == None):
            ron.minusfan()
        ron.setJudgeRon("混全带幺九")
    if(yiqiguantong(hand,openHand)):
        ron.addfan(2)
        #副露减番
        if(not openHand == None):
            ron.minusfan()
        ron.setJudgeRon("一气贯通")
    if(sansets(hand,openHand)):
        ron.addfan(2)
        #副露减番
        if(not openHand == None):
            ron.minusfan()
        ron.setJudgeRon("三色同顺")
    #一番机会
    if(noyaojiu(hand,openHand)):
        ron.addfan(1)
        ron.setJudgeRon("断幺九")
    if(zifeng(hand,openHand,zifeng)):
        ron.addfan(1)
        ron.setJudgeRon("自风")
    if(changfeng(hand,openHand,changfeng)):
        ron.addfan(1)
        ron.setJudgeRon("场风")
    if(sanyuan_fa(hand,openHand)):
        ron.addfan(1)
        ron.setJudgeRon("役牌 发")
    if(sanyuan_bai(hand,openHand)):
        ron.addfan(1)
        ron.setJudgeRon("役牌 白")
    if(sanyuan_zhong(hand,openHand)):
        ron.addfan(1)
        ron.setJudgeRon("役牌 中")
    ron.calcultateFu(hand,openHand,beforehand,tumo,hepai,zifeng,changfeng)
    ron.setallup()
    return ron