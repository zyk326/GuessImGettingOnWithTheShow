# 二叉树的层平均值

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        que = []
        que.append([root, 0])
        depth = 0
        bufsum = 0
        ans = []
        nums = 0
        while que:
            node, dep = que.pop(0)
            if dep != depth:
                ans.append(bufsum / nums)
                bufsum = 0
                nums = 0
                depth += 1
            bufsum += node.val
            nums += 1
            if node.left:
                que.append([node.left, dep + 1])
            if node.right:
                que.append([node.right, dep + 1])
        ans.append(bufsum / nums)
        return ans