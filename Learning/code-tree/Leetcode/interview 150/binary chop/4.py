class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        if len(a) > len(b):
            a, b = b, a

        m, n = len(a), len(b)
        l, r = 0, m
        while(l <= r):
            i = (l + r) // 2
            j = (m + n) // 2 - i

            max_a_left = a[i - 1] if i > 0 else float('-inf')
            min_a_right = a[i] if i < m else float('inf')
            max_b_left = b[i - 1] if j > 0 else float('-inf')
            min_b_right = b[i] if j < n else float('inf')

            if max_a_left < min_b_left and min_a_right > max_b_left:
                if (m + n) % 2 == 0:
                    return (max(max_a_left, max_b_left) + min(min_a_right, min_b_right)) / 2
                else:
                    return max(max_a_left, max_b_left)
            elif max_a_left > min_b_right:
                right = i - 1
            else:
                left = i + 1

        return ValueError("error")  