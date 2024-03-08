def deal(N, str):
    inf = [0]
    for i in range(N):
        inf.append(int(str[i]))
    res = 0
    s = [0]
    for i in range(1, N + 1):
        s.append(s[i - 1] + inf[i])
    ind = (N + 1) // 2
    for i in range(1, N + 1 - ind):
        res = max(res, s[i + ind - 1] - s[i - 1])
    return res

if __name__ == '__main__':
    T = int(input())
    ans = []
    for i in range(T):
        N = int(input())
        str = input()
        ans.append(deal(N, str))
    for i in range(T):
        print("Case #%d: %d"%(i, ans[i]))