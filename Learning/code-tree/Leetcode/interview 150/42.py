# 接雨水

# 左右前缀分割问题，重点是要记录每一个点的前缀最大值，然后每个点得到一个结果，最后合并成ans

class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        left = [0 for i in range(n)]
        right = [0 for i in range(n)]
        left[0] = height[0]
        right[-1] = height[-1]
        for i in range(1, n):
            left[i] = max(left[i - 1], height[i])
        ans = 0
        for i in range(n - 2, -1, -1):
            right[i] = max(right[i + 1], height[i])
            ans += min(right[i], left[i]) - height[i]
        return ans
