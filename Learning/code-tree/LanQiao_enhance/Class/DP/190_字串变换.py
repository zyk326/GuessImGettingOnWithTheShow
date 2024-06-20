# 双端bfs的写法

from collections import deque
A, B = input().split()
a, b = [], [] # 扩展规则

def extend(q, da, db, a, b):
    n = len(a) # 对应的串的规则的长度
    t = q.popleft()
    l = len(t)
    for i in range(l):
        for j in range(n):
            if t[i : i + len(a[j])] == a[j]:
                state = t[:i] + b[j] + t[i + len(a[j]) : ] # 这里就是状态变换了,把固定长度的中间部分变换掉
                if db.get(state) != None: #已经在另一个状态数组里找到变换到这个状态需要的步骤数量
                    return da[t] + 1 + db[state]
                if da.get(state) != None: # 字典获取对应value的函数
                    continue
                q.append(state)
                da[state] = da[t] + 1
    return 11

def bfs(A, B):
    global a, b
    da, db = {}, {}
    qa, qb = deque(), deque() # 双端队列
    da[A] = 0   # 字典,一个状态对应一个步数
    db[B] = 0   # 字典,一个状态对应一个步数
    qa.append(A)    # 状态队列
    qb.append(B)    # 状态队列
    if A == B:
        return 0
    while qa and qb: # 双端队列的写法
        if len(qb) >= len(qa):
            t = extend(qa, da, db, a, b)
        else:
            t = extend(qb, db, da, b, a)
        if t <= 10:
            return t
    return 11


while True:                     #神奇的写法
    try:                        #神奇的写法
        x, y = input().split()                      #神奇的写法
        a.append(x)                     #神奇的写法
        b.append(y)                     #神奇的写法
    except:                     #神奇的写法
        break                       #神奇的写法

t = bfs(A, B)
print(t) if t <= 10 else print("NO ANSWER!")