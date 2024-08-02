# 最长连续序列

# list的查找是O(n), set的查找是O(1),所以需要转换一下数据结构

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        longest_streak = 0
        num_set = set(nums)
        current_num = -1
        current_streak = -1
        for i in num_set:
            if i - 1 not in num_set:
                current_num = i
                current_streak = 1
            while current_num + 1 in num_set:
                current_num += 1
                current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        return longest_streak
