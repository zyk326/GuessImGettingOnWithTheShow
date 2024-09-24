# 环形子数组的最大和

# 不用数组拼接,直接用空间优化版的dp来做.
# 太精秒了

class Solution:
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        max_s, min_s = -inf, 0
        max_f, min_f = 0, 0
        for i in nums:
            max_f = max(max_f + i, i)
            min_f = min(min_f + i, i)

            max_s = max(max_s, max_f)
            min_s = min(min_s, min_f) 
        if min_s == sum(nums):
            return max_s
        return max(max_s, sum(num) - min_s) 


## 手写数组拼接,没通过
class Solution:
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        le = len(nums)
        nums = nums + nums
        dp = [0 for i in range(2 * le)]
        dp[0] = nums[0]
        j = 0
        for i in range(1, 2 * le):
            if dp[i - 1] < 0:
                dp[i] = nums[i]
                j = i
            else:
                dp[i] = dp[i - 1] + nums[i]
                while (i - j) >= le or nums[j] <= 0:
                    dp[i] -= nums[j]
                    j += 1
        return max(dp)