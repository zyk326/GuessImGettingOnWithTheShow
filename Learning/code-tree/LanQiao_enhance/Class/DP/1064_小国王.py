# 状态压缩DP说的是把状态分组,加上状态机的思维,用不同维度做关系转移之后,看联系得到数组的值
N, K = map(int, input().split())

def count(num):
    res = 0
    for i in range(N):
        res += (num >> i & 1)
    return res

def check(num):
    for i in range(N):
        if (num >> i & 1) and (num >> (i + 1) & 1):
            return False
    return True

state = []
cnt = [0 for i in range(1 << N)]
for i in range(1 << N):
    if check(i):
        state.append(i)
        cnt[i] = count(i)

head = [[] for _ in range(1 << N)]
for i in range(len(state)):
    for j in range(len(state)):
        a = state[i]
        b = state[j]
        if (a & b) == 0 and check(a | b):
            head[i].append(j)
f = [[[0 for i in range(1 << N)] for _ in range(K + 10)] for _ in range(N + 10)]
f[0][0][0] = 1
for i in range(1, N + 2):
    for j in range(K + 1):
        for a in range(len(state)):
            for b in head[a]:
                c = cnt[state[a]]
                if j >= c:
                    f[i][j][state[a]] += f[i - 1][j - c][state[b]]
print(f[N + 1][K][0])