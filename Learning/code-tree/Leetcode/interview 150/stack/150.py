# 逆波兰表达式求值

# 有一个点,是使用除法的时候,python的/是浮点除,//是向下取证除,而不是向0除,python里要用向0除,可以先浮点除,再转整数就可以实现向零除

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stk = []
        for i in tokens:
            if i in "+-*/":
                if len(stk) >= 2:
                    a, b = stk[-2], stk[-1]
                    stk.pop()
                    stk.pop()
                    if i == '+':
                        buf = a + b
                    if i == '-':
                        buf = a - b
                    if i == '*':
                        buf = a * b
                    if i == '/':
                        buf = a // b
                    stk.append(buf)
            else:
                stk.append(int(i))
        return stk[-1]