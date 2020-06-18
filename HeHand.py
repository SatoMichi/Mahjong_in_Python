import JudgeRon

class HeHand:
    def __init__(self,beforeHand,hand,openHand,hepai,zifeng,changfeng,angang,tumo):
        self.beforeHand = beforeHand    # [[(int,int)]]: hand which is not Open and does not include hepai
        self.hand = hand                # [[(int,int)]]: hand which is not Open and include hepai
        self.openHand = openHand        # [[(int,int)]]: Hand which is Open
        self.hepai = hepai              # (int,int): Pai which lead to 和
        self.zifeng = zifeng            # int: 自风
        self.changfeng = changfeng      # int: 长风
        self.angang = angang            # [Boolean]: if 1st 杠 in OpenHand is 暗杠 then angang[0] is True 
                                        #            if 2nd 杠 in OpenHand is 明杠 then angang[1] is False
        self.tumo = tumo                # Boolean: if 自摸 then True
    
    # if 自摸 return True
    def isTumo(self):
        return self.tumo
    # if 门前清 return True
    def isMenQing(self):
        return self.openHand == [] or all(self.angang):
    # if 门前清 and Not 自摸 return True
    def isMenQingRon(self):
        return self.isMenQing() and not self.isTumo()
    # if 门前清自摸 return True
    def isMenQingTumo(self):
        return self.isMenQing() and self.isTumo
    
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
        if open and len(paiset)==3 and self.duanYaoJiu(paiset):
            return (paiset,"明刻断幺九")
        elif open and len(paiset)==3 and not self.duanYaoJiu(paiset):
            return (paiset,"明刻2-8")
        elif not open and len(paiset)==3 and self.duanYaoJiu(paiset):
            return (paiset,"暗刻断幺九")
        elif not open and len(paiset)==3 and not self.duanYaoJiu(paiset):
            return (paiset,"暗刻2-8")
        elif open and len(paiset)==4 and self.duanYaoJiu(paiset) and not angang:
            return (paiset,"明杠断幺九")
        elif open and len(paiset)==4 and not self.duanYaoJiu(paiset) and not angang:
            return (paiset,"明杠2-8")
        elif open and len(paiset)==4 and self.duanYaoJiu(paiset) and angang:
            return (paiset,"暗杠断幺九")
        elif open and len(paiset)==4 and not self.duanYaoJiu(paiset) and angang:
            return (paiset,"暗杠2-8")
        else:
            return (paiset,"顺子")

    # helper function for judgeMianzi if paiset is 断幺九刻(杠)子 return True
    def duanYaoJiu(self,paiset):
        nums = [pai[0] for pai in paiset]
        isSame = len(set(nums)) == 1
        if isSame and nums[0] in [0,8,9,17,18,26,27,28,29,30,31,32,33]:
            return True

    # return 等牌的型 (嵌張聴,辺張聴,单钓)
    def judgeWaiting(self):
        # waiting 雀头
        if 1 in [len(paiset) for paiset in self.beforeHand]:
            return "单钓"
        # waiting paiset
        else:
            pentyan = [[0,1],[7,8],[9,10],[16,17],[18,19],[25,26]]
            shunzi = self.takeSunzi([len(paiset) for paiset in self.beforeHand if len(paiset)==2])
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