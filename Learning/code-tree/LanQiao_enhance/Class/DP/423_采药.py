# 01背包的优化版(降维版)
# T, M = map(int, input().split())

# m = M
# f = [0] * 1010
# while(m):
#     v, w = map(int, input().split())
#     for i in range(T, v - 1, -1):
#         f[i] = max(f[i], f[i - v] + w)   
#     m -= 1
# print(f[T])


# 手撕版
T, M = map(int, input().split())

m = M
f = [0] * 1010
while(m):
    v, w = map(int, input().split())
    for i in range(T, v - 1, -1):
        f[i] = max(f[i], f[i - v] + w)
    m -= 1
print(f[T])