# 最大子数组和
# kadane算法就是用动态规划来解决最大子数组和的问题的解法
# 这里涉及到一个空间优化

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        dp = [0 for i in range(len(nums))]
        dp[0] = nums[0]
        for i in range(1, len(nums)):
            if dp[i - 1] >= 0:
                dp[i] = dp[i - 1] + nums[i]
            else:
                dp[i] = nums[i]
        return max(dp)

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        size = len(nums)
        pre = 0  # 存储当前的最大和
        res = nums[0]  # 初始结果是第一个元素
        for i in range(size):
            pre = max(nums[i], pre + nums[i])  # 更新当前已经找到的最大子数组和
            res = max(res, pre)  # 更新最终结果
        return res  # 返回最大子数组的和