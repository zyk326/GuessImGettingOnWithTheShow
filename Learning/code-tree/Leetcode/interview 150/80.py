# 删除有序数组中的重复项ii

# 官方给的快慢指针的做法:slow指向已经排好的最后一个数的后一个,fast指向正在排的那个数
# 因为不能相同必连续,所以,只需要看slow-2是否与fast相同即可,同则直接fast++,否则加入到slow的位置,slow和fast都++

# 但是官方的双指针算法运行速度要慢一倍

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        slow, fast = 2, 2
        n = len(nums)
        if n <= 2:
            return n
        while(fast < n):
            if nums[slow - 2] != nums[fast]:
                nums[slow] = nums[fast]
                slow += 1
            fast += 1
        return slow
            
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        j = 0
        k = 1
        tis = 1
        for i in range(1, len(nums)):
            if nums[i] == nums[j]:
                tis += 1
                if tis > 2:
                    nums[i] = float("INF")
                else:
                    tis += 1
                    k += 1
                continue
            tis = 1
            k += 1
            j = i
        nums.sort()
        return k