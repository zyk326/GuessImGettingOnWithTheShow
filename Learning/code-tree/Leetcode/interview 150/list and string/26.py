# 删除有序数组中的重复项

# 双指针的解法,初始状态直接就是1,直接判下一个数字

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        j = 0
        k = 1
        for i in range(1, len(nums)):
            if nums[i] == nums[j]:
                nums[i] = float("INF")
                continue
            k += 1
            j = i
        nums.sort()
        return k
        