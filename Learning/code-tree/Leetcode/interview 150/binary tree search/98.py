# 验证二叉搜索树

# 用中序遍历来看树的合法性

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        pre = -inf
        def check(root):
            nonlocal pre
            if not root:
                return True
            if not check(root.left):
                return False
            if pre >= root.val:
                return False
            pre = root.val
            return check(root.right)
        return check(root)