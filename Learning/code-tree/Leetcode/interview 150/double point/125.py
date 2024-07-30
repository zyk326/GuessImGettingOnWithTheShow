# 验证回文串

# 神奇的python函数,str.isalnum(),检测字符串是否由字母和数字组成
# sth.lower()把大写转换成小写

class Solution:
    def isPalindrome(self, s: str) -> bool:
        sgood = "".join(ch.lower() for ch in s if ch.islnum())
        return sgood == sgood[::-1]

class Solution:
    def isPalindrome(self, s: str) -> bool:
        st = ""
        for key, value in enumerate(s):
            va = ord(value)
            if va >= 97 and va <= 122 or va >= 48 and va <= 57:
                st += s[key]
            if va >= 65 and va <= 90:
                st += chr(va + 32)
        l, r = 0, len(st) - 1
        print(st)
        while(l < r):
            if st[l] != st[r]:
                return False
            l += 1
            r -= 1
        return True