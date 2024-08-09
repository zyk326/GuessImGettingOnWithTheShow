# 二叉树中的最大路径和

# 递归的神奇 用法注意,这里是链,所以可以遍历一个节点和它的左右子链来看这条路径是不是最大的

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        ans = float('-INF')
        def dfs(root):
            if not root:
                return 0
            l_val = dfs(root.left)
            r_val = dfs(root.right)
            nonlocal ans
            ans = max(ans, l_val + r_val + root.val)
            return max(max(l_val, r_val) + root.val, 0)
        dfs(root)
        return ans