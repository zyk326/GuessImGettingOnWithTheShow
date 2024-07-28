# 多数元素

# 计数法,用一个vote维护当前数与众数的比较值

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        vote = 0
        for i in nums:
            if vote == 0: x = i
            vote += 1 if i == x else -1
        return x