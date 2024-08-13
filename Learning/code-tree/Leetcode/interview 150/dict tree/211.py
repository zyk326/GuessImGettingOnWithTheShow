# 添加与搜索单词-数据结构设计

# 这里有一种dfs的写法

class Node():
    def __init__(self) -> None:
        self.children = [None] * 26
        self.isEnd = False

class WordDictionary:

    def __init__(self):
        self.root = Node()

    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            id_ = ord(char) - ord('a')
            if not node.children[id_]:
                node.children[id_] = Node()
            node = node.children[id_]
        node.isEnd = True

    def search(self, word: str) -> bool:
        return self.__dfs_search(word, 0, self.root)
    
    def __dfs_search(self, word: str, idx: int, node: Node) -> bool:
        if idx == len(word):
            return node.isEnd
        if word[idx] == '.':
            for child in node.children:
                if child and self.__dfs_search(word, idx + 1, child):
                    return True
        else:
            child = node.children[ord(word[idx]) - ord('a')]
            if child and self.__dfs_search(word, idx + 1, child):
                return True
        return False


# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)