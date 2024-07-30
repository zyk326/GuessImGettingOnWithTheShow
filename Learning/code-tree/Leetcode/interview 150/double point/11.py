# 盛最多水的容器

# 没啥好说的,双指针也就这样

class Solution:
    def maxArea(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        maxWater = 0
        while(l < r):
            maxWater = max(maxWater, (r - l) * min(height[l], height[r]))
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        return maxWater