# 从前序与中序遍历序列构造二叉树

# 一个找根节点的逻辑,在前缀表达的节点集合中,右子树的根节点是当前跟节点+左子树的节点数量+1
# 把找右节点的公式找准之后,写函数内函数和函数逻辑框架都是一样的

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        def buildTrees(L, R, root):
            if L > R:
                return 
            node = TreeNode(preorder[root])
            i = dic[preorder[root]]
            node.left = buildTrees(L, i - 1, root + 1)
            node.right = buildTrees(i + 1, R, i - L + root + 1)
            return node
        
        dic = dict()
        # preorder = preorder
        for i, v in enumerate(inorder):
            dic[v] = i
        return buildTrees(0, len(inorder) - 1, 0)