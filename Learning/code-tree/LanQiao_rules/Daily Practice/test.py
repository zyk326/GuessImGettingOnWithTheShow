def get(i, ti):
    return max(0, fishes[i] - ti * loss[i])

def work(i, t):
    ans = 0
    ti = [0 for i in range(N + 1)]

    for s in range(1, t + 1):
        j = 1
        for k in range(2, i + 1):
            if get(k, ti[k]) > get(j, ti[j]):
                j = k
        ans += get(j, ti[j])
        ti[j] += 1
    return ans

if __name__ == '__main__':
    N = int(input())
    fishes = list(map(int, input().strip().split()))
    loss = list(map(int, input().strip().split()))
    totime = list(map(int, input().strip().split()))
    fishes.insert(0, 0)
    loss.insert(0, 0)
    totime.insert(0, 0)
    totime.insert(0, 0)
    for i in range(2, N + 1):
        totime[i] += totime[i - 1]
    T = int(input())
    d = [0 for i in range(1, N + 1)]
    res = 0
    for i in range(1, N + 1):
        res = max(res, work(i, T - totime[i]))
    print(res)
