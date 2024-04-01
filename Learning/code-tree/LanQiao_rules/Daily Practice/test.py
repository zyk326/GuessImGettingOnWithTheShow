# 状态压缩DP
# 731 毕业旅行问题
n = int(input())
N = 20
M = 1 << N
g = []
for _ in range(n):
    buf = list(map(int, input().split()))
    g.append(buf)

m = [[0x3f3f3f3f] * N for i in range(M)]
# m = [[[0x3f3f3f3f] * (n + 1)] for i in range(n + 1)]

m[1][0] = 0

for i in range(1, 1 << n, 2):
    for j in range(n):
        if i >> j & 1:
            for k in range(n):
                if ((i - (1 << j)) >> k & 1):
                    m[i][j] = min(m[i][j], m[i - (1 << j)][k] + g[k][j])
res = 0x3f3f3f3f

for i in range(1, n):
    res = min(res, m[(1 << n) - 1][i] + g[i][0])

print(res)
