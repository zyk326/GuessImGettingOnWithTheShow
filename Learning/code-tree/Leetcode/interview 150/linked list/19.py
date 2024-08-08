# 删除链表的倒数第N个结点

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        left = right = dummy = NodeList(next = head)
        for _ in range(n):
            right = right.next

        while(right.next):
            left = left.next
            right = right.next
        left.next = left.next.next
        return dymmy.next