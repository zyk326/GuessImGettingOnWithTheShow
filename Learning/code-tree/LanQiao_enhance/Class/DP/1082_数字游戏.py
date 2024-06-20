# 数位DP
# 有板子
# 技巧是f(Y) - f(X)
# 技巧是用树的方式
# 一点数论的东西 Ca b = Ca-1 b-1 + Ca b-1
X, Y = map(int, input().split())
K = int(input())
B = int(input())

N = 33
f = [[0 for i in range(N)] for i in range(N)]

def init():
    for i in range(N):
        for j in range(0, i + 1):
            if j == 0:
                f[i][j] = 1
            else:
                f[i][j] = f[i - 1][j - 1] + f[i - 1][j]

def dp(n):
    if n == 0:
        return 0
    nums = []
    while(n):
        nums.append(n % B)
        n //= B
    res = 0
    last = 0
    for i in range(len(nums) - 1, -1, -1):
        x = nums[i]
        if x:
            res += f[i][K - last]
            if x > 1:
                if K - last - 1 >= 0:
                    res += f[i][K - last - 1]
                    break
            else:
                last += 1
                if last > K:
                    break
    if i == 0 and last == K:# 判断右侧分支的合法性,才能加1
        res += 1
    return res

init()
print(dp(Y) - dp(X))