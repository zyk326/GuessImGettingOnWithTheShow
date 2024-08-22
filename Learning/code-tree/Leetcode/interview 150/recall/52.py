# N皇后ii

# 有一个对角线的公式

class Solution:
    def totalNQueens(self, n: int) -> int:
        col = [False] * n
        diag1 = [False] * (2 * n - 1)
        diag2 = [False] * (2 * n - 1)
        ans = 0

        def dfs(row: int):
            nonlocal ans
            if row == n:
                ans += 1
                return
            
            for current_col in range(n):
                if not col[current_col] and not diag1[current_col + row] and not diag2[row - current_col + n - 1]:
                    col[current_col] = True
                    diag1[row + current_col] = True
                    diag2[row - current_col + n - 1] = True
                    dfs(row + 1)
                    col[current_col] = False
                    diag1[row + current_col] = False
                    diag2[row - current_col + n - 1] = False
        dfs(0)
        return ans