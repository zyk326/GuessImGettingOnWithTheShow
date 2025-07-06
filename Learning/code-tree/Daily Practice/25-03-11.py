# 2012. 数组美丽值求和
# 中等
# 相关标签
# 相关企业
# 提示
# 给你一个下标从 0 开始的整数数组 nums 。对于每个下标 i（1 <= i <= nums.length - 2），nums[i] 的 美丽值 等于：

# 2，对于所有 0 <= j < i 且 i < k <= nums.length - 1 ，满足 nums[j] < nums[i] < nums[k]
# 1，如果满足 nums[i - 1] < nums[i] < nums[i + 1] ，且不满足前面的条件
# 0，如果上述条件全部不满足
# 返回符合 1 <= i <= nums.length - 2 的所有 nums[i] 的 美丽值的总和 。

 

# 示例 1：

# 输入：nums = [1,2,3]
# 输出：2
# 解释：对于每个符合范围 1 <= i <= 1 的下标 i :
# - nums[1] 的美丽值等于 2
# 示例 2：

# 输入：nums = [2,4,6,4]
# 输出：1
# 解释：对于每个符合范围 1 <= i <= 2 的下标 i :
# - nums[1] 的美丽值等于 1
# - nums[2] 的美丽值等于 0
# 示例 3：

# 输入：nums = [3,2,1]
# 输出：0
# 解释：对于每个符合范围 1 <= i <= 1 的下标 i :
# - nums[1] 的美丽值等于 0
 

# 提示：

# 3 <= nums.length <= 105
# 1 <= nums[i] <= 105

nums = list(map(int, input().split()))
ans = 0
l = nums[0]
r = [nums[-1]] * len(nums)
for i in range(len(nums) - 2, -1, -1):
    r[i] = min(r[i + 1], nums[i])
for i in range(1, len(nums) - 1):
    rt = r[i + 1]
    if l < nums[i] < rt:
        ans += 2
    elif nums[i - 1] < nums[i] < nums[i + 1]:
        ans += 1
    l = max(nums[i], l)
print(ans)



class Solution:
    def sumOfBeauties(self, nums: List[int]) -> int:
        ans = 0
        l = nums[0]
        n = len(nums)
        right = [nums[-1]] * n
        for i in range(n - 2, -1, -1):
            right[i] = min(right[i + 1], nums[i])
        for i in range(1, n - 1):
            rt = right[i + 1]
            if l < nums[i] < rt:
                ans += 2
            elif nums[i - 1] < nums[i] < nums[i + 1]:
                ans += 1
            l = max(l, nums[i])
        return ans