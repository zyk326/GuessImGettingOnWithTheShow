def deal(k, n, m, info):
    res = 0
    
    return res

def main():
    T = int(input())
    t = T
    ans = []
    while(t):
        k, n, m = map(int, input().split())
        info = []
        for i in range(n):
            info.append(list(map(int, input().split())))
        ans.append(deal(k, n, m, info))
        t -= 1
    for i in ans:
        print(i)
    pass


if __name__ == '__main__':
    main(); 