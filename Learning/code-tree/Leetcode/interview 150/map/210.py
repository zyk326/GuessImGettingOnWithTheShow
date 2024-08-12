# 课程表ii

# 很神奇的入度出度的问题

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        res = []
        g = defaultdict(list)
        endug = [0] * numCourses
        for a, b in prerequisites:
            g[b].append(a)
            endug[a] += 1
        
        q = deque(i for i, j in enumerate(endug) if j == 0)
        while q:
            node = q.popleft()
            res.append(node)
            for i in g[node]:
                endug[i] -= 1
                if endug[i] == 0:
                    q.append(i)
        print(res)
        return res if len(res) == numCourses else []