# 组合

# 调个包就完了
# import itertools


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        return list(combinations(range(1, n + 1), k))