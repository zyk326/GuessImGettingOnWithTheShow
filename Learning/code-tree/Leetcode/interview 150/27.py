# 移除元素

# 把要替换的值变成无穷大即可,再用原地排序.sort()即可
nums = list(map(int, input().split()))
val = int(input())

k = 0
for i in range(len(nums)):
    if nums[i] == val:
        nums[i] = float("inf")
    else:
        k += 1
nums.sort()


# class Solution:
#     def removeElement(self, nums: List[int], val: int) -> int:
#         k = 0
#         for i in range(len(nums)):
#             if nums[i] == val:
#                 nums[i] = float("inf")
#             else:
#                 k += 1
#         nums.sort()
#         return k