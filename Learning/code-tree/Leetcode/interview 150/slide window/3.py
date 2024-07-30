# 无重复字符的最长子串

# 用到字符哈希,存放字符的最晚出现位置
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        dic, i, res = {}, -1, 0
        for j in range(n):
            if s[j] in dic:
                i = max(i, dic[s[j]]) # 找到相同字符的index,这两个相同字符的中间部分是没有任何重复的
            dic[s[j]] = j
            res = max(res, j - i)
        return res