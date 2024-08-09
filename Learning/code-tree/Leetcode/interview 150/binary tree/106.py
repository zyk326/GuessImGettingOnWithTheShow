# 从中序与后序遍历序列构造二叉树

# 重要的还是那个公式

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        dic = {}
        postorder = postorder
        for i, v in enumerate(inorder):
            dic[v] = i
        
        def buildtrees(L, R, root):
            if L > R:
                return 
            node = TreeNode(postorder[root])
            i = dic[postorder[root]]
            node.left = buildtrees(L, i - 1, root - R + i - 1)
            node.right = buildtrees(i + 1, R, root - 1)
            return node
        return buildtrees(0, len(inorder) - 1, len(inorder) - 1)