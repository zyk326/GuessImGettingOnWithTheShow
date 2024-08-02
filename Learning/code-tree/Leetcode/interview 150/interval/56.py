# 合并区间

# 在这里先把初始值直接给赋值成第一个元素,然后在循环里重复判断第一个元素就好了,然后结尾处理最后一个结果

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals = sorted(intervals, key = lambda K:(K[0], K[1]))
        st, ed = intervals[0][0], intervals[0][1]
        n = len(intervals)
        ans = []
        for i in range(n):
            if ed >= intervals[i][0] and ed <= intervals[i][1]:
                ed = intervals[i][1]
                continue
            if ed < intervals[i][0]:
                ans.append([st, ed])
                st = intervals[i][0]
                ed = intervals[i][1]
        ans.append([st, ed])
        return ans
    
# leetcode版本

# 这里是一个方法论,判断条件精简进入就可以.

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key = lambda p : p[0])  # 这里只需要单点排序
        ans = []
        for p in intervals:
            if ans and p[0] <= ans[-1][1]:      # 这里判空 然后判加入条件,只需要新序列左端点小于ans的最远即可进入加入程序
                ans[-1][1] = max(ans[-1][1], p[1])   # 用max来判断最远是否更新,优雅
            else:
                ans.append(p)
        return ans