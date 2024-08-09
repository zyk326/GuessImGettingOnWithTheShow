# 对称二叉树

# 一个python的写法,def里面定义def
# 然后在最外层调用这个函数
# 还有就是一个很神奇的逻辑,跳出条件的写法,也可以说是递归的写法,仔细品代码

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def iscur(L, R):
            if not L and not R: return True
            if not L or not R or L.val != R.val: return False
            return iscur(L.left, R.right) and iscur(L.right, R.left)
        return not root or iscur(root.left, root.right)