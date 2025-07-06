# 三数之和

# 固定一个数的双指针,把双指针的左指针固定在这个数的右边,很容易减少一半计算量
# python的用法,not 一个list,来确定list里有没有元素
# 在这里不能用set直接去掉数组中的所有重复元素，因为，只限制了i，j，k也就是下标不同而已

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        if (not nums or n < 3):
            return []
        res = []
        nums.sort()
        for i in range(n):
            if nums[i] > 0:
                return res
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            l = i + 1
            r = n - 1
            while(l < r):
                buf = nums[i] + nums[l] + nums[r]
                if buf == 0:
                    res.append([nums[i], nums[l], nums[r]])
                    while(l < r and nums[l] == nums[l + 1]):
                        l += 1
                    while(l < r and nums[r] == nums[r - 1]):
                        r -= 1
                    l += 1
                    r -= 1
                elif buf > 0:
                    r -= 1
                elif buf < 0:
                    l += 1 
        return res

        