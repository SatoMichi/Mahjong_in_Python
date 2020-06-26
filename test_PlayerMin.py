import unittest
from unittest.mock import patch
from Player import Player

class PlayerTestMin(unittest.TestCase):
    def setUp(self):
        self.player = Player("a",0)
        hand = [(29,1),(29,2),(31,1),(31,2),(1,0),(1,1),(2,2),(4,3),(5,0),(8,1),(9,2),(0,2),(0,3)]
        self.player.setHand(hand)
    
    @patch('builtins.input', lambda *args: '0')
    def testChi(self):
        r = self.player.chi((3,0))
        self.assertEqual(r,"chi")
        self.assertEqual(self.player.openHand["chi"],[[(2,2),(4,3),(3,0)]])
        
        
if __name__ == '__main__':
    unittest.main()