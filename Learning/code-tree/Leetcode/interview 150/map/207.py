# 课程表

# 一个判断有无环的问题,思路是 用拓扑图的思想来判断 建立图,用入度来判断每次加入队列的元素.

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        g = defaultdict(list)
        indug = [0] * numCourses
        for a, b in prerequisites:
            g[b].append(a)
            indug[a] += 1
        
        res = 0
        q = deque(i for i, j in enumerate(indug) if j == 0)
        while q:
            i = q.popleft()
            res += 1
            for j in g[i]:
                indug[j] -= 1
                if indug[j] == 0: q.append(j)
        return res == numCourses