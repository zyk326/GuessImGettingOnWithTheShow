# 二元素相加排序,每点判断能不能加入,不能则判能不能打折加入
def main():
    N, B = map(int, (input().split()))
    n = N
    info = []
    while(n):
        info.append(list(map(int, (input().split()))))
        n -= 1
    info = sorted(info, key = lambda K:K[0] + K[1])
    idx = 0
    res = 0
    for dat in info:
        buf = dat[0] + dat[1]
        if res + buf <= B:
            B -= buf
            idx += 1
        else:
            buf -= dat[0]
            buf += dat[0] // 2
            if res + buf <= B:
                B -= buf
                idx += 1
    print(idx)
    pass


if __name__ == '__main__':
    main(); 