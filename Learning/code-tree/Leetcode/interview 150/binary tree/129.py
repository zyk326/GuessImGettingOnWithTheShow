# 求根节点到叶节点数字之和

# 一个python的用法:
# 在函数内部修改外部变量时,需要声明nonlocal

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        sums = 0
        def dfs(root, num):
            nonlocal sums
            if not root:
                return
            if not root.left and not root.right:
                sums += int(num + str(root.val))
            dfs(root.left, num + str(root.val))
            dfs(root.right, num + str(root.val))
        dfs(root, '')
        return sums