# 3498 日期差值
def is_leap(y):
    if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
        return 1
    return 0

def get_days(y, i):
    if i == 2:
        return 28 + is_leap(y)
    return months[i]

def calc(y, m, d):
    y = int(y)
    m = int(m)
    d = int(d)
    days = 0
    for i in range(1, y):
        days += 365 + is_leap(i)
    for i in range(1, m):
        days += get_days(y, i)
    return days + d

if __name__ == '__main__':
    months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    ans = []
    while True:
        try:
            st = input()
            ed = input()
            res = abs(calc(st[0:4], st[4:6], st[6:8]) - calc(ed[0:4], ed[4:6], ed[6:8])) + 1 
            ans.append(res)
        except:
            break
    for i in ans:
        print(i)
