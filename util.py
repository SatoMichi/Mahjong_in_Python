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
    
    # 面子
    if begin + 3 <= len(hand):
        if (
            hand[begin] + 1 == hand[begin+1] == hand[begin+2] -1 or
            hand[begin] == hand[begin+1] == hand[begin+2]
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
                hand[begin] + 1 == hand[begin+1] or 
                hand[begin] + 2 == hand[begin+1] 
            ):
                split.append([hand[begin],hand[begin+1]])
                dfs(hand,begin+2,melds,single,adj_tiles + 1,pairs,split,result)
                split.pop()
            if (
                hand[begin] == hand[begin+1]
            ):
                split.append([hand[begin],hand[begin+1]])
                dfs(hand,begin+2,melds,single,adj_tiles,pairs+1,split,result)
                split.pop()
    # 复合型(被隔开的顺子)
    while(begin <= len(hand) - 2):
        # find first different
        # find second different
        # copy hand and pop these, recurse on new hand
    


def tenpai(melds,single,adj_tiles,pairs):
    if melds == 3:
        return adj_tiles <= 1 and (adj_tiles + pairs) == 2 and single == 0
    if melds == 4:
        return single == 1
    return False

def is_shuntsu˜(hand,indexs):
    

if __name__ == "__main__":
    hand = [2,3,4,4,4,4,5,6,6,6,6,7,8]
    r = []
    s = []
    dfs(hand,0,0,0,0,0,s,r)
    print(r)