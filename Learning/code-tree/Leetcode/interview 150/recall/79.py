# 单词搜索

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        row, col = len(board), len(board[0])

        def dfs(i, j, k):
            if not 0 <= i < row or not 0 <= j < col or board[i][j] != word[k]:
                return
            if k == len(word) - 1:
                return True
            
            temp = board[i][j]
            board[i][j] = '#'

            found = dfs(i + 1, j, k + 1) or dfs(i - 1, j, k + 1) or dfs(i, j + 1, k + 1) or dfs(i, j - 1, k + 1)

            board[i][j] = temp
            return found

        for i in range(row):
            for j in range(col):
                if dfs(i, j, 0):
                    return True
        return False