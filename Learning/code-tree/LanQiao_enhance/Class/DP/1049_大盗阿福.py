T = int(input())

def deal(N, info):
    res = 0
    f = [[0, 0] for i in range(100010)]    
    f[0][0] = 0
    f[0][1] = -float("inf")
    for i in range(1, N + 1):
        f[i][0] = max(f[i - 1][0], f[i - 1][1])
        f[i][1] = f[i - 1][0] + info[i - 1]
    return max(f[N][0], f[N][1])

ans = []
t = T
while(t):
    N = int(input())
    info = list(map(int, input().split()))
    ans.append(deal(N, info))
    t -= 1

for i in ans:
    print(i)