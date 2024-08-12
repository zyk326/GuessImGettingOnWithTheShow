# 岛屿的数量

# 有两个点,函数nonlocal grid 的使用:
# nonlocal 通常用在嵌套函数中来引用外层最近的可变变量。由于 grid 在这里并不是在外层函数的可变局部变量中定义，所以这不是必要的。

# DFS 函数中的坐标更新:
# 在调用 dfs(x, y) 之前，使用 x += dx[i] 和 y += dy[i] 是错误的。改变 x 和 y 后，应再调用 dfs，但返回后 x 和 y 应该恢复，使用局部变量会更合理。

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0
        row, col = len(grid), len(grid[0])

        def dfs(x, y):
            grid[x][y] = '0'
            dx, dy = [1, 0, -1, 0], [0, 1, 0, -1]
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                if 0 <= nx < row and 0 <= ny < col and grid[nx][ny] == '1':
                    dfs(nx, ny)

        ans = 0
        for i in range(row):
            for j in range(col):
                if grid[i][j] == '1':
                    dfs(i, j)
                    ans += 1
        return ans