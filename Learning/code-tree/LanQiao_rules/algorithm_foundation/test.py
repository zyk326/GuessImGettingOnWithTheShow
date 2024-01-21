N = 100001
h = [-1 for i in range(N)]
w = [0 for i in range(N)]
e = [0 for i in range(N)]
ne = [0 for i in range(N)]
idx = 0
dist = [N for i in range(N)]
st = [0 for i in range(N)]

def add(a, b, c):
    global idx
    e[idx] = b
    w[idx] = c
    ne[idx] = h[a]
    h[a] = idx
    idx += 1

def spfa():
    dist[1] = 0
    q = []
    q.append(1)
    st[1] = 1
    while(len(q)):
        t = q[0]
        del q[0]
        st[t] = 0
        i = h[t]
        while(i != -1):
            j = e[i]
            if(dist[j] > dist[t] + w[i]):
                dist[j] = dist[t] + w[i]
                if(st[j] == 0):
                    q.append(j)
                    st[j] = 1
            i = ne[i]
    if(dist[n] == N):
        return -1
    else:
        return dist[n]

if __name__ == '__main__':
    n, m = input().split()
    n = int(n)
    m = int(m)

    while(m):
        a, b, c = input().split()
        a = int(a)
        b = int(b)
        c = int(c)
        add(a, b, c)
        m -= 1
    
    t = spfa()

    print(t)