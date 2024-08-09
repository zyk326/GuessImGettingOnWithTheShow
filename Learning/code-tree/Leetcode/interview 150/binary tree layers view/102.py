# 二叉树的层序遍历

# 一个点,双端队列deque的popleft是O(1),que的pop(0)是O(n)的

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root: return []
        res, que = [], deque()
        que.append(root)
        while que:
            tmp = []
            for _ in range(len(que)):
                node = que.popleft()
                tmp.append(node.val)
                if node.left: que.append(node.left)
                if node.right: que.append(node.right)
            res.append(tmp)
        return res