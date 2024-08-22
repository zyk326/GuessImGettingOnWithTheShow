# 电话号码的字母组合

# 这题感觉主要锻炼递归这种写法比较重点

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        phone = {'2':['a','b','c'],
                 '3':['d','e','f'],
                 '4':['g','h','i'],
                 '5':['j','k','l'],
                 '6':['m','n','o'],
                 '7':['p','q','r','s'],
                 '8':['t','u','v'],
                 '9':['w','x','y','z']}

        res = []        
        def backtrack(combination, nextdigit):
            if not nextdigit:
                res.append(combination)
            else:
                for char in phone[nextdigit[0]]:
                    backtrack(combination + char, nextdigit[1:])

        backtrack('', digits)
        return res