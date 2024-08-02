# 存在重复元素ii

# 把见过的且没有作用的元素放到dic里去

class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        dic = {}
        for key, value in enumerate(nums):
            if value in dic and abs(dic[value] - key) <= k:
                return True
            dic[value] = key
        return False