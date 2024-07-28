# 最长公共前缀

# 还是python的用法，zip函数和set函数 
# *strs 是对strs列表进行解包，把strs中的每个字符串作为独立的参数传递给zip

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        ans = ''
        for i in list(zip(*strs)):
            if len(set(i)) == 1:
                ans += i[0]
            else:
                break
        return ans