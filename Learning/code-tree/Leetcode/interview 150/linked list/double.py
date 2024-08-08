class Node:
    __slot__ = 'prev', 'next', 'key', 'value'

    def __init__(self, value = 0, key = 0):
        self.value = value
        self.key = key

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_to_node = dict()
        self.dummy = Node()
        self.dummy.next = self.dummy
        self.dummy.pre = self.dummy

    def get_node(self, key: int) -> Optional[Node]:
        if key not in self.key_to_node:
            return None
        node = self.key_to_node[key]
        self.remove(node)
        self.put_front(node)
        return node

    def get(self, key: int) -> int:
        node = self.get_node(key)
        return node.value if node else -1

    def put(self, key: int, value: int) -> None:
        node = self.get_node(key)
        if node:
            node.value = value
            return 
        self.key_to_node[key] = node = Node(value, key)
        self.put_front(node)
        if len(self.key_to_node) > self.capacity:
            delnode = self.dummy.prev
            del self.key_to_node[delnode.key]
            self.remove(delnode)
        
    def remove(self, node : Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def put_front(self, node : Node):
        node.next = self.dummy.next
        node.prev = self.dummy
        self.dummy.next.prev = node
        self.dummy.next = node
        



# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)