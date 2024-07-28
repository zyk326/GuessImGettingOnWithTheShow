# 跳跃游戏ii

nums = list(map(int, input().split()))
n = len(nums)
st = [0 for i in range(11100)]
for i, jump in enumerate(nums):
    for j in range(1, jump + 1):
        print(i, jump)
        if st[i + j] == 0:
            st[i + j] = st[i] + 1
    print(st[:15])


class Solution:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return 0
        st = [0 for i in range(11100)]
        for i, jump in enumerate(nums):
            for j in range(1, jump + 1):
                print(i, jump)
                if st[i + j] == 0:
                    st[i + j] = st[i] + 1
        return st[n - 1]