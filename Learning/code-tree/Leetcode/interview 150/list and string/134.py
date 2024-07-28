# 加油站

# 一道模拟题,也不是模拟题,需要判断当前油量最小的内部含义,考虑得到最小值结果和答案的关系
# 从最小值开始往后,均为正值

class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        have = gas[0] - cost[0]
        minnum = [have, 0]
        for i in range(1, len(gas)):
            have += gas[i] - cost[i]
            if have <= minnum[0]:
                minnum = [have, i]
        if have < 0:
            return -1
        return ((minnum[1] + 1) % len(gas)) #因为这里要得到可行的起始点,所以要在最小点处加1