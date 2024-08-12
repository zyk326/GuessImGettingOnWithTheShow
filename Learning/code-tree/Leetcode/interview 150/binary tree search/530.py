# 二叉搜索树的最小绝对值

# 一个python的用法:yield,生成器,不返回所有值,而是一次生成一个值,yield from可以委托另一个生成器执行.  
# 另一个python的用法:pairwise,获取连续的两个数.  

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
        def dfs(root):
            if not root:
                return
            yield from dfs(root.left)
            yield root.val
            yield from dfs(root.right)
        return min(b - a for a, b in pairwise(dfs(root)))