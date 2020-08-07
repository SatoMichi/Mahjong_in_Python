import pytest
from Player import Player
from Pai import parsedPai, shorthand

t = Player("a",0)
t.changfeng = 30
t.zifeng = 31
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
    assert t.checkWait() == [parsedPai("1z")]


def test_checkJapanRon_sianke():
    hand = [(p,0) for p in parsedPai("222444m333555s2p")]
    t.setHand(hand)
    ron = t.checkRon((parsedPai("2p")[0],0))[1]
    assert ron.judgeRon == " 四暗刻"
    assert ron.zj == 32000
    assert ron.dj == 16000
    assert ron.xj == 8000

def test_checkJapanRon_yiqiguantong():
    hand = [(p,0) for p in parsedPai("23456789m11sccc")]
    t.setHand(hand)
    ron = t.checkRon((parsedPai("1m")[0],0))[1]
    print(ron.judgeRon)
    assert ron.judgeRon == " 一气贯通 役牌 中"

def test_checkJapanRon_qingyise():
    #[一筒,二筒,三筒,三筒,五筒,六筒,六筒,六筒,七筒,七筒,九筒,九筒,九筒]
    hand = [(p,0) for p in parsedPai("1234566677999m")]
    t.setHand(hand)
    ron = t.checkRon((parsedPai("3m")[0],0))[1]
    assert ron.judgeRon == " 清一色"

def test_checkJapanRon_sananke():
    hand = [(p,0) for p in parsedPai("66m34777pbbb222z")]
    t.setHand(hand)
    t.ifzhuang = False
    ron = t.checkRon((parsedPai("2p")[0],0))[1]
    assert ron.judgeRon == " 三暗刻 自风 役牌 白"