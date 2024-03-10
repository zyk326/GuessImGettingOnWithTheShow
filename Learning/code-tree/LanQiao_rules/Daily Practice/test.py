def work(a):
    buf = [[]]
    for i in range(1, n + 1):
        bufs = [a[i]]
        bufs.append(i)
        buf.append(bufs)
    buf[1:] = sorted(buf[1:], key = lambda k:k[0])
    for i in range(1, n + 1):
        a[buf[i][1]] = i

def merge_res(l, r):
    if l >= r:
        return 0
    mid = (l + r) >> 1
    res = (merge_res(l, mid) + merge_res(mid + 1, r)) % mod
    i, j, k = l, mid + 1, 0
    while(i <= mid and j <= r):
        if b[i] < b[j]:
            p[k] = b[i]
            k += 1
            i += 1
        else:
            p[k] = b[j]
            k += 1
            j += 1
            res = (res + mid - i + 1) % mod
    while(i <= mid):
        p[k] = b[i]
        k += 1
        i += 1
    while(j <= r):
        p[k] = b[j]
        k += 1
        j += 1
    b[l:l + k] = p[:k]
    return res

if __name__ == '__main__':
    n = int(input())
    a = list(map(int, input().strip().split()))
    b = list(map(int, input().strip().split()))
    a.insert(0, 0)
    b.insert(0, 0)
    N = 100010
    mod = 99999997
    c = [0 for i in range(N)]
    p = [0 for i in range(N)]
    work(a)
    work(b)
    for i in range(1, n + 1):
        c[a[i]] = i
    for i in range(1, n + 1):
        b[i] = c[b[i]]
    res = merge_res(1, n)
    print(res)