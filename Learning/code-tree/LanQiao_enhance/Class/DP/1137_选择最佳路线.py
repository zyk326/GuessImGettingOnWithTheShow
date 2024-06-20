# 引入一个虚拟原点,把原多个起点变成路径中的一个节点
# 有一个分组输入形式的问题 x 搞不对
import sys

def add(a, b, c):
    global idx
    e[idx] = b
    ne[idx] = h[a]
    h[a] = idx
    w[idx] = c
    idx += 1

def spfa():
    st = [0 for i in range(1000 + 10)]
    q = []
    dist = [float("INF") for i in range(1000 + 10)]
    dist[0] = 0
    q.append(0)
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
    if dist[S] == float("INF"):
        return -1
    return dist[S]

anss = []

while True:
    s = sys.stdin.readline()
    if not s:
        break
    N, M, S = map(int, s.split())
    e = [0 for i in range(20000 + 1000)]
    ne = [0 for i in range(20000 + 1000)]
    w = [0 for i in range(20000 + 1000)]
    h = [0 for i in range(1000 + 1000)]
    idx = 0
    m = M
    while(m):
        p, q, t = map(int, input().split())
        add(p, q, t)
        m -= 1
    W = int(input())
    sta = list(map(int, input().split()))
    for i in sta:
        add(0, i, 1)
    anss.append(spfa())

for i in anss:
    print(i)