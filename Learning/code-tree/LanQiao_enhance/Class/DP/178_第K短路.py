# 这里是A*算法,没看懂,看不懂就算了,可以过了
import collections
import heapq

INF = 10 ** 9

MAX_N = 1001                    #最大的结点数量

adjvex = collections.defaultdict(list)          #邻接矩阵，有向图
reverse_adjvex = collections.defaultdict(list)  #逆向建图
N, M = 0, 0                     #结点个数，边的数量
S, T, K = 0, 0, 0               #起点，目标点，第k短的路径
cnt = [0 for _ in range(MAX_N)] #执行A*算法时，第i个点已经是第cnt[i]次到达。


#-------------------------------- 计算估计函数 -------------------------------------
dist = [INF for _ in range(MAX_N)]          #每个点，到T点的最短距离。-------- 作为估价函数h(u)
visited = [False for _ in range(MAX_N)]     #记忆化

#-------- 计算T到每个点的最短距离。
def dijkstra() -> None:
    minHeap = []
    heapq.heappush(minHeap, (0, T))
    dist[T] = 0
    while minHeap:
        d, x = heapq.heappop(minHeap)
        if visited[x] == True:
            continue
        visited[x] = True
        for y, w in reverse_adjvex[x]:
            if dist[x] + w < dist[y]:
                dist[y] = dist[x] + w
                heapq.heappush(minHeap, (dist[y], y))


#---------------------------------- A* 算法 -------------------------------------------
def A_star() -> int:
    minHeap = []
    #----按照g[u]+h[u]排序，每次都是让最小的出队
    heapq.heappush(minHeap, (0 + dist[S], 0, S))
    while minHeap:
        _, cur_d, x = heapq.heappop(minHeap)
        cnt[x] += 1
        #---- 目标点T已经被访问过K次了。就返回结果
        if cnt[T] == K:
            return cur_d
        for y, w in adjvex[x]:
            #-------- 如果一个点，已经到达过K次了，然而还没有return 结果，说明从y出发是找不到第K短路的。如果继续让y进队列没有意义
            if cnt[y] < K:
                #--------按照 真实走过的距离+未走过的估价函数值 进行排序
                heapq.heappush(minHeap, (cur_d + w + dist[y], cur_d + w, y))
    return -1



#------------------------- 输入参数
N, M = map(int, input().split())

for _ in range(M):
    x, y, w = map(int, input().split())
    adjvex[x].append((y, w))
    reverse_adjvex[y].append((x, w))

S, T, K = map(int, input().split())

#起点==终点时 则d[S→S] = 0 这种情况就要舍去 ,总共第K大变为总共第K+1大
if S == T:
    K += 1

#从各点到终点的最短路距离 作为估计函数h[u]
dijkstra()

res = A_star()
print(res)