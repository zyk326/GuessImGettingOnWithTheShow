# 买卖股票的最佳时机ii

# 所有的上升交易日都买卖，从每一个小段做，这样直观地表现了没有漏掉每一个上升交易日
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        profit, temp = 0, 0
        for i in range(1, len(prices)):
            temp = prices[i] - prices[i -1]
            profit += temp if temp > 0 else 0
        return profit