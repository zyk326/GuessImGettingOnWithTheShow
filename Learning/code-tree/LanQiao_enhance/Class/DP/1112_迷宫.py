# dfs写迷宫问题
# dfs的意思是如果不能做,就接着做,在代码上反映的是跳过不满足的值
K = int(input())
st = [[0 for i in range(110)] for j in range(110)]

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
def dfs(g, x, y, x2, y2, n): # 写法问题,不要遇到第一个#就返回了,这样就是说即使有合法解,也不能找到
    if g[x][y] == '#':
        return False
    if x == x2 and y == y2:
        return True
    st[x][y] = 1
    for i in range(4):
        x1, y1 = x + dx[i], y + dy[i]
        if x1 < 0 or x1 >= n or y1 < 0 or y1 >= n:
            continue
        if st[x1][y1] == 1:
            continue
        if dfs(g, x1, y1, x2, y2, n):
            return True   # 这里是返回值
    return False


k = K
anss = []
while(k):
    n = int(input())
    g = []
    st = [[0 for i in range(110)] for j in range(110)]
    for i in range(n):
        g.append(list(input()))
    x1, y1, x2, y2 = map(int, input().split())
    if dfs(g, x1, y1, x2, y2, n):
        anss.append("YES")
    else:
        anss.append("NO")
    k -= 1

for i in anss:
    print(i)