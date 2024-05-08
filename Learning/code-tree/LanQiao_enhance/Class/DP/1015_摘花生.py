T = int(input())

def deal(info, R, C):
    res = 0
    dp = [[0 for _ in range(C + 10)] for _ in range(R + 10)]
    for i in range(1, R + 1):
        for j in range(1, C + 1):
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]) + info[i - 1][j - 1]
    return dp[R][C]

ans = []
t = T
while(t):
    info = []
    R, C = map(int, input().split())
    for i in range(R):
        info.append(list(map(int, input().split())))
    ans.append(deal(info, R, C))
    t -= 1

for i in ans:
    print(i)