# 随机链表的复制 

# 用hash表存所有的节点,然后来配置next和random
# 感觉是用dict模拟了一个链表,在node上加了一个数据结构的维度
# 据说大厂很喜欢考这个

"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head:
            return
        dict = {}
        cur = head
        while cur:
            dict[cur] = Node(cur.val)
            cur = cur.next
        cur = head
        while cur:
            dict[cur].next = dict.get(cur.next)
            dict[cur].random = dict.get(cur.random)
            cur = cur.next
        return dict[head]