li = list(map(int, input().split()))

le = len(li)
dp = [[1 for _ in range(le + 10)] for _ in range(le + 10)]

def isup(a, b):
    return 0 if a < b else 1

for i in range(le):
    for j in range(i + 1, le):
        dp[i][j] = dp[i][j - 1] - isup(li[j - 1], li[j]) # 只有是递增序列我才会保持1,否则会小于1

for i in range(le):
    print(dp[i][0:le])

ans = 0
for i in range(le):
    for j in range(i, le):
        if i == 0 and j == le - 1:
            ans += 1
            continue
        if i - 1 >= 0 and j + 1 < le:
            if dp[0][i - 1] == 1 and dp[j + 1][le - 1] == 1 and li[i - 1] < li[j + 1]:
                ans += 1
        if i == 0:
            if dp[j + 1][le - 1] == 1:
                ans += 1
        if j == le - 1:
            if dp[0][i - 1] == 1:
                ans += 1
print(ans)




# leetcode 版本
class Solution:
    def isup(self, a, b):
        return 0 if a < b else 1

    def incremovableSubarrayCount(self, nums: List[int]) -> int:
        li = nums
        le = len(nums)
        dp = [[1 for _ in range(le + 10)] for _ in range(le + 10)]
        for i in range(le):
            for j in range(i + 1, le):
                dp[i][j] = dp[i][j - 1] - self.isup(li[j - 1], li[j]) # 只有是递增序列我才会保持1,否则会小于1

        ans = 0
        for i in range(le):
            for j in range(i, le):
                if i == 0 and j == le - 1:
                    ans += 1
                    continue
                if i - 1 >= 0 and j + 1 < le:
                    if dp[0][i - 1] == 1 and dp[j + 1][le - 1] == 1 and li[i - 1] < li[j + 1]:
                        ans += 1
                if i == 0:
                    if dp[j + 1][le - 1] == 1:
                        ans += 1
                if j == le - 1:
                    if dp[0][i - 1] == 1:
                        ans += 1
        return ans