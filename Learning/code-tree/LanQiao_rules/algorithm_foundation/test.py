N = 100010
index = 0

def add(a, b):
    global index, e, ne, index, h
    e[index] = b
    ne[index] = h[a]
    h[a] = index
    index += 1

def bfs():
    print(d[0:10])
    hh, tt = 0, 0
    q[0] = 1
    d[1] = 0
    while(hh <= tt):
        t = q[hh]
        hh += 1
        i = h[t]
        while(i != -1):
            j = e[i]
            print(i, j)
            if(d[j] == -1):
                d[j] = d[t] + 1
                tt += 1
                q[tt] = j
            i = ne[i]
    return d[n]

if __name__ == '__main__':
    h = [-1 for i in range(N)]
    e = [0 for i in range(2 * N)]
    ne = [0 for i in range(2 * N)]
    st = [0 for i in range(N)]
    q = [0 for i in range(N)]
    d = [-1 for i in range(N)]
    n, m = input().split()
    n = int(n)
    m = int(m)
    while(m):
        m -= 1
        a, b = input().split()
        a = int(a)
        b = int(b)
        add(a, b)
    print(bfs())
    print(d[0:10])