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

def test_checkWait_tenpai():
    hand = [(p,0) for p in parsedPai("112233556677s1z")]
    t.setHand(hand)
    assert t.checkWait() == [[parsedPai("1z")]]

def test_checkRon_tenpai():
    hand = [(p,0) for p in parsedPai("112233556677s1z")]
    t.setHand(hand)
    assert t.checkRon((30,0))[0] == True

def test_checkJapanRon_duiduihe():
    hand = [(p,0) for p in parsedPai("222444m333555s2p")]
    t.changfeng = 30
    t.zifeng = 31
    t.setHand(hand)
    ron = t.checkRon((parsedPai("2p")[0],0))[1]
    assert ron.judgeRon == " 对对和 断幺九"
    assert ron.zj == 5200
    assert ron.dj == 2600
    assert ron.xj == 1300

def test_checkJapanRon_yiqiguantong():
    hand = [(p,0) for p in parsedPai("23456789m11sccc")]
    t.changfeng = 30
    t.zifeng = 31
    t.setHand(hand)
    ron = t.checkRon((parsedPai("1m")[0],0))[1]
    print(ron.judgeRon)
    assert ron.judgeRon == " 一气贯通"