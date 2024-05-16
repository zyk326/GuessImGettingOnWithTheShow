N, k = map(int, input().split())

info = list(map(int, input().split()))
f = [[[-float("inf"), -float("inf")] for _ in range(N + 10)] for _ in range(N + 10)]

for i in range(N + 1):
    f[i][0][0] = 0

for i in range(1, N + 1):
    for j in range(1, k + 1):
        f[i][j][0] = max(f[i - 1][j][0], f[i - 1][j][1] + info[i - 1])
        f[i][j][1] = max(f[i - 1][j][1], f[i - 1][j - 1][0] - info[i - 1])

res = 0
for i in range(k + 1):
    res = max(res, f[N][i][0])

print(res)