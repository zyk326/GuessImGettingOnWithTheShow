# 字母异位词分组

# 一个点sorted之后,得到的是一个list
# 得到字典的value和key可以用:dic.keys() and dic.values()

# print(list({'a':1, 'b':2}.values()))

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        d = defaultdict(list)
        for i in strs:
            d[''.join(sorted(i))].append(i)
        return(list(d.values()))