# SPFA的模版题,背!!!

T, C, Ts, Te = map(int, input().split())

# e 给两倍的边的数量加10就可以
e = [0 for i in range(2 * C + 10)]
ne = [0 for i in range(2 * C + 10)]
w = [0 for i in range(2 * C + 10)]
h = [-1 for i in range(T + 10)]
idx = 0

def add(a, b, c):
    global idx
    e[idx] = b
    w[idx] = c
    ne[idx] = h[a]
    h[a] = idx
    idx += 1

dist = [float("INF") for i in range(T + 10)]
st = [0 for i in range(T + 10)]
q = []
def spfa():
    dist[Ts] = 0
    q.append(Ts)
    st[Ts] = 1
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

c = C
while(c):
    Rs, Re, Ci = map(int, input().split())
    add(Rs, Re, Ci)
    add(Re, Rs, Ci)
    c -= 1

spfa()
print(dist[Te])