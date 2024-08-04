# 简化路径

# 栈的运用,想好规则,什么要进,什么不进,这都是想思路的时候应该做的

class Solution:
    def simplifyPath(self, path: str) -> str:
        stack = []
        path = path.split('/')

        for i in path:
            if i == '..':
                if stack: stack.pop()
            elif i and i != '.':
                stack.append(i)
        return '/' + '/'.join(stack)