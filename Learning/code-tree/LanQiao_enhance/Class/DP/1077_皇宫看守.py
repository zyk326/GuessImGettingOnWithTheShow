N = int(input())

e = [0 for i in range(N + 10)]
ne = [0 for i in range(N + 10)]
h = [-1 for i in range(N + 10)]
w = [0 for i in range(N + 10)]
idx = 0

def add(a, b):
    global idx
    e[idx] = b
    ne[idx] = h[a]
    h[a] = idx
    idx += 1

n = N 
st = [0 for i in range(N + 10)]
while(n):
    buf = list(map(int, input().split()))
    i, k, m = buf[0], buf[1], buf[2]
    w[i] = k
    M = m
    while(m):
        add(i, buf[3 + M - m])
        st[buf[3 + M - m]] = 1
        m -= 1
    n -= 1

root = 1
while(st[root]):
    root += 1

f = [[0 for _ in range(3)] for _ in range(N + 10)]

def dfs(u):
    f[u][2] = w[u]
    i = h[u]
    while(i != -1):
        j = e[i]
        dfs(j)
        f[u][0] += min(f[j][1], f[j][2])
        f[u][2] += min(min(f[j][0], f[j][1]), f[j][2])
        i = ne[i]
    f[u][1] = float("INF")
    i = h[u]
    while(i != -1):
        j = e[i]
        f[u][1] = min(f[u][1], f[j][2] + f[u][0] - min(f[j][1], f[j][2]))
        i = ne[i]

dfs(root)

print(min(f[root][1], f[root][2]))