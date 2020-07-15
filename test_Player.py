import pytest
from Player import Player
from Pai import parsedPai, shorthand

t = Player("a",0)
# reference: http://arcturus.su/wiki/Machi

def test_checkWait_Ryanmen():
    hand = [(pai,0) for pai in parsedPai("23m112233s11122z")]
    t.setHand(hand)
    assert t.checkWait() == [[0,3]]
    
def test_checkWait_Penchan():
    hand = [(pai,0) for pai in parsedPai("45689m112233s22z")]
    t.setHand(hand)
    assert t.checkWait() == [[6]]
    
def test_checkWait_Shanpon():
    hand = [(pai,0) for pai in parsedPai("456789m123s1122z")]
    t.setHand(hand)
    assert t.checkWait() == [parsedPai("12z")]