# DP区间DP,神了,还能这么用的
# 两个数组,一个存分数,一个存根节点
N = int(input())
info = list(map(int, input().split()))

def dfs(l, r):
    if l > r:
        return
    print(g[l][r] + 1, end=" ")
    dfs(l, g[l][r] - 1)
    dfs(g[l][r] + 1, r)
    

f = [[0 for i in range(N + 10)] for j in range(N + 10)]
g = [[0 for i in range(N + 10)] for j in range(N + 10)]
for i in range(1, N + 1):
    j = 0
    while(j + i - 1 <= N - 1):
        l = j
        r = j + i - 1
        if l == r:
            f[l][r] = info[l]
            g[l][r] = l
        else:
            for k in range(l, r + 1):
                left = 1 if l == k else f[l][k - 1]
                right = 1 if r == k else f[k + 1][r]
                score = left * right + info[k]
                if f[l][r] < score:
                    f[l][r] = score
                    g[l][r] = k
        j += 1

print(f[0][N - 1])
dfs(0, N - 1)