# 使用对象排序
# 难点在于前置的贪心处理
T = int(input())
t = T
class Info:
    def __init__(self, S, E, L):
        self.S = S
        self.E = E
        self.L = L
    
    def __lt__(self, other):
        return self.S * other.L < self.L * other.S

ans = []
while(t):
    N = int(input())
    n = N
    info = []
    m = 0
    while(n):
        S, E, L = map(int, input().split())
        ifo = Info(S, E, L)
        info.append(ifo)
        m += S
        n -= 1

    f = [-float("inf") for _ in range(10010)]
    info = sorted(info)
    f[0] = 0

    for i in range(N):
        s, e, l = info[i].S, info[i].E, info[i].L
        for j in range(m, s - 1, -1):
            f[j] = max(f[j], f[j - s] + e - (j - s) * l)

    res = 0
    for i in range(m + 1):
        res = max(res, f[i])
    ans.append(res)
    t -= 1

for i in range(T):
    print("Case #%d: %d"%(i + 1, ans[i]))