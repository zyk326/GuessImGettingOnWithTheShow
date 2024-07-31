# 矩阵置零

# 无聊的提取行列的题
# set的用法,它不会记录重复的元素
# 一个思路,先把所有需要改变的行列记录下来再来集中处理值的问题

class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        n, m = len(matrix), len(matrix[0])
        row, col = set(), set()
        for i in range(n):
            for j in range(m):
                if matrix[i][j] == 0:
                    row.add(i)
                    col.add(j)
        for i in range(n):
            for j in range(m):
                if i in row or j in col:
                    matrix[i][j] = 0