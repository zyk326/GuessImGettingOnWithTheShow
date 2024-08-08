# 旋转链表

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head or k == 0:
            return head
        dummy = right = ListNode(next = head)
        n = 0
        while(right.next):
            right = right.next
            n += 1
        last = right
        right = dummy
        for _ in range(n - (k % n)):
            right = right.next
        neh = right.next
        last.next = dummy.next
        right.next = None
        return neh if neh else dummy.next
