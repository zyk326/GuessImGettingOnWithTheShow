# 两数之和

# 你注意,这里是hash表的题目
# 一开始的思路就是把每个数加一个idx加入到dic中,这里一个神奇的思路是直接在dic里进行查找操作

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dic = {}
        for idx, value in enumerate(nums):
            buf = target - value
            if buf in dic:
                return [dic[buf], idx]
            dic[value] = idx
        return [-1, -1]