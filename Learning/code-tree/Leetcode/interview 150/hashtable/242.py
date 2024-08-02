# 有效的字母异位词

# 就是python的Counter函数

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)