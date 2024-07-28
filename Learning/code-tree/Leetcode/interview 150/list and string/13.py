# 罗马数字转整数

# 一个字典的get函数，首先查看第一个key，如果不存在就返回value
# 主要还是python的语法

class Solution:
    def romanToInt(self, s: str) -> int:
        disk = {'I' : 1, 'V' : 5, 'X' : 10, 'L' : 50, 'C' : 100, 'D' : 500, 'M' : 1000, 'IV' : 3, 'IX' : 8, 'XL' : 30, 'XC' : 80, 'CD' : 300, 'CM' : 800}
        return sum(disk.get(s[max(i - 1, 0) : i + 1], disk[k]) for i, k in enumerate(s))