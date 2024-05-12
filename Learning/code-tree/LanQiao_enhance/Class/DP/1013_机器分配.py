# 这是一个类分组背包问题,即需要转化成分组背包问题的问题
N, M = map(int, input().split())

info = []
n = N
while(n):
    buf = list(map(int, input().split()))
    buf.insert(0, 0)
    info.append(buf)
    n -= 1
    
f = [[0 for _ in range(20)] for _ in range(20)]
way = [0] * 20

for i in range(1, N + 1):
    for j in range(M + 1):
        for k in range(j + 1):
            f[i][j] = max(f[i][j], f[i - 1][j - k] + info[i - 1][k])
print(f[N][M])

j = M
for i in range(N, 0, -1):
    for k in range(j + 1):
        if f[i][j] == f[i - 1][j - k] + info[i - 1][k]:
            way[i] = k
            j -= k
            break
for i in range(N):
    print(i + 1, " ", way[i + 1])