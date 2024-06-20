# 这是一个单调队列优化DP
# 把它变成一个前缀和的问题
# 队列里面存下标
N, M = map(int, input().split())
info = list(map(int, input().split()))

f = [0 for _ in range(N + 10)]
for i in range(1, N + 1):
    f[i] = info[i - 1] + f[i - 1]

res = 0
q = []
for i in range(1, N + 1):
    if len(q) and q[0] < i - M:
        q.pop(0)
    if len(q):
        res = max(res, f[i] - f[q[0]])
    while(len(q) and f[q[0]] >= f[i]):
        q.pop(0)
    q.append(i)
print(res)