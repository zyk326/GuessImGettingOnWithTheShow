# 思路是暴力 -> n^3 然后优化
# 用双指针算法

n, k = map(int, input().split())

num = list(map(int, input().split()))

zero = 0
j = 0
len, r = 0, 0
for i in range(n):
    if num[i] ==  0:
        zero += 1
    while(zero > k):
        if num[j] == 0:
            zero -= 1
        j += 1
    t = i - j + 1
    if t > len:
        len = t 
        r = i
for i in range(r, r - len, -1):
    num[i] = 1
print(len)
for i in num:
    print(i, end=' ')