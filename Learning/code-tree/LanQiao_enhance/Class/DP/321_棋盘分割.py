# sqrt()是个开平方的函数，输出的时候，%d是TM的整数，%f才是TM的浮点数
import math

N = int(input())
s = [[0] * 9]
for i in range(8):
    s.append([0] + list(map(int, input().split())))

f = [[[[[-1 for i in range(N + 10)] for i in range(10)] for i in range(10)] for i in range(10)] for i in range(10)]
for i in range(1, 9):
    for j in range(1, 9):
        s[i][j] += s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1]

X = s[8][8] / N

def get(x1, y1, x2, y2):
    sum = s[x2][y2] - s[x1 - 1][y2] - s[x2][y1 - 1] + s[x1 - 1][y1 - 1] - X
    return sum * sum / N

def dp(x1, y1, x2, y2, n):
    if f[x1][y1][x2][y2][n] >= 0:
        return f[x1][y1][x2][y2][n]
    if n == 1:
        f[x1][y1][x2][y2][n] = get(x1, y1, x2, y2)
        return f[x1][y1][x2][y2][n]
    f[x1][y1][x2][y2][n] = float("INF")
    for i in range(x1, x2):
        f[x1][y1][x2][y2][n] = min(f[x1][y1][x2][y2][n], dp(x1, y1, i, y2, n - 1) + get(i + 1, y1, x2, y2))
        f[x1][y1][x2][y2][n] = min(f[x1][y1][x2][y2][n], dp(i + 1, y1, x2, y2, n - 1) + get(x1, y1, i, y2))
    for i in range(y1, y2):
        f[x1][y1][x2][y2][n] = min(f[x1][y1][x2][y2][n], dp(x1, y1, x2, i, n - 1) + get(x1, i + 1, x2, y2))
        f[x1][y1][x2][y2][n] = min(f[x1][y1][x2][y2][n], dp(x1, i + 1, x2, y2, n - 1) + get(x1, y1, x2, i))
    return f[x1][y1][x2][y2][n]

print("%.3f"%(math.sqrt(dp(1, 1, 8, 8, N))))