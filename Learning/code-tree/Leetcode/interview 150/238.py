# 除自身以外数组的乘积

# 一个纯上下三角的乘法

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        ans, tmp = [1] * len(nums), 1
        for i in range(1, len(nums)):
            ans[i] = ans[i - 1] * nums[i - 1]
        for i in range(len(nums) - 2, -1, -1):
            tmp *= nums[i + 1]
            ans[i] *= tmp
        return ans