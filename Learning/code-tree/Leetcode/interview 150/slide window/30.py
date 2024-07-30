# 串联所有单词的子串

# 这个思路非常绝,建议反复观看

# 这段代码实现了在字符串 s 中找到一个包含所有指定单词的连续子串的起始索引。这里有详细的解释和步骤：

### 代码分解

# 1. **定义函数与初始化变量**
    
#     class Solution:
#         def findSubstring(self, s: str, words: List[str]) -> List[int]:
    
#     - 定义了一个名为 findSubstring 的函数，参数为字符串 s 和一个字符串列表 words。
#     - word_len 是每个单词的长度（假设所有单词长度相同）。
#     - word_num 是单词的数量。
#     - window 是包含所有单词的子串的总长度。
#     - ans 是保存结果的列表。

# 2. **初始化单词计数器**
    
#         cnt = {word: 0 for word in words}
#         word_cnt = cnt.copy()
#         for word in words:
#             word_cnt[word] += 1
    
#     - cnt 和 word_cnt 是两个字典，用于记录每个单词的出现次数。cnt 用于计数当前窗口的单词次数，word_cnt 记录目标单词的次数。

# 3. **遍历字符串**
    
#         start = 0
#         while start < len(s) - window + 1:
    
#     - start 是当前窗口的起始位置。while 循环确保窗口不会越界。

# 4. **检查当前窗口中的单词**
    
#             tmp_cnt = cnt.copy()
#             for i in range(start, start + window, word_len):
#                 tmp_word = s[i:i + word_len]
#                 if tmp_word in tmp_cnt:
#                     tmp_cnt[tmp_word] += 1
#                 else:
#                     break
    
#     - 在每个窗口内初始化一个临时计数器 tmp_cnt。
#     - 遍历窗口内的每个单词，并检查它们是否在 tmp_cnt 中。如果是，增加相应的计数；如果不是，跳出循环。

# 5. **比较计数器**
    
#             if tmp_cnt == word_cnt:
#                 ans.append(start)
#             start += 1
    
#     - 比较 tmp_cnt 和 word_cnt，如果它们相等，说明当前窗口包含所有目标单词的正确次数，将 start 添加到结果列表 ans 中。
#     - 将 start 增加1，继续检查下一个窗口。

# 6. **返回结果**
    
#         return ans
    
#     - 返回包含所有符合条件的起始索引的列表 ans。

# ### 总结

# 这个算法利用滑动窗口和计数器来高效地查找字符串 s 中所有包含 words 列表中所有单词的连续子串的起始位置。通过这种方式，可以在合理的时间复杂度内解决问题。

# 字典的合理运用是很好的
# 怎么说这题叫滑动窗口呢

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        word_len = len(words[0])
        words_len = len(words)
        window = word_len * words_len
        start = 0
        cnt = {word : 0 for word in words}
        tmp_dic = cnt.copy()
        ans = []
        for i in words:
            tmp_dic[i] += 1
        while(start < len(s) - window + 1):
            words_dic = cnt.copy()
            for i in range(start, start + window, word_len):
                buf_s = s[i : i + word_len]
                if buf_s in words_dic:
                    words_dic[buf_s] += 1
                else:
                    break
            if words_dic == tmp_dic:
                ans.append(start)
            start += 1
        return ans