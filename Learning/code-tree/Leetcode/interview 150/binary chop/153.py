# 寻找旋转排序数组中的最小值

# 判断条件要求精简,有多余条件会导致部分数字筛选不正确

class Solution:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        while l < r:
            mid = (l + r) >> 1
            if nums[mid] > nums[r]:
                l = mid + 1
            else:
                r = mid
        return nums[l]
