# 填充每个节点的下一个右侧节点指针ii

# 很神奇的dfs思路,把第一次深搜出来的节点作为pre数组,value是node,在后序的所有当前depth层都将作为pre[depth]的后序next
# 也可以用BFS做,这里涉及一个pairwise的 用法.获取两个连续的元素.  

"""
# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next
"""

class Solution:
    def connect(self, root: 'Node') -> 'Node':
        pre = []
        def dfs(node, depth):
            if not node:
                return
            if depth == len(pre):
                pre.append(node)
            else:
                pre[depth].next = node
                pre[depth] = node
            dfs(node.left, depth + 1)
            dfs(node.right, depth + 1)
        dfs(root, 0)
        return root