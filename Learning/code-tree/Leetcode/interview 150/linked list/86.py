# 分隔链表

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        dummy = ListNode(next = head)
        small, big = ListNode(0), ListNode(0)
        sml, bg = small, big
        p = dummy
        while p.next:
            if p.next.val < x:
                sml.next = p.next
                p.next = p.next.next
                sml.next.next = None
                sml = sml.next
            else:
                bg.next = p.next
                p.next = p.next.next
                bg.next.next = None
                bg = bg.next
        sml.next = big.next
        bg.next = None
        return small.next