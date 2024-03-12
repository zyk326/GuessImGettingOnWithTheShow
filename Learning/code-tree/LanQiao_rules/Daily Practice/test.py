# 1343 挤牛奶
# 区间合并
# 思路维护一个连续区间的左端点和右端点
# 按左端点排序,查看一个新区间的时候,更新连续区间的左, 右端点
if __name__ == '__main__':
    N = int(input())
    inf = [[0, 1e7]]
    for i in range(N):
        inf.append(list(map(int, input().split())))
    inf[1:] = sorted(inf[1:], key=lambda k:k[0]) # 区间排序,区间覆盖
    l = 1
    res1, res2 = 0, 0
    mr = inf[1][1] # 最右端点
    for i in range(1, N + 1):
        if inf[i][0] <= mr and inf[i][1] >= mr: # 加等于是为了算第一个区间值, 否则需要初始化
            res1 = max(res1, inf[i][1] - inf[l][0])
            mr = max(mr, inf[i][1])
        if inf[i][0] > mr: # 算距离,第一个元素的右端点不能在第一个区间的左端点右边,所以初始化的时候需要把填充端点的右端点无限往右拉
            res2 = max(res2, inf[i][0] - mr)
            l = i
            mr = inf[i][1]
    res1 = max(res1, inf[N][1] - inf[N][0]) # 最后一个区间初始化
    print("%d %d"%(res1, res2))