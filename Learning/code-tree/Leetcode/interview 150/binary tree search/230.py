# 二叉搜索树中第K小的元素

# 一种递归中不返回值的结构,在递归里面更改局部的全局变量.  

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        res = 0
        def dfs(root):
            nonlocal res, k
            if not root or k < 1:
                return
            dfs(root.left)
            if k == 1:
                res = root.val
            k -= 1
            dfs(root.right)
        dfs(root)
        return res