# 判断子序列

# 没啥好说的,就是个很简单的双指针

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        a, b = len(s), len(t)
        i, j = 0, 0
        while(i != a and j != b):
            if s[i] == t[j]:
                i += 1
                j += 1
            else:
                j += 1
        return i == a