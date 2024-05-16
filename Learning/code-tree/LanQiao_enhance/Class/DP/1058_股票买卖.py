# 画状态机就出来了
N = int(input())

info = list(map(int, input().split()))

f = [[0 for i in range(3)] for i in range(N + 10)]
f[0][0], f[0][1] = -float("inf"), -float("inf")
f[0][2] = 0

for i in range(1, N + 1):
    f[i][0] = max(f[i - 1][0], f[i - 1][2] - info[i - 1])
    f[i][1] = f[i - 1][0] + info[i - 1]
    f[i][2] = max(f[i - 1][1], f[i - 1][2])

print(max(f[N][1], f[N][2]))