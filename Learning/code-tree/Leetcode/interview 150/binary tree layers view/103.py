# 二叉树的锯齿形层序遍历

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:    
        if not root:
            return []
        res, que = [], deque()
        que.append(root)
        while que:
            tmp = deque()
            for _ in range(len(que)):
                node = que.popleft()
                if len(res) % 2 == 0:
                    tmp.append(node.val)
                else:
                    tmp.appendleft(node.val)
                if node.left: que.append(node.left)
                if node.right: que.append(node.right)
            res.append(list(tmp))
        return res
