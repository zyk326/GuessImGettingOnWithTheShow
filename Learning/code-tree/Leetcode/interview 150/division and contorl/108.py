# 将有序数组转换为二叉搜索树

# 把中间的节点变陈当前位置的根节点就好了

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        n = len(nums)
        if n == 0:
            return None
        left = self.sortedArrayToBST(nums[ : n // 2])
        right = self.sortedArrayToBST(nums[n // 2 + 1 : ])
        return TreeNode(nums[n // 2], left, right)