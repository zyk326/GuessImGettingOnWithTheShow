# 373. 查找和最小的 K 对数字
# 中等
# 相关标签
# 相关企业
# 给定两个以 非递减顺序排列 的整数数组 nums1 和 nums2 , 以及一个整数 k 。

# 定义一对值 (u,v)，其中第一个元素来自 nums1，第二个元素来自 nums2 。

# 请找到和最小的 k 个数对 (u1,v1),  (u2,v2)  ...  (uk,vk) 。

 

# 示例 1:

# 输入: nums1 = [1,7,11], nums2 = [2,4,6], k = 3
# 输出: [1,2],[1,4],[1,6]
# 解释: 返回序列中的前 3 对数：
#      [1,2],[1,4],[1,6],[7,2],[7,4],[11,2],[7,6],[11,4],[11,6]
# 示例 2:

# 输入: nums1 = [1,1,2], nums2 = [1,2,3], k = 2
# 输出: [1,1],[1,1]
# 解释: 返回序列中的前 2 对数：
#      [1,1],[1,1],[1,2],[2,1],[1,2],[2,2],[1,3],[1,3],[2,3]

# import heapq
# nums1 = [1,1,2]
# nums2 = [1,2,3]
# k = 2
# ans = []
# flag, ans = (n := len(nums1)) > (m := len(nums2)), []
# if flag:
#     n, m, nums1, nums2 = m, n, nums2, nums1
# pq = []
# for i in range(min(n, k)):
#     heapq.heappush(pq, (nums1[i] + nums2[0], i, 0))
# while(len(ans) < k and pq):
#     _, a, b = heapq.heappop(pq)
#     ans.append([nums2[b], nums1[a]] if flag else [nums1[a], nums2[b]])
#     if b + 1 < m:
#         heapq.heappush(pq, (nums1[a] + nums2[b + 1], a, b + 1))
# print(ans)


nums1 = [1,7,11]
nums2 = [2,4,6]
k = 3

import heapq
hp = []
flag, ans = (n := len(nums1)) > (m := len(nums2)), []
if flag:
    n, m, nums1, nums2 = m, n, nums2, nums1
for i in range(n):
    heapq.heappush(hp, (nums1[i] + nums2[0], i, 0))
while len(ans) < k and hp:
    _, a, b = heapq.heappop(hp)
    ans.append([nums2[b], nums1[a]] if flag else [nums1[a], nums2[b]])
    if b + 1 < m:
        heapq.heappush(hp, (nums1[a] + nums2[b + 1], a, b + 1))
print(ans)