# 买卖股票的最佳时机

# 用指针标记最小并只比较当前日期卖出，可以大大减少计算量
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        cost, profit = float("INF"), float("-INF")
        for price in prices:
            cost = min(cost, price)
            profit = max(profit, price - cost)
        return profit

# 分割线找左边的最小和右边的最大，会超时，因为会存在大量的重复计算
class Solution:
    def deal(self, prices: List[int], sk: int, n: int):
        mi, ma = float("INF"), float("-INF")
        for i in range(sk + 1):
            mi = min(mi, prices[i])
        for i in range(sk, n):
            ma = max(ma, prices[i])
        return mi, ma

    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        left = []
        right = []
        for i in range(n):
            a, b = self.deal(prices, i, n)
            left.append(a)
            right.append(b)
        ans = -1
        for i in range(n):
            ans = max(ans, right[i] - left[i])
        return ans