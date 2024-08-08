# 反转链表

# 链表的题目都好神奇啊,很神奇的链表思路

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        dummy = ListNode(next = head)
        p = dummy
        for i in range(left - 1):
            p = p.next
        cur = p.next
        pre = None
        for _ in range(right - left + 1):
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt

        p.next.next = cur
        p.next = pre
        return dummy.next