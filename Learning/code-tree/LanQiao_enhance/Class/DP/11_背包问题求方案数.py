# 把最大值和最多方法分开放,就是说开两个数组,用于求方案的数量的问题
N, V = map(int, input().split())

n = N
mod = 1000000007
f = [-1 for _ in range(N + 10)]
g = [0 for _ in range(N + 10)]
f[0] = 0
g[0] = 1
while(n):
    v, w = map(int, input().split())
    for i in range(V, v - 1, -1):
        maxv = max(f[i], f[i - v] + w)
        cnt = 0
        if maxv == f[i]:
            cnt += g[i]
        if maxv == f[i - v] + w:
            cnt += g[i - v]
        g[i] = cnt % mod
        f[i] = maxv
    n -= 1

res = 0
for i in range(V + 1):
    res = max(res, f[i])
cnt = 0
for i in range(V + 1):
    if res == f[i]:
        cnt = (cnt + g[i]) % mod

print(cnt)