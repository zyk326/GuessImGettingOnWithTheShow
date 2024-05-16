# 问题向完全背包问题转化
# 初始状态要记得更新一下

T = int(input())

def deal(N, info):
    info = sorted(info)
    f = [0 for _ in range(info[N - 1] + 10)]
    f[0] = 1  ###########################################
    res = 0
    for i in range(N):
        if f[info[i]] == 0:
            res += 1
        for j in range(info[i], info[N - 1] + 1):
            f[j] += f[j - info[i]]
    return res

ans = []
while(T):
    N = int(input())
    info = list(map(int, input().split()))
    ans.append(deal(N, info))
    T -= 1

for i in ans:
    print(i)