# 二叉树的右视图

# 先递归右子树,在递归左子树,当某一层第一次到达的时候,就是答案
# 这里有一个ans的写法,if len(ans) == depth

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        ans = []
        def dfs(depth, root):
            if not root:
                return
            if depth == len(ans):
                ans.append(root.val)
            dfs(depth + 1, root.right)
            dfs(depth + 1, root.left)
        dfs(0, root)
        return ans
        