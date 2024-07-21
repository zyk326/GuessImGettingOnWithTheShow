# 合并两个有序数组

# 主要是数组的原地操作，排序直接用.sort()就行，.sort（）和sorted（XXX）是不同的

nums1 = list(map(int, input().split()))
m = int(input())
nums2 = list(map(int, input().split()))
n = int(input())


nums1 = nums1[:m]
nums1 += nums2
nums1 = sorted(nums1)
print(nums1)

# class Solution:
#     def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
#         """
#         Do not return anything, modify nums1 in-place instead.
#         """
#         nums1[m:] = nums2
#         nums1.sort()