# 单词接龙

# 这题跟基因变换是一样的

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        def dist(a, b):
            return sum(1 if i != j else 0 for i, j in zip(a, b))
        
        if endWord not in wordList:
            return 0

        trans = defaultdict(list)
        for i, j in combinations(wordList + [beginWord], 2):
            if dist(i, j) == 1:
                trans[i].append(j)
                trans[j].append(i)
        
        que, explored, step = deque([beginWord]), {beginWord}, 1
        while que:
            lenth = len(que)
            for _ in range(lenth):
                cur = que.popleft()
                if cur == endWord:
                    return step
                for nxt in trans[cur]:
                    if nxt not in explored:
                        que.append(nxt)
                        explored.add(nxt)
            step += 1
        return 0