# 用最少数量的箭引爆气球

# 最右射击

class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        points.sort(key = lambda p: p[1])
        rig, ans = float("-inf"), 0
        for i in points:
            if i[0] > rig:
                ans += 1
                rig = i[1]
        return ans