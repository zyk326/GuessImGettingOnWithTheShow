# 最后一个单词的长度

# python 的用法，strip函数

class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        inf = s.strip().split(" ")
        return len(inf[-1])