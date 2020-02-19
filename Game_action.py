from Pai import originalYama
import numpy as np

def getFirstHand(yama):
    return yama[0:13], yama[13:26], yama[26:39], yama[39:52], yama[52:]

def justCut(hand):
    cut = hand[-1]
    hand = hand[:-1]
    return hand,cut

def decideCut(hand):
    hand = np.random.permutation(hand)
    cut = hand[-1]
    hand = hand[:-1]
    return hand,cut
