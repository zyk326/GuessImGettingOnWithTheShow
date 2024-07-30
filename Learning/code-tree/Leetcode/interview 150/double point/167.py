# 两数之和ii -输入有序数组

# 没啥好说的,很简单的双指针

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        l, r = 0, len(numbers) - 1
        while(l < r):
            buf = numbers[l] + numbers[r]
            if buf == target:
                return [l + 1, r + 1]
            if buf > target:
                r -= 1
            if buf < target:
                l += 1
        return [-1, -1]