# 有效的括号

# 想这种有对应关系的就首先想到用字典

class Solution:
    def isValid(self, s: str) -> bool:
        stk = []
        for i in s:
            if i in ['(', '{', '[']:
                stk.append(i)
            else:
                if not stk:
                    return False
                if i == ')':
                    if stk[-1] != '(':
                        return False
                if i == ']':
                    if stk[-1] != '[':
                        return False
                if i == '}':
                    if stk[-1] != '{':
                        return False
                stk.pop()
        if stk:
            return False
        return True
    
# leetcode 的写法
class Solution:
    def isValid(self, s: str) -> bool:
        dic = {')' : '(', ']' : '[', '}' : '{'}
        stack = []
        for i in s:
            if stack and i in dic:
                if stack[-1] == dic[i]: stack.pop()
                else: return False
            else:
                stack.append(i)
        return not stack