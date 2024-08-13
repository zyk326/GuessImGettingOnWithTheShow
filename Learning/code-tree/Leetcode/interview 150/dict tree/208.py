# 实现Trie(前缀树)

# 把前缀树的概念搞清楚就能写,前缀树就是用每一个路径代表某一位上有某一值,从而搞成一个树的样子.  

class Node:
    def __init__(self):
        self.children = [None] * 26
        self.isend = False

class Trie:

    def __init__(self):
        self.root = Node()

    def insert(self, word: str) -> None:
        node = self.root
        for chr in word:
            id_ = ord(chr) - ord('a')
            if not node.children[id_]:
                node.children[id_] = Node()
            node = node.children[id_]
        node.isend = True

    def search(self, word: str) -> bool:
        node = self.__search_prefix(word)
        return node != None and node.isend
    
    def startsWith(self, prefix: str) -> bool:
        return self.__search_prefix(prefix) != None

    def __search_prefix(self, word: str) -> bool:
        node = self.root
        for chr in word:
            node = node.children[ord(chr) - ord('a')]
            if not node:
                return 
        return node

# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)