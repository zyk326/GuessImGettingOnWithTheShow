# 轮转数组

#直接就是用数组的拼接，切片的操作，熟悉的话就很好做

nums = list(map(int, input().split()))
k = int(input())
n = len(nums)

nums[:] = nums[-k % n:] + nums[:-k % n]
print(nums)

# class Solution:
#     def rotate(self, nums: List[int], k: int) -> None:
#         """
#         Do not return anything, modify nums in-place instead.
#         """
#         nums[:] = nums[-k % n:] + nums[:-k % n]
#         print(nums)
        