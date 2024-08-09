# 二叉树展开为链表

# 一个神奇的二叉树拉直的思路,左子树变成右子树,右子树放到最下面

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        if not root:
            return 
        right = root.right
        self.flatten(root.left)
        self.flatten(root.right)
        root.left, root.right = None, root.left
        tmp = root
        while tmp.right:
            tmp = tmp.right
        tmp.right = right
        
