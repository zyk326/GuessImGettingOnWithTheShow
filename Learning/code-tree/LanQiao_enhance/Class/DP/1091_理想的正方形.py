# 单调队列优化DP
# 核心是单调队列,对不对的再看
a, b, N = map(int, input().split())

f = [[0 for i in range(b + 1)]]
A = a
while(A):
    f.append([0] + list(map(int, input().split())))
    A -= 1

def get_max(a, b, tot):
    h = []
    for i in range(1, tot + 1):
        if len(h) and h[0] <= i - N:
            h.pop(0)
        while len(h) and a[h[-1]] >= a[i]:
            h.pop()
        h.append(i)
        b[i] = a[h[0]]

def get_min(a, b, tot):
    h = []
    for i in range(1, tot + 1):
        if len(h) and h[0] <= i - N:
            h.pop(0)
        while len(h) and a[h[-1]] <= a[i]:
            h.pop()
        h.append(i)
        b[i] = a[h[0]]

low_li, hi_li = [[0 for i in range(b + 1)] for i in range(a + 1)], [[0 for i in range(b + 1)] for i in range(a + 1)]
for i in range(1, a + 1):
    get_max(f[i], hi_li[i], b)
    get_min(f[i], low_li[i], b)

a1 = [0 for i in range(max(a, b) + 1)]
b1 = [0 for i in range(max(a, b) + 1)]
c1 = [0 for i in range(max(a, b) + 1)]

res = float("INF")
for i in range(N, b + 1):
    for j in range(1, a + 1):
        a1[j] = low_li[j][i]
    get_min(a1, b1, a)
    for j in range(1, a + 1):
        a1[j] = hi_li[j][i]
    get_max(a1, c1, a)
    for j in range(N, a + 1):
        res = min(res, c1[j] - b1[j])
print(res)