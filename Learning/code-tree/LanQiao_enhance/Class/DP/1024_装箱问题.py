# 把体积等价为价值
V = int(input())
N = int(input())

n = N
f = [0] * 20010
while(n):
    v = int(input())
    for i in range(V, v - 1, -1):
        f[i] = max(f[i], f[i - v] + v)
    n -= 1

print(V - f[V])