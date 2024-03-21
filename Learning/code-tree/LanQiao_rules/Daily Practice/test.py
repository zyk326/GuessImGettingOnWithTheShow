# 查分 + 哈希
n = int(input())
inf = list(map(int, input().split()))
p = sorted(inf, reverse=True)
inf.insert(0, 0)
for i in range(1, n + 1):
    inf[i] += inf[i - 1]
m = int(input())
ans = 0
q = [0] * (n + 2)
while(m):
    x, y = map(int, input().split())
    q[x] += 1
    q[y + 1] -= 1
    ans += inf[y] - inf[x - 1]
    m -= 1
for i in range(1, n + 1):
    q[i] += q[i - 1]
q = sorted(q, reverse=True)
p.append(0)
for i in range(n + 1):
    ans -= q[i] * p[i]
print(-ans)