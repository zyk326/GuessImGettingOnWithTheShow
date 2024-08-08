# LRU缓存

# 华为 字节笔试题
# 一个python的点，__slot__ 变量可以阻止实例化类的时候为实力分配__dict__，这里面声明的变量变成了类的描述符，相当于c++的成员变量声明。
# 该实例只能有slots中定义的变量，且不能再增加新的变量。定义了slot就不能再有dict

# 这是一个字典和实际链表节点分离的思想，虽然里面存放的值都是一样的，节点也是同样的节点，可以说是一个元素体现在了两个数据结构上。

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