# 路径总和

# python的写法:if xxx: return xx == xx
# 还有,判断叶子结点就是要看你的左右是不是空,而不是当前是不是空

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        def dfs(root, sums):
            if not root:
                return False
            if not root.left and not root.right:
                return root.val == sums
            return self.hasPathSum(root.left, sums - root.val) or self.hasPathSum(root.right, sums - root.val)
        return dfs(root, targetSum)