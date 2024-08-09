# 二叉树的最大深度

# 没啥好说的,深搜,递归的实现

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        dep = 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
        return dep