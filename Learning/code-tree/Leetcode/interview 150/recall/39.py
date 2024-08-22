# 组合总数

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        def dfs(start: int, target: int, path: List[int], res: List[List[int]]):
            if target == 0:
                res.append(path.copy()) # 避免后序改变path
                return 
            if target < 0:
                return 
            
            for i in range(start, len(candidates)):
                if candidates[i] > target:
                    break
                path.append(candidates[i])
                dfs(i, target - candidates[i], path, res)
                path.pop()
            
        candidates.sort()
        res = []
        dfs(0, target, [], res)
        return res