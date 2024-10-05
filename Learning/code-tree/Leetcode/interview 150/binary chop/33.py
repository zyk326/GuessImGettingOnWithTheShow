# 搜索旋转排序数组

# 这个思路屌爆了

# 这里又要用=，因为要判断这个mid是不是target，然后，这个上取整不太好搞。

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1

        while l <= r:
            mid = (l + r) >> 1
            
            if nums[mid] == target:
                return mid
            
            if nums[l] <= nums[mid]:
                if nums[l] <= target < nums[mid]:
                    r = mid - 1
                else:
                    l = mid + 1
            else:
                if nums[mid] < target <= nums[r] :
                    l = mid + 1
                else:
                    r = mid - 1
        return -1