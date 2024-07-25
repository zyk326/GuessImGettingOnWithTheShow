# 跳跃游戏

# 有点区间合并的意思在里面

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        max_jump = 0
        for idx, jump in enumerate(nums):
            max_jump = idx + jump if (idx <= max_jump and max_jump < idx + jump) else max_jump
        return max_jump >= idx