# 分发糖果

# 左右规则遍历后结合,有一个点是说答案直接取left[-1]做基是因为此点已经是max(A, B)中的结果了.

class Solution:
    def candy(self, ratings: List[int]) -> int:
        left = [1 for i in range(len(ratings))]
        right = [1 for i in range(len(ratings))]
        for i in range(1, len(ratings)):
            if ratings[i] > ratings[i - 1]:
                left[i] = left[i - 1] + 1
        ans = left[-1]
        for i in range(len(ratings) - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                right[i] = right[i + 1] + 1
            ans += max(left[i], right[i])
        return ans