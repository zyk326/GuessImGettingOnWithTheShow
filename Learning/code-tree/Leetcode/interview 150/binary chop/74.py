# 搜索二维矩阵

# 可能有不存在的情况,所以不能用yxc的板子

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False
            
        r, c = len(matrix), len(matrix[0])
        
        # 查找目标所在的行
        lr, rr = 0, r - 1
        while lr <= rr:
            mid = (lr + rr) // 2
            if matrix[mid][0] > target:
                rr = mid - 1
            else:
                lr = mid + 1
                
        # 确定目标行
        row = rr
        if row < 0:
            return False  # 要搜索的行超出范围
        
        # 查找目标所在的列
        lc, rc = 0, c - 1
        while lc <= rc:
            mid = (lc + rc) // 2
            if matrix[row][mid] > target:
                rc = mid - 1
            elif matrix[row][mid] < target:
                lc = mid + 1
            else:
                return True  # 找到目标
                
        return False  # 没有找到目标

# 这个是必找到值的方法,用了yxc的板子
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        r, c = len(matrix), len(matrix[0])
        lr, rr = 0, r - 1
        while(lr < rr):
            mid = (lr + rr + 1) >> 1
            if matrix[mid][0] > target:
                rr = mid - 1
            else:
                lr = mid
        
        lc, rc = 0, c - 1
        while(lc < rc):
            mid = (lc + rc + 1) >> 1
            if matrix[lr][mid] > target:
                rc = mid - 1
            elif matrix[lr][mid] < target:
                lc = mid
            else:
                return True
        return matrix[lr][lc] == target