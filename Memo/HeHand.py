import Pai

class HeHand:
    def __init__(self,beforeHand,hand,openHand,hepai,zifeng,changfeng,angang,tumo):
        self.beforeHand = beforeHand    # [[(int,int)]]: hand which is not Open and does not include hepai
        self.hand = hand                # [[(int,int)]]: hand which is not Open and include hepai
        self.openHand = openHand        # [[(int,int)]]: Hand which is Open
        self.hepai = hepai              # (int,int): Pai which lead to 和
        self.zifeng = zifeng            # int: 自风
        self.changfeng = changfeng      # int: 场风
        self.angang = angang            # [Boolean]: if 1st 杠 in OpenHand is 暗杠 then angang[0] is True 
                                        #            if 2nd 杠 in OpenHand is 明杠 then angang[1] is False
        self.tumo = tumo                # Boolean: if 自摸 then True
    
    # if 自摸 return True
    def isTumo(self):
        return self.tumo
    # if 门前清 return True
    def isMenQing(self):
        isAllAngang = all(self.angang) and all([len(paiset)==4 for paiset in self.openHand])
        return self.openHand == [] or isAllAngang
    # if 门前清 and Not 自摸 return True
    def isMenQingRon(self):
        return self.isMenQing() and not self.isTumo()
    # if 门前清自摸 return True
    def isMenQingTumo(self):
        return self.isMenQing() and self.isTumo()
    
    # retrun id of 雀头
    def queTou(self):
        paiset = [paiset for paiset in self.hand if len(paiset)==2][0]
        paiId = paiset[0][0]
        return paiId
    
    # return list of 面子(paiset in OpenHand and Hand)
    def Mianzi(self):
        paisets = []
        gangCount = 0
        for paiset in self.openHand:
            if len(paiset) == 4:
                paisets.append(self.judgeMianzi(paiset,True,self.angang[gangCount]))
                gangCount += 1
            else:
                paisets.append(self.judgeMianzi(paiset,True,False))
        
        hand = [paiset for paiset in self.hand if not len(paiset)==2] # removed 雀头
        for paiset in hand:
            paiset.append(self.judgeMianzi(paiset,False,False))
        
        return paisets

    # helper function for Mianzi
    def judgeMianzi(self,paiset,open,angang):
        if open and len(paiset)==3 and self.isSame(paiset) and self.YaoJiu(paiset):
            return (paiset,"明刻幺九")
        elif open and len(paiset)==3 and self.isSame(paiset) and not self.YaoJiu(paiset):
            return (paiset,"明刻断幺九")
        elif not open and len(paiset)==3 and self.isSame(paiset) and self.YaoJiu(paiset):
            return (paiset,"暗刻幺九")
        elif not open and len(paiset)==3 and self.isSame(paiset) and not self.YaoJiu(paiset):
            return (paiset,"暗刻断幺九")
        elif open and len(paiset)==4 and self.isSame(paiset) and self.YaoJiu(paiset) and not angang:
            return (paiset,"明杠幺九")
        elif open and len(paiset)==4 and self.isSame(paiset) and not self.YaoJiu(paiset) and not angang:
            return (paiset,"明杠断幺九")
        elif open and len(paiset)==4 and self.isSame(paiset) and self.YaoJiu(paiset) and angang:
            return (paiset,"暗杠幺九")
        elif open and len(paiset)==4 and self.isSame(paiset) and not self.YaoJiu(paiset) and angang:
            return (paiset,"暗杠断幺九")
        else:
            return (paiset,"顺子")

    # helper function for judgeMianzi if paiset is 幺九刻(杠)子 return True
    def YaoJiu(self,paiset):
        nums = [pai[0] for pai in paiset]
        if nums[0] in [0,8,9,17,18,26,27,28,29,30,31,32,33]:
            return True
        else:
            return False
    # helper function for judgeMianzi if Paiset is not 顺子 return True
    def isSame(self,paiset):
        nums = [pai[0] for pai in paiset]
        return len(set(nums))==1
    
    # return 等牌的型 (嵌張聴,辺張聴,单钓)
    def judgeWaiting(self):
        # waiting 雀头
        if 1 in [len(paiset) for paiset in self.beforeHand]:
            return "单钓"
        # waiting paiset
        else:
            pentyan = [[0,1],[7,8],[9,10],[16,17],[18,19],[25,26]]
            shunzi = self.takeShunzi([paiset for paiset in self.beforeHand if len(paiset)==2])
            if shunzi == []:
                return "双碰"
            elif [pai[0] for pai in shunzi[0]] in pentyan:
                return "辺張"
            elif sum([pai[0] for pai in shunzi[0]])%2==0:
                return "嵌張"
            else:
                return "两面"
    
    # helper function for judgeWaiting
    def takeShunzi(self,paisets):
        paisetsCopy = paisets.copy()
        for paiset in paisets:
            if paiset[0][0] == paiset[1][0]:
                paisetsCopy.remove(paiset)
        return paisetsCopy

    def __str__(self):
        hand = []
        for s in self.beforeHand:
            for p in s:
                hand.append(p)
        ophand = []
        for s in self.openHand:
            for p in s:
                ophand.append(p)
        return Pai.showHand(hand) + Pai.showHand(ophand) + Pai.showHand([self.hepai])

if __name__ == "__main__":
    print("test 1: 门前清栄和，雀头：中， 暗杠幺九，单钓")
    beforehand = [[(27,0)],[(1,0),(2,1),(3,2)],[(6,0),(7,1),(8,2)],[(22,0),(23,1),(24,2)]]
    hepai = (27,1)
    afterhand = [[(27,0),(27,1)],[(1,0),(2,1),(3,2)],[(6,0),(7,1),(8,2)],[(22,0),(23,1),(24,2)]]
    ophand = [[(30,0),(30,1),(30,2),(30,3)]]
    angang = [True]
    zi = 30
    chang= 30
    tumo = False
    hehand = HeHand(beforehand,afterhand,ophand,hepai,zi,chang,angang,tumo)
    print(hehand)
    print("门前清自摸",hehand.isMenQingTumo())
    print(hehand.Mianzi())
    print(hehand.queTou())
    print(hehand.judgeWaiting())
    print("\n")

    print("test 2: 门前清栄和，雀头：中， 暗杠幺九，嵌張")
    beforehand = [[(27,0),(27,1)],[(1,0),(2,1),(3,2)],[(6,0),(7,1),(8,2)],[(22,0),(24,2)]]
    hepai = (23,1)
    afterhand = [[(27,0),(27,1)],[(1,0),(2,1),(3,2)],[(6,0),(7,1),(8,2)],[(22,0),(23,1),(24,2)]]
    ophand = [[(30,0),(30,1),(30,2),(30,3)]]
    angang = [True]
    zi = 30
    chang= 30
    tumo = False
    hehand = HeHand(beforehand,afterhand,ophand,hepai,zi,chang,angang,tumo)
    print(hehand)
    print("门前清自摸",hehand.isMenQingTumo())
    print(hehand.Mianzi())
    print(hehand.queTou())
    print(hehand.judgeWaiting())
    print("\n")

    print("test 3: 非门前清自摸，雀头：南， 暗杠幺九，辺張")
    beforehand = [[(32,0),(32,1)],[(6,0),(7,1),(8,2)],[(18,0),(19,2)]]
    hepai = (20,1)
    afterhand = [[(32,0),(32,1)],[(6,0),(7,1),(8,2)],[(22,0),(23,1),(24,2)]]
    ophand = [[(1,0),(2,1),(3,2)],[(30,0),(30,1),(30,2),(30,3)]]
    angang = [True]
    zi = 30
    chang= 30
    tumo = True
    hehand = HeHand(beforehand,afterhand,ophand,hepai,zi,chang,angang,tumo)
    print(hehand)
    print("门前清自摸",hehand.isMenQingTumo())
    print("自摸",hehand.isTumo())
    print(hehand.Mianzi())
    print(hehand.queTou())
    print(hehand.judgeWaiting())