# 生命游戏

# 无聊的遍历游戏
# 矩阵的题就是玩下标,无聊死了

class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        n, m = len(board), len(board[0])
        for i in range(n):
            for j in range(m):
                cnt = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if x == 0 and y == 0 or i + x < 0 or i + x >= n or j + y < 0 or j + y >= m:
                            continue
                        if board[i + x][j + y] == 1 or board[i + x][j + y] == 2:
                            cnt += 1
                if board[i][j] == 1 and (cnt < 2 or cnt > 3): board[i][j] = 2
                if board[i][j] == 0 and cnt == 3: board[i][j] = 3

        for i in range(n):
            for j in range(m):
                board[i][j] %= 2