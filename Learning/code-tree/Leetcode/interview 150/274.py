# H指数

# 第一想到二分法
# 二分的板子有点不熟了
citations = list(map(int, input().split()))

n = len(citations)
l, r = 0, n - 1
while(l < r):
    mid = (l + r +  1) >> 1
    flag = check(mid)
    if flag:
        l = mid
    else:
        r = mid - 1

class Solution:
    def check(self, citations, mid):
        cnt = 0
        for i in citations:
            if i >= mid:
                cnt += 1
        return cnt >= mid

    def hIndex(self, citations: List[int]) -> int:
        l, r = 0, len(citations) - 1
        while(l < r):
            mid = (l + r + 1) >> 1
            flag = self.check(citations, mid)
            if flag:
                l = mid
            else:
                r = mid - 1
        return l