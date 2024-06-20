#SPFA跟dfs结合,预处理 + 查表
# 3.1.2可以接着看
N, M = map(int, input().split())

abcde = list(map(int, input().split()))
abcde.insert(0, 1)

e = [0 for i in range(2 * M + 10)]
ne = [0 for i in range(2 * M + 10)]
w = [0 for i in range(2 * M + 10)]
h = [-1 for i in range(N + 10)]
idx = 0

def add(a, b, c):
    global idx
    e[idx] = b
    ne[idx] = h[a]
    h[a] = idx
    w[idx] = c
    idx += 1

m = M
while(m):
    x, y, t = map(int, input().split())
    add(x, y, t)
    add(y, x, t)
    m -= 1

def spfa(u, dist):
    q = []
    dist[u] = 0
    st = [0 for i in range(N + 10)]
    q.append(u)
    st[u] = 1
    while(len(q)):
        t = q.pop(0)
        st[t] = 0
        i = h[t]
        while(i != -1):
            j = e[i]
            if dist[j] > dist[t] + w[i]:
                dist[j] = dist[t] + w[i]
                if st[j] == 0:
                    q.append(j)
                    st[j] = 1
            i = ne[i]

dist = [[float("INF") for i in range(N + 10)] for j in range(6)]
for i in range(6):
    spfa(abcde[i], dist[i])

stt = [0 for i in range(6)]
def dfs(u, start, distance):
    if u == 6:
        return distance
    res = float("INF")
    for i in range(1, 6):
        if stt[i] == 0:
            next = abcde[i]
            stt[i] = 1
            res = min(res, dfs(u + 1, i, distance + dist[start][next]))
            stt[i] = 0
    return res

print(dfs(1, 0, 0))