import unittest
from unittest.mock import patch
from Player import Player

class PlayerTestMin(unittest.TestCase):
    def setUp(self):
        self.player_0 = Player("empty",0)
        
        self.player_1 = Player("a",0)
        self.hand_1 = [(29,1),(29,2),(31,1),(31,2),(1,0),(1,1),(2,2),(4,3),(5,0),(8,1),(9,2),(0,2),(0,3)]
        self.player_1.setHand(self.hand_1)

        #玩家想要吃四筒,系统需要给出提示询问以非红宝牌五筒的形式吃进or以红宝牌五筒的形式吃进
        #{中，中，中，三筒，三筒，五筒，五筒(红)，五筒，二索，三索，五索，一万，四万}
        self.player_2 = Player("b",0)
        self.hand_2 = [(27,0),(27,1),(27,3),(11,3),(11,1),(13,0),(13,1),(13,2),(19,0),(20,1),(22,2),(0,2),(3,1)]
        self.player_2.setHand(self.hand_2)

        #上家打出八索,系统不应作出任何反应(八索，九索，中 不能组成顺子即使数字连在一起)
        #上家打出北风,系统不应作出任何反应(南风，西风，北风 不能组成顺子即使数字连在一起)
        #{九索，中，白，白，发，发，东风，东风，东风，西风，西风，南风，南风}
        self.player_3 = Player("c",0)
        self.hand_3 = [(26,1),(27,1),(28,3),(28,2),(29,1),(29,0),(30,1),(30,2),(30,0),(32,1),(32,2),(33,2),(33,1)]
        self.player_3.setHand(self.hand_3)

        #上家打出八万,系统不应作出任何反应(八万，九万，一筒 不能组成顺子即使数字连在一起)
        #{九万，九万，一筒，五索，五索，三索，六筒，三筒，中，九索，东风，东风，东风}
        self.player_4 = Player("d",0)
        self.hand_4 = [(8,1),(8,0),(9,1),(22,0),(22,2),(20,0),(14,3),(11,1),(27,1),(26,2),(30,1),(30,2),(30,0)] 
        self.player_4.setHand(self.hand_4)

        #上家打出六万,系统应询问的吃进方式有:五万-七万，四万五万-，-七万，八万
        #{二万，二万，二万，三万，四万，五万，五万，六万，七万，七万，八万，九万，九万}
        self.player_5 = Player("e",0)
        self.hand_5 = [(1,1),(1,0),(1,2),(2,1),(3,2),(4,1),(4,2),(5,2),(6,2),(6,0),(7,1),(8,0),(8,1)]
        self.player_5.setHand(self.hand_5)

        #玩家想要吃三索,系统不应询问直接吃入
        #{三万，四万，五万，一索，一索，二索，二索，四筒，五筒，六筒，东风，东风，东风}
        self.player_6 = Player("f",0)
        self.hand_6 = [(2,1),(3,0),(4,2),(18,0),(18,2),(19,2),(19,1),(12,1),(13,2),(14,0),(30,1),(30,2),(30,0)]
        self.player_6.setHand(self.hand_6)    
    
    @patch('builtins.input', lambda *args: '0')
    def testMutipleChi(self):
        """
        test multiple chi, select first with @patch
        """
        r = self.player_1.chi((3,0))
        self.assertEqual(r,"chi")
        self.hand_1.pop(7)
        self.hand_1.pop(6)
        self.assertEqual(self.player_1.hand,sorted(self.hand_1))
        self.assertEqual(self.player_1.openHand["chi"],[[(2,2),(4,3),(3,0)]])


    #def testMutipleChiwith(self):

    
    def testPon(self):
        r= self.player_1.pon((29,0))
        self.assertEqual(r,"pon")
        self.assertEqual(self.player_1.hand,sorted(self.hand_1[2:]))
        self.assertEqual(self.player_1.openHand["pon"],[[(29,1),(29,2),(29,0)]])
    
    def testGetAllHand(self):
        hand = [(29,1),(29,2),(1,0),(1,1),(2,2),(2,3),(8,0),(8,1),(0,2),(0,3)]
        openHand = [(31,1),(31,2),(31,0)]
        self.player_0.setHand(hand)
        self.player_0.openHand["pon"] = openHand
        r = self.player_0.getAllHand()
        self.assertEqual(r, sorted(hand + openHand))
        
        
    def testAskRiichiFalse(self):
        r = self.player_1.askRiichi()
        self.assertEqual(r,False)
        
    @patch('builtins.input', lambda *args: ' ')
    def testAskRiichiSelectTrue(self):
        hand = [(29,1),(29,2),(1,0),(1,1),(2,2),(2,3),(2,0),(0,1),(0,2),(0,3)]
        openHand = [(31,1),(31,2),(31,0)]
        self.player_0.setHand(hand)
        self.player_0.openHand["pon"] = openHand
        r = self.player_0.askRiichi()
        self.assertEqual(r, True)
        
if __name__ == '__main__':
    unittest.main()