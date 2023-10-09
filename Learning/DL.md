# 深度学习
深度学习的核心来自神经网络(可以看做一门语言),它是一个非常灵活的框架(组合神经元来表达问题的先验知识).   

#### **跳转**  
[数据](#数据) [线性代数](#线性代数) [矩阵计算](#矩阵计算)  
[待学链接](#这里是待学链接)

![AI地图](./img/AIMap.png)  

#### 机器学习/深度学习 的应用  
* 图片分类  
* 物体检测(*人在什么地方*)和分割(*每一个像素属于飞机还是人*)  
* 样式迁移  
* 人脸合成  
* 文字生成图片  
* 文字生成(*GPT*)  
* 无人驾驶
>案例研究：广告点击  
特征提取（*广告主；产品描述；产品图片*） => 模型（训练数据【过去广告展现和用户点击】 -> 特征和用户点击 -> 模型） => 点击率预测

### 环境安装
> 前置conda  

```
conda env remove d2l-zh  
conda create -n d2l-zh python==3.8
conda activate d2l-zh  
pip install d2l torch torchvision  
```
[d2l资源包下载点击此处](https://zh-v2.d2l.ai/d2l-zh.zip) 


## 数据
#### n维度数组是机器学习和神经网络的主要数据结构  

> 0-d(标量)(一个类别)   
> 1-d(向量)(一个特征向量)  
> 2-d(矩阵)(一个样本-特征矩阵)(行是样本,列是特征)  
> 3-d **RGB图片** (宽x高x通道)  
> 4-d **一个RGB图片的批量** (批量大小x宽x高x通道)  
> 5-d **视频批量** (批量大小x时间x宽x高x通道)

创建数组需要三个东西 : **形状 + 数据类型 + 元素值**

**[这里是代码预览](../Code/Preview/data.md)**   
###### [这里是数据代码下载](../Code/data.ipynb)  

标准的算术运算(+ - * / **)都是按元素运算的

张量(tensor)就是多维数组

**广播机制** : 用于维度不同的两个张量执行元素操作,具体是shape中数字向上变化.  
> eg. a.shape = (3, 1) b.shape = (1, 2)  
> trans to a.shape = (3, 2) b.shape = (3, 2)  
> [0] &emsp;  [0] [0]  &emsp;&emsp;[2, 3] &emsp; [2] [3]  
> [1] to [1] [1]  &emsp; &emsp;&emsp;&emsp; to [2] [3]  
> [2] &emsp; [2] [2]  &emsp;&emsp; &emsp; &emsp;&emsp; [2] [3]

执行原地操作:
```
# 创建一个shape与Y相同,元素全为0的张量Z
Z = torch.zeros_like(Y)
Z[:] = X + Y
# 执行完之后,Z的id与会与Z之前保持一致,原因是没有找一个新的变量来保存结果(没有重新分配内存),只是改变了Z中的值.
# 如果不需要保存x的值,则可以直接在x所处内存中直接改写值:
X += Y
# 这样也不会改变X的id,也是原地操作
```
Numpy的ndarray可以转换为torch的Tensor
```
A = X.numpy()
B = torch.tensor(A)
type(A), type(B)
=>(numpy.ndarray, torch.Tensor)
```

## 线性代数

矩阵可以把向量扭曲,**方向不会被矩阵改变的向量是特征向量**  

![矩阵扭曲向量](./img/Matrix%20distortion.png)

> 标量的shpe是空的

**[这里是代码预览](../Code/Preview/Linear%20algebra.md)**  

## 矩阵计算

> 主要问题是看矩阵怎么求导数(模型的优化求解都是通过求导数进行的)

![向量和标量的各种组合乘积](./img/vector%20puls%20vector.png)

> ∂y/∂**x** 是行向量,∂**y**/∂x 是列向量 (x,y本身就是列向量), ∂**y**/∂**x** 是一个矩阵

![向量乘以向量](./img/vector%20puls%20vector%20true.png)

## 自动求导

![反向传递](./img/Back-propagation.png)

---
## [这里是待学链接](https://www.bilibili.com/video/BV1eK4y1U7Qy/?spm_id_from=333.999.0.0&vd_source=5a8651962259df7b14781b1d0370c6a0)