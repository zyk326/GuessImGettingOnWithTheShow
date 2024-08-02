# 插入区间

class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        def merge(intervals: List[List[int]]) -> List[List[int]]:
            ans = []
            intervals.sort(key = lambda p:p[0])
            for i in intervals:
                if ans and ans[-1][1] >= i[0]:
                    ans[-1][1] = max(ans[-1][1], i[1])
                else:
                    ans.append([i[0], i[1]])
            return ans
        intervals.append(newInterval)
        return merge(intervals)