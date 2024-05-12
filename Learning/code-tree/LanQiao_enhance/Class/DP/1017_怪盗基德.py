# 可以跑两个方向,所以要从两个方向遍历出最长递减子串

K = int(input())

def deal(info, N):
    res1, res2 = 0, 0
    dp = [1 for i in range(N + 10)]

    for i in range(1, N + 1):#######################################核心是这里
        for j in range(1, i):#######################################核心是这里
            if info[j - 1] > info[i - 1]:#######################################核心是这里
                dp[i] = max(dp[i], dp[j] + 1)#######################################核心是这里
        res1 = max(dp[i], res1)

    dp = [1 for i in range(N + 10)]
    for i in range(N, 0, -1):
        for j in range(N, i, -1):
            if info[j - 1] > info[i - 1]:
                dp[i] = max(dp[i], dp[j] + 1)
        res2 = max(res2, dp[i])
    return max(res1, res2)
    

ans = []
k = K
while(k):
    N = int(input())
    info = list(map(int, input().split()))
    ans.append(deal(info, N))
    k -= 1

for i in ans:
    print(i)