# DFS搜索剪枝的问题:
# 1.可行性剪枝 2.同质剪枝 3.优化搜索顺序 4.最优性剪枝

N, W = map(int, input().split())

def dfs(u, t):
    global ans
    if t >= ans: # 最优性剪枝
        return 
    if u == N:
        ans = t
        return
    for i in range(t):
        if info[i] + w[u] <= W: # 可行性剪枝
            info[i] += w[u]
            dfs(u + 1, t)
            info[i] -= w[u]
    info[t] += w[u]
    dfs(u + 1, t + 1)
    info[t] -= w[u]
    
w = []
info = [0 for i in range(N + 10)]
n = N
ans = float("INF")
while(n):
    w.append(int(input()))
    n -= 1
w = sorted(w, reverse=True)
dfs(0, 0)
print(ans)