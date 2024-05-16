#  初始状态没有给
#  测试样例的问题
# 完全背包,空间优化,从小到大
N, M = map(int, input().split())

f = [0 for _ in range(3010)]
f[0] = 1
n = N
while(n):
    v = int(input())
    for i in range(v, M + 1):
        f[i] += f[i - v]
    n -= 1

print(f[M])