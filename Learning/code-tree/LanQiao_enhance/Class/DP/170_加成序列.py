# IDA* 算法,适用于dfs中,层数很深,但答案很浅的情况

def dfs(u, dep, path):
    if u > dep:
        return False
    if path[u - 1] == n:
        return True
    st = [0 for i in range(110)]

    for i in range(u - 1, -1, -1):
        for j in range(i, -1, -1):
            s = path[i] + path[j]
            if s > n or s <= path[u - 1] or st[s]:
                continue
            path[u] = s
            if dfs(u + 1, dep, path):
                return True

def deal(num):
    path = []
    len = 1
    while(dfs(1, len, path) == False):
        len += 1
    return path        

n = int(input())
anss = []
while(n):
    anss.append(deal(n))
    n = int(input())

for i in anss:
    for j in i:
        print(j, end=" ")
    print()