def dfs(u, su, sd):
    global ans##########这里在做答案筛选
    if su + sd >= ans:##########这里在做答案筛选
        return##########这里在做答案筛选
    if u == n:##########这里在做答案筛选
        ans = su + sd##########这里在做答案筛选
        return ##########这里在做答案筛选
    
    k = 0
    while(k < su and up[k] >= info[u]):
        k += 1
    t = up[k]
    up[k] = info[u]
    if k < su:
        dfs(u + 1, su, sd)
    else:
        dfs(u + 1, su + 1, sd)

    up[k] = t #恢复现场

    k = 0
    while(k < sd and down[k] <= info[u]):
        k += 1
    t = down[k]
    down[k] = info[u]
    if k < sd:
        dfs(u + 1, su, sd)
    else:
        dfs(u + 1, su, sd + 1)
    down[k] = t


n = int(input())
anss = []
ans = n
up = []
down = []
while(n):
    ans = n
    up = [0] * (n + 10)
    down = [0] * (n + 10)
    info = list(map(int, input().split()))
    dfs(0, 0, 0)
    anss.append(ans)
    n = int(input())

for i in anss:
    print(i)