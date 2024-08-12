# 最小基因变化

# 这里涉及到一个python的用法:combinations
# 还有一个看到就知道用BFS的思路,找最短路径
# 这里构造图用的是combinations函数,利用变化仅1来构造图

class Solution:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:
        def dist(a, b):
            return sum(1 if i != j else 0 for i, j in zip(a, b))
        
        if endGene not in bank:
            return -1
        
        trans = defaultdict(list)
        for a, b in combinations(bank + [startGene], 2):
            if dist(a, b) == 1:
                trans[a].append(b)
                trans[b].append(a)
        
        queue, explore, step = deque([startGene]), {startGene}, 0

        while queue:
            lenth = len(queue)
            for _ in range(lenth):
                cur = queue.popleft()
                if cur == endGene:
                    return step
                for nxt in trans[cur]:
                    if nxt not in explore:
                        explore.add(nxt)
                        queue.append(nxt)
            step += 1
        return -1