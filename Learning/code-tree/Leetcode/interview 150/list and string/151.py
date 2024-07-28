# 反转字符串中的单词

# python的用法，join函数，用指定字符串拼接序列
# split()会忽略连续的空格

class Solution:
    def reverseWords(self, s: str) -> str:
        return ' '.join(s.strip().split()[::-1])