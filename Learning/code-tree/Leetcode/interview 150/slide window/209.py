# 长度最小的子数组

# 感觉是有点像那个双指针的感觉

# 进while循环,先判断条件时,起始条件为0, -1,判断完后,再做-1向的自加,再做结果的自加,但是要注意-1向的加法溢出.
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        minLen = float("inf")
        l, r = 0, -1
        winbuf = 0
        while(r != n):
            if winbuf >= target:
                minLen = min(minLen, r - l + 1)
                winbuf -= nums[l]
                l += 1
                continue
            r += 1
            if r < n:
                winbuf += nums[r]
        return minLen if minLen != float("inf") else 0