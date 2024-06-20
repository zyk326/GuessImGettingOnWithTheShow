# Flood fill算法， 用bfs实现的
# 随便写
N, M = map(int, input().split())

info = []
st = [[0 for i in range(M)] for j in range(N)]
n = N
while(n):
    info.append(list(input()))
    n -= 1

def bfs(x, y):
    q = []
    q.append([x, y])
    while(len(q)):
        x, y = q.pop(0)
        st[x][y] = 1
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i == x and j == y:
                    continue
                if i < 0 or i >= N or j < 0 or j >= M:
                    continue
                if info[i][j] == 'W' and st[i][j] == 0:
                    q.append([i, j])
                    st[i][j] = 1

res = 0
for i in range(N):
    for j in range(M):
        if info[i][j] == 'W' and st[i][j] == 0:
            bfs(i, j)
            res += 1
print(res)