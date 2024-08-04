# 基本计算器

# 这个困难题确实有点困难我丢,主要是逻辑,唉有点难我丢,这题要再想想


class Solution:
    def calculate(self, s: str) -> int:
        stack = []
        res, num, sign = 0, 0, 1
        for i in s:
            if i.isdigit():
                num = num * 10 + int(i)
            elif i in '+-':
                res = sign * num
                num = 0
                sign = 1 if i == "+" else -1
            elif i == '(':
                stack.append(res)
                stack.append(sign)
                res = 0
                sign = 1
            elif i == ')':
                res += sign * num
                num = 0
                res *= stack.pop()
                res += stack.pop()
        res += sign * num
        return res