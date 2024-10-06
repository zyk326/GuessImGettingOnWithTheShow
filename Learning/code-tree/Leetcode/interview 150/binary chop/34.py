# 在排序数组中查找元素的第一个和最后一个位置

# 找这个数的第一个位置和比这个数大1的第一个位置
# yxc的板子就是垃圾

class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def search(target):
            l, r = 0, len(nums) - 1
            while l <= r:
                mid = (l + r) >> 1
                if nums[mid] < target:
                    l = mid + 1
                else:
                    r = mid - 1
            return l

        st = search(target)
        if st == len(nums) or nums[st] != target:
            return [-1, -1]
        ed = search(target + 1) - 1
        return [st, ed]
            