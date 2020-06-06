import Pai
import numpy as np
import itertools

def dfs(hand,begin, melds, single, adj_tiles, pairs, split,result):
    if begin == len(hand):
        if tenpai(melds,single,adj_tiles,pairs):
            # this is a viable split
            result.append(split[:])
        return
    # prune if tenpai can no longer be achieved
    if (
        single >=2 or adj_tiles >= 2 or
        adj_tiles + pairs > 2):
        return
    
    # 复合型(被隔开的顺子)
    if begin + 3 <= len(hand):
        indexs = find_sequence(hand,begin)
        if indexs is not None:
            if is_sequence(hand,indexs):
                split.append([hand[i] for i in indexs])
                # copy hand and pop
                hand_copy = hand[:]
                for i in sorted(indexs,reverse=True):
                    hand_copy.pop(i)
                dfs(hand_copy,begin,melds+1,single,adj_tiles,pairs,split,result)
                split.pop()
    
    # 面子
    if begin + 3 <= len(hand):
        indexs = list(range(begin,begin+3))
        if (
            is_3ofakind(hand,indexs)
        ):
            split.append([hand[begin],hand[begin+1],hand[begin+2]])
            dfs(hand,begin+3,melds+1,single,adj_tiles,pairs,split,result)
            split.pop()

    # 1 分出孤张，继续搜索
    if begin + 1 <= len(hand):
        if single == 0 and adj_tiles + pairs == 0:
            # explore deeper
            split.append([hand[begin]])
            dfs(hand,begin+1,melds,single + 1,adj_tiles,pairs,split,result) 
            # roll back
            split.pop()
    
    # 2 分出搭子或对子        
    if begin + 2 <= len(hand):
        if single == 0 and pairs <= 2 and adj_tiles + pairs <= 2:
            # 搭子
            if (
                is_seq2(hand,[begin,begin+1])
            ):
                split.append([hand[begin],hand[begin+1]])
                dfs(hand,begin+2,melds,single,adj_tiles + 1,pairs,split,result)
                split.pop()
            if (
                is_pair(hand,[begin,begin+1])
            ):
                split.append([hand[begin],hand[begin+1]])
                dfs(hand,begin+2,melds,single,adj_tiles,pairs+1,split,result)
                split.pop()
                
    
    


def tenpai(melds,single,adj_tiles,pairs):
    if melds == 3:
        return adj_tiles <= 1 and (adj_tiles + pairs) == 2 and single == 0
    if melds == 4:
        return single == 1
    return False

def is_sequence(hand,indexs):
    """
    example: is_shuntsu([一万，二万，二万，三万]，[0,2,3]) == True
    """
    h = [Pai.paiSet[i] for i in hand]
    if len(indexs) != 3:
        return False
    a,b,c = indexs
    # 花色相等而且不是字牌
    if all(h[a].suit ==h[i].suit for i in indexs):
        if h[a].num != -1 and h[a].num + 1 == h[b].num == h[c].num - 1:
            return True
    return False

def is_3ofakind(hand,indexs):
    if len(indexs) != 3:
        return False
    a,b,c = indexs
    if hand[a][0] == hand[b][0] == hand[c][0]:
        return True
    return False

def is_seq2(hand,indexs):
    if len(indexs) != 2:
        return False
    h = [Pai.paiSet[i] for i in hand]
    a,b = indexs
    if (
        h[a].suit == h[b].suit and 
        h[a].num != -1 and 
        h[a].num+1 == h[b].num
    ):
        return True
    return False

def is_pair(hand,indexs):
    if len(indexs) != 2:
        return False
    return hand[indexs[0]][0] == hand[indexs[1]][0]

def find_sequence(hand,begin):
    a = b = c = begin
    # find first different
    for i in range(a,len(hand)-1):
        if hand[i][0] != hand[a][0]:
            b = i
            break
    for i in range(b,len(hand)):
        if hand[i][0] != hand[b][0]:
            c =i
            break
    if is_sequence(hand,[a,b,c]):
        return [a,b,c]
    else:
        return None




if __name__ == "__main__":
    hand = [(2,0),(3,0),(4,0),(4,1),(4,2),(4,3),(5,0),(6,0),(6,1),(6,2),(6,3),(7,0),(8,0)]
    r = []
    s = []
    dfs(hand,0,0,0,0,0,s,r)
    