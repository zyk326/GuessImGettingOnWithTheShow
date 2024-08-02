# 赎金信

# python的用法,counter(),collection,在滑动窗口中有使用过

class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        return Counter(ransomNote) <= Counter(magazine)