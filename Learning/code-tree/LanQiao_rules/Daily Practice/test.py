# 4964 子矩阵
# 二维的单调队列
# 用滑动窗口(队列实现) 融合单调队列实现

n, m, A, B = map(int, input().split())
g = []
for _ in range(n):
    g.append(list(map(int, input().split())))

# 对每一行做滑动窗口
rmax = [[0 for i in range(m)] for j in range(n)]
rmin = [[0 for i in range(m)] for j in range(n)]
q = []

# 变成可复用的模式,因为这里只处理原g的一个维度,还有另一个维度要处理,然而后者需要使用不同的数组
def get_max(t, f, m, B):
    q = []
    q.append(0)
    for i in range(m):
        if len(q) > 0 and q[0] <= i - B:
            q.pop(0)
        while len(q) > 0 and t[q[-1]] <= t[i]: # 当队尾元素小于当前元素,意思是不能完成单调递减队列要求时,出小数
            q.pop()
        q.append(i)
        f[i] = t[q[0]]

def get_min(t, f, m, B):
    q = []
    q.append(0)
    for i in range(m):
        if len(q) > 0 and q[0] <= i - B:
            q.pop(0)
        while len(q) > 0 and t[q[-1]] >= t[i]:
            q.pop()
        q.append(i)
        f[i] = t[q[0]]

for i in range(n):
    get_max(g[i], rmax[i], m, B)
    get_min(g[i], rmin[i], m, B)

a = [0] * (n + 10)
b = [0] * (n + 10)
c = [0] * (n + 10)
res = 0
mod = 998244353
for i in range(B - 1, m):
    for j in range(n):
        a[j] = rmax[j][i]
    get_max(a, b, n, A)
    for j in range(n):
        a[j] = rmin[j][i]
    get_min(a, c, n, A)
    for j in range(A - 1, n):
        res = (res + b[j] * c[j]) % mod

print(res)