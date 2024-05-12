# 完全背包问题,从小到大,然后空间优化之后,需要注意dp数组的初始值要初始化
N = int(input())
books = [10, 20, 50, 100]

f = [0] * (N + 10)
f[0] = 1
for i in range(4):
    for j in range(N + 1):
        if j >= books[i]:
            f[j] += f[j - books[i]]
print(f[N])