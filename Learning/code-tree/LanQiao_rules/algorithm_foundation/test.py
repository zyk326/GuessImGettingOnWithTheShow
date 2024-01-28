def find(x):
    if (p[x] != x):
        p[x] = find(p[x])
    return p[x]

if __name__ == '__main__':
    n, m = input().split()
    n = int(n)
    m = int(m) 
    mm = m
    N = 100001
    edge = []
    p = [0 for i in range(N)]
    while(mm):
        a, b, c = input().split()
        a = int(a)
        b = int(b)
        c = int(c)
        edge.append([a, b, c])
        mm -= 1
    edge = sorted(edge, key = lambda edge:edge[2])
    for i in range(1, n + 1):
        p[i] = i
    res = 0
    cnt = 0
    for i in range(m):
        aa, bb, cc = edge[i][0],edge[i][1],edge[i][2]
        aa, bb = find(aa), find(bb)
        if aa != bb:
            p[aa] = bb
            res += cc
            cnt += 1
    if cnt < n - 1:
        print("impossible")
    else:
        print(res)