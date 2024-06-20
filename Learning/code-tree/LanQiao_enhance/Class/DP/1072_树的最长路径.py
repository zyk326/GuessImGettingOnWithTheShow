N = int(input())

e = [0 for _ in range(N + 10)]
ne = [0 for _ in range(N + 10)]
h = [-1 for _ in range(N + 10)]
w = [0 for _ in range(N + 10)]
idx = 0

def add(a, b, c):
    global idx
    e[idx] = b
    ne[idx] = h[a]
    w[idx] = c
    h[a] = idx
    idx += 1

n = N - 1
while(n):
    a, b, c = map(int, input().split())
    add(a, b, c)
    add(b, a, c)
    n -= 1

ans = -1
def dfs(u, fa):
    global ans
    dist = 0
    d1, d2 = 0, 0
    i = h[u]
    while(i != -1):
        if e[i] == fa:
            i = ne[i]  
            continue
        d = dfs(e[i], u) + w[i]
        dist = max(dist, d)
        if d >= d1:
            d2 = d1
            d1 = d
        elif d > d2:
            d2 = d
        i = ne[i]   
    ans = max(ans, d1 + d2)
    return dist

dfs(1, -1)
print(ans)