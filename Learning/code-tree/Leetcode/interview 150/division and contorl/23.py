# 合并K个升序链表

# 这里涉及到一个堆的用法

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
ListNode.__lt__ = lambda a, b: a.val < b.val

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        dummy = ListNode()
        cur = dummy
        heap = []

        for head in lists:
            if head:
                heappush(heap, head)
        
        while heap:
            node = heappop(heap)
            cur.next = node

            if node.next:
                heappush(heap, node.next)
            
        return dummy.next