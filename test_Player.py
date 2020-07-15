import pytest
from Player import Player
from Pai import parsedPai, shorthand

t = Player("a",0)

def test_checkWait():
    t.setHand(parsedPai("23m112233s11122z"))
    assert t.checkWait == [[0,3]]