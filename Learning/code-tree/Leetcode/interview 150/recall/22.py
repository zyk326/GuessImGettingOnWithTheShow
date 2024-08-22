# 括号生成

# 这是一种代码结构,只需要保证递归顺序即可

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        ans = []

        def dfs(cur, op, ed):
            if len(cur) == 2 * n:
                ans.append(cur)
                return
            if op < n:
                dfs(cur + '(', op + 1, ed)
            if ed < op:
                dfs(cur + ')', op, ed + 1)

        dfs('', 0, 0)
        return ans