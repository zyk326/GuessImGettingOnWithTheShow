# 有效的矩阵

# 有额外的空间支出,就是记录,打各种记录点,重点是行列计算出当前位置属于哪个块的公式

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        row = [[0] * 9 for _ in range(9)]
        col = [[0] * 9 for _ in range(9)]
        block = [[0] * 9 for _ in range(9)]

        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":
                    continue
                num = int(board[i][j]) - 1
                if row[i][num] or col[j][num] or block[(i // 3) * 3 + j // 3][num]:
                    return False
                row[i][num] = col[j][num] = block[(i // 3) * 3 + j // 3][num] = 1
        return True