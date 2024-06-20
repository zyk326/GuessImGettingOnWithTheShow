# BFS的多源问题
N, M = map(int, input().split())

info = []
n = N
while(n):
    info.append(list(input()))
    n -= 1

q = []
dist = [[-1 for i in range(M)] for j in range(N)]
def bfs():
    for i in range(N):
        for j in range(M):
            if info[i][j] == '1':
                dist[i][j] = 0
                q.append([i, j])
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]
    while(len(q)):
        xp, yp = q.pop(0)
        for i in range(4):
            x = xp + dx[i]
            y = yp + dy[i]
            if x < 0 or x >= N or y < 0 or y >= M:
                continue
            if dist[x][y] != -1:
                continue
            dist[x][y] = dist[xp][yp] + 1 
            q.append([x, y])    
bfs()

for i in range(N):
    for j in range(M):
        print(dist[i][j], end=' ')
    print()