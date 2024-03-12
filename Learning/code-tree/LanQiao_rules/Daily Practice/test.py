# 1343 挤牛奶
# 区间合并
# 思路维护一个连续区间的左端点和右端点
# 按左端点排序,查看一个新区间的时候,更新连续区间的左, 右端点
if __name__ == '__main__':
    N = int(input())
    inf = []
    for i in range(N):
        inf.append(list(map(int, input().split())))
    inf = sorted(inf, key=lambda k:k[0]) # 区间排序,区间覆盖
    l = inf[0][0] # 最左
    res1, res2 = 0, 0
    mr = inf[0][1] # 最右端点
    for i in range(1, N):
        if inf[i][0] <= mr: # 加等于是为了算第一个区间值, 否则需要初始化
            mr = max(mr, inf[i][1])
        else: # 算距离,第一个元素的右端点不能在第一个区间的左端点右边,所以初始化的时候需要把填充端点的右端点无限往右拉
            res1 = max(res1, mr - l)
            res2 = max(res2, inf[i][0] - mr)
            l = inf[i][0]
            mr = inf[i][1]
    res1 = max(res1, mr - l) # 最后一个区间初始化
    print("%d %d"%(res1, res2))