# 二维DP高级版
# 需要开4维DP数组,加入优化后可以省去一维,主要方法是横纵坐标的和相等,可以使用加法合并两维
# 数组边界要加入判断,上下左右四个方向判断清除就可以

N = int(input())
info = [[0 for _ in range(N + 10)] for _ in range(N + 10)]

a, b, c = map(int, input().split())
while(a or b or c):
    info[a][b] = c
    a, b, c = map(int, input().split())

dp = [[[0 for _ in range(N + 10)] for _ in range(N + 10)] for _ in range(2 * N + 10)]

for k in range(2, N + N + 1):
    for i1 in range(1, N + 1):
        for i2 in range(1, N + 1):
            j1, j2 = k - i1, k - i2
            if j1 >=1 and j1 <= N and j2 >=1 and j2 <= N:
                t = info[i1][j1]
                if j1 != j2:
                    t += info[i2][j2]
                dp[k][i1][i2] = max(dp[k][i1][i2], dp[k - 1][i1 - 1][i2 - 1] + t)
                dp[k][i1][i2] = max(dp[k][i1][i2], dp[k - 1][i1][i2 - 1] + t)
                dp[k][i1][i2] = max(dp[k][i1][i2], dp[k - 1][i1 - 1][i2] + t)
                dp[k][i1][i2] = max(dp[k][i1][i2], dp[k - 1][i1][i2] + t)

print(dp[N + N][N][N])