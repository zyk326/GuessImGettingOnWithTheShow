# 汇总区间

# 再强调一遍,边界条件要看清楚

class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        ans = []
        st, ed = -1, -1
        i = 0
        n = len(nums)
        while(i < n):
            st = i
            j = 1
            while(st + j < n and nums[st + j] == nums[st] + j):
                ed = st + j
                j += 1
            ans.append(str(nums[st]) + (("->" + str(nums[ed])) if st < ed else ""))
            i += j
        return ans