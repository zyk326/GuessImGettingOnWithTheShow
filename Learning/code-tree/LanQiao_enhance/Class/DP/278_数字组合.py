N, M = map(int, input().split())
n = N

info = list(map(int, input().split()))
f = [0] * 10010
f[0] = 1
while(n):
    for i in range(M, info[N - n] - 1, -1):
        f[i] += f[i - info[N - n]]
    n -= 1
print(f[M])