#环装变成线性,把数组扩充一倍即可,先循环长度,再循环左端点,再循环中间点
N = int(input())
info = list(map(int, input().split()))
info += info

f = [[0 for i in range(N * 2 + 10)] for _ in range(N * 2 + 10)]

for len in range(3,  N + 2):
    l = 0
    while(l + len - 1 <= N * 2 - 1):
        r = l + len - 1
        for i in range(l + 1, r):
            f[l][r] = max(f[l][r], f[l][i] + f[i][r] + info[l] * info[i] * info[r])
        l += 1

res = 0
for i in range(N):
    res = max(res, f[i][i + N])

print(res)