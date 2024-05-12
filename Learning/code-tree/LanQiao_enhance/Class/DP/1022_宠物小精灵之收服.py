# 阅读理解和二维的01背包问题
N, M, K = map(int, input().split())

k = K 
f = [[0 for _ in range(510)] for _ in range(1010)] 
while(k):
    v1, v2 = map(int, input().split())
    for i in range(N, v1 - 1, -1):
        for j in range(M - 1, v2 - 1, -1):
            f[i][j] = max(f[i][j], f[i - v1][j - v2] + 1)
    k -= 1

print(f[N][M - 1])
k = M - 1
while(k > 0 and f[N][k - 1] == f[N][M - 1]):
    k -= 1
print(M - k)