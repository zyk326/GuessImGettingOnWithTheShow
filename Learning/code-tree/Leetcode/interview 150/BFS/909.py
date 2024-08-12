# 蛇形棋

# 垃圾题目不想看

class Solution:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        n = len(board)   # 获取方阵的边长
        target = n * n     # 获取方阵尺寸，也是最后要到达目的地
        queue = [(1, 0)]   # 队列用于BFS，存放待搜索的方格编号和到达该方格时的最少移动数; 初始{1,0}入队，表示起点1，0次移动
        visited = [[False] * n for _ in range(n)]   # 用于BFS过程中标记方格是否搜索过
        # BFS
        while queue:
            curr, cnt = queue.pop(0)   # 获取队首的方格编号和到达该方格的最少移动数
            cnt += 1  # 移动数加1
            for i in range(curr + 1, min(curr + 6, target) + 1):
                # 枚举所有下一个可搜索且未搜索过的方格编号
                r, c = n-1 - (i-1) // n, (i-1) % n     # 根据方格编号获取这个编号的行和列
                c += (n-1 - 2*c) * ((n-1-r) & 1)       # 根据行数修正列数
                if visited[r][c]: continue  # 跳过搜索过的编号
                visited[r][c] = True       # 标记该编号已搜索
                next_ = i if board[r][c] == - 1 else board[r][c]    # 如果这个编号所在的方格可以转移到其他格子，转移到对应编号；否则就是在当前编号
                if next_ == target: return cnt   # 到达终点，直接返回最小移动数 
                queue.append((next_, cnt))  # 加入队列
        return -1  # 退出循环说明没有到达目的地
