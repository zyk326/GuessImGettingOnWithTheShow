# 线性筛\
# 筛的是从2到n的素数有哪些
# 从2开始筛,如果st当前数是0就加入素数列表
# 之后将已有的素数列表的当前值的倍数更新到st中
# 期间要判断当前素数到达当前i的最小质因子没有,如果是,则退出
st = [0] * 5000
primes = [] * 5000
cnt = 0

def deal(a):
    global cnt
    for i in range(2, a + 1):
        if st[i] == 0:
            primes[cnt] = i
            cnt += 1
        j = 0
        while(primes[j] * i <= a):
            st[primes[j] * i] = 1
            if i % primes[j] == 0:
                break
            j += 1