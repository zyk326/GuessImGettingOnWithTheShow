# 螺旋矩阵

# 无聊的模拟题,控制上下左右边界就可以

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        l, r, t, b, res = 0, len(matrix[0]) - 1, 0, len(matrix) - 1, []
        while True:
            for i in range(l, r + 1): res.append(matrix[t][i])
            t += 1
            if t > b:
                break
            for i in range(t, b + 1): res.append(matrix[i][r])
            r -= 1
            if l > r:
                break
            for i in range(r, l - 1, -1): res.append(matrix[b][i])
            b -= 1
            if t > b:
                break
            for i in range(b, t - 1, -1): res.append(matrix[i][l])
            l += 1
            if l > r:
                break
        return res