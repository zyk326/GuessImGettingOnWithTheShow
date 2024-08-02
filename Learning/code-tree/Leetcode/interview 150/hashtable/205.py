# 同构字符串

# 就是一个映射关系,开两个字典就行

class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        s2t, t2s = {}, {}
        for a, b in zip(s, t):
            if a in s2t and s2t[a] != b or b in t2s and t2s[b] != a:
                return False
            s2t[a] = b
            t2s[b] = a
        return True