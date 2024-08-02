# 单词规律

# 还是一种对应关系,注意一定要是双向的,不然可能一个新对应,映射到了一个旧目标

class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        lis = list(s.split())
        pl, sl = len(pattern), len(lis)
        if pl != sl:
            return False
        dic1, dic2 = {}, {}
        for i, j in zip(pattern, lis):
            if i in dic1 and dic1[i] != j or j in dic2 and dic2[j] != i:
                return False
            dic1[i] = j
            dic2[j] = i
        return True