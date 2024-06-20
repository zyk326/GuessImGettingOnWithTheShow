# 数位DP的完全理解了的版本
# 重点是把f初始化，后面的dp直接查表，先枚举位数，后状态分别分类枚举最高位的取值
f = [[0 for i in range(12)] for i in range(12)]
def init():
    for i in range(10):
        if i != 4:
            f[1][i] = 1
    for i in range(2, 9):
        for j in range(10):
            if j == 4:
                continue
            for k in range(10):
                if k == 4 or j == 6 and k == 2:
                    continue
                f[i][j] += f[i - 1][k]

def dp(n):
    res = 0
    last = 0
    nums = []
    while(n):
        nums.append(n % 10)
        n //= 10
    for i in range(len(nums) - 1, -1, -1):
        x = nums[i]
        for j in range(x):
            if j == 4 or last == 6 and j == 2:
                continue
            res += f[i + 1][j]
        if x == 4 or last == 6 and x == 2:
            break
        last = x
        if i == 0:
            res += 1
    return res

init()


a, b = map(int, input().split())

anss = []
while(a != 0 or b != 0):
    anss.append(dp(b) - dp(a))
    a, b = map(int, input().split())
for i in anss:
    print(i)