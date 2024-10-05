# 寻找峰值

# 太精妙了,比mid大的那一边一定有波峰

# 因为你这是上取整,涉及到上取整就要调整题目里的判断位置,因为有的地方你没有值.

class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        while l < r:
            mid = (l + r + 1) >> 1
            if nums[mid] < nums[mid - 1]:
                r = mid - 1
            else:
                l = mid
        return l