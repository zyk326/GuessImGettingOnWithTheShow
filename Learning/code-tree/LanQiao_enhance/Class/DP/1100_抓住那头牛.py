# 注意开的数组的空间大小就可以了

n, k = map(int, input().split())
N = 10010
q = []
p = [-1 for i in range(2 * N)]
def bfs():
    q.append(n)
    while(len(q)):
        x = q.pop(0)
        if x == k:
            return p[x]
        if x - 1 >= 0 and p[x - 1] == -1:
            q.append(x - 1)
            p[x - 1] = p[x] + 1
        if x + 1 <= 2 * N and p[x + 1] == -1:
            q.append(x + 1)
            p[x + 1] = p[x] + 1
        if x * 2 <= 2 * N and p[x * 2] == -1:
            q.append(x * 2)
            p[x * 2] = p[x] + 1
    return -1


print(bfs())