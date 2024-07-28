# 文本左右对齐

# 这个可以好好再揣摩一下

class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        res, line, str_num = [], [], 0
        for word in words:
            if str_num + len(line) - 1 + len(word) >= maxWidth: # 之前的单词组长度，单词间隔，新的单词长度
                for i in range(maxWidth - str_num):
                    line[i % max(len(line) - 1, 1)] += ' '
                res.append(''.join(line))
                line, str_num = [], 0
            line.append(word)
            str_num += len(word)
        return res + [' '.join(line).ljust(maxWidth)]