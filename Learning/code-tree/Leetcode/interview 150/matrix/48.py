# 旋转图像

# 无聊的找规律题,重点是行列变换公式
# 一个点,浅拷贝是改变拷贝,源也会改,深拷贝是改了不会改源
# 浅拷贝只用a.copy()
# 深拷贝要导入copy模块,用法:copy.deepcopy(list)

class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        tmp = copy.deepcopy(matrix)
        for i in range(n):
            for j in range(n):
                matrix[j][n - i - 1] = tmp[i][j]