# 数组化的单链表 + 深搜
# 背包问题的降维操作
N, V = map(int, input().split())

e = [0 for _ in range(N + 10)]
ne = [0 for _ in range(N + 10)]
h = [-1 for _ in range(N + 10)]
w = [0 for _ in range(N + 10)]
v = [0 for _ in range(N + 10)]
idx = 0

def add(a, b):
    global idx
    e[idx] = b
    ne[idx] = h[a]
    h[a] = idx
    idx += 1

f = [[0 for i in range(N + 10)] for i in range(N + 10)]
def dfs(u):
    i = h[u]
    while(i != -1):
        son = e[i]
        dfs(e[i])

        #分组背包
        j = V - v[u]
        while(j >= 0):
            for k in range(j + 1):
                f[u][j] = max(f[u][j], f[u][j - k] + f[son][k])
            j -= 1
        
        i = ne[i]
    for i in range(V, V - v[u] - 1, -1):
        f[u][i] = f[u][i - v[u]] + w[u]
    for i in range(v[u]):
        f[u][i] = 0

n = N
root = -1
while(n):
    v1, w1, p = map(int, input().split())
    v[N - n + 1] = v1
    w[N - n + 1] = w1
    if p == -1:
        root = N - n + 1
    else:
        add(p, N - n + 1)
    n -= 1

dfs(root)

print(f[root][V])