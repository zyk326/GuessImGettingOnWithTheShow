# 快乐数

# 阅读理解没做好啊

# 变量要存储好,体现在一个常用变量名里的值要更新频繁,不要造成丢失的情况

class Solution:
    def isHappy(self, n: int) -> bool:
        li = []
        sumn = 0
        while True:
            for i in str(n):
                sumn += int(i) ** 2
            n = sumn
            sumn = 0
            if n == 1:
                return True
            if n in li:
                return False
            li.append(n)