# 全排列

# 这里有一个切片的方式来回溯,就不用那个itertools了
# 几个点,nonlocal, [] only + []

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []
        def dfs(lis, strs):
            nonlocal res
            if not lis:
                res.append(strs)
            else:
                for i in range(len(lis)):
                    dfs(lis[ : i] + lis[i + 1 : ], strs + [lis[i]])
        dfs(nums, list())
        return res