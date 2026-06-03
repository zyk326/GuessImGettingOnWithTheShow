# 算法 DRI-Cover 实战攻略

> **版本** v1.0  
> **来源** 内部项目经验总结  
> **范围** 涵盖深度学习算法与 HALCON 传统算法两大板块

---

## 总目录

- **第一部分：深度学习算法**
- **第二部分：HALCON 传统算法**

---

# 第一部分：深度学习算法

---

## 目录（第一部分）

1. [工程搭建](#1-工程搭建)
2. [训练脚本配置说明](#2-训练脚本配置说明)
3. [数据集转换](#3-数据集转换)
4. [模型划分方法论](#4-模型划分方法论)
5. [DFM 设计文档分析](#5-dfm-设计文档分析)
6. [模型检出分析及优化](#6-模型检出分析及优化)
7. [项目推进流程](#7-项目推进流程)
8. [缺陷评估与报告](#8-缺陷评估与报告)
9. [模型训练实操](#9-模型训练实操)
10. [Alpha Vision 部署](#10-alpha-vision-部署)
11. [DRI 算法处理专项](#11-dri-算法处理专项)
12. [模型部署与 DLL 打包](#12-模型部署与-dll-打包)
13. [项目实践记录](#13-项目实践记录)

---

## 1. 工程搭建

### 1.1 目录结构规范

为防止文件杂糅，采用三级目录结构进行工程化管理：

```
train_data_xxx/                          # 一级：个人工作空间
├── V8/                                  # 二级：YOLO 版本隔离（V8 / V12 等）
│   ├── Code/                            # 三级：训练工程
│   │   └── train_FLW_part/              # 单个项目工作空间
│   │       ├── DataYamls/               # 数据集说明 YAML（数据在哪 + 类别是什么）
│   │       ├── PyFiles/                 # 训练启动 PY 文件 + yolovxn.pt 预训练权重
│   │       └── Runs/                    # 训练结果输出
│   └── data/                            # 三级：数据集
│       └── LY_B868TMM/                  # 项目文件夹
│           ├── TMM_A/                   # A 面模型数据
│           ├── TMM_B/                   # B 面模型数据
│           └── TMM_CD/                  # C/D 面模型数据
```

### 1.2 DataYaml 字段说明

| 字段 | 说明 |
|------|------|
| `path` | 数据集存储路径（绝对路径） |
| `train` / `val` | 训练集/验证集相对路径 |
| `nc` | number of classes，类别数量 |
| `names` | 从 0 开始的类别名称列表 |

### 1.3 文件对应规范

一个模型 PY 文件对应一个 DataYaml，一个 DataYaml 对应 data 下的一个数据区块。

---

## 2. 训练脚本配置说明

### 2.1 关键参数一览

| 参数 | 用途 | 说明 |
|------|------|------|
| `project` | 结果保存目录 | 所有训练产物均保存至此路径 |
| `name` | 结果文件夹名称 | 建议加入时间后缀以区分 |
| `weights` | 模型架构/预训练权重 | 可传 .pt 文件或模型 yaml 路径；使用 `-p6` 后缀时 imgsz 需为 64 的倍数 |
| `data` | 数据集 YAML 路径 | 指向 DataYaml 文件 |
| `epochs` | 训练轮次 | 默认 300，随数据集大小调整 |
| `batch` | 批次大小 | 控制 BN、显存、速度、泛化，默认 16/32 |
| `imgsz` | 输入图片尺寸 | 控制检测精度与显存；非 -p6 模型为 32 的倍数 |
| `device` | 推理设备 | 显卡编号，逗号分隔 |
| `workers` | 数据加载进程数 | 默认 8/16 |
| `resume` | 断点续训 | 自动读取 last.pt 继续训练 |

### 2.2 训练产物

| 产物 | 路径 | 说明 |
|------|------|------|
| 训练指标 | `[project]/results.csv` | 每个 epoch 的详细指标 |
| 模型权重 | `[project]/weights/best.pt` / `last.pt` | 一般情况下使用 best.pt |
| 训练配置 | `[project]/args.yaml` | 所有训练配置的溯源备份 |
| BoxPR 曲线 | — | 目标框对测试集的拟合程度 |
| MaskPR 曲线 | — | 掩码对测试集的拟合程度 |

### 2.3 超参数调整

默认超参数在 `ultralytics/cfg/default.yaml` 中。修改时只需在 `model.train()` 的参数列表中传入 `<超参数名=指定值>` 即可。

---

## 3. 数据集转换

### 3.1 数据源路径

```
\\172.16.3.238\标注数据\<具体项目>
```

### 3.2 转换脚本说明

使用 `data_conversion_utils` 工具包。核心修改三个部分：

**① folder_path & target_names**

- `folder_path`：标注完成的文件夹根目录
- `target_names`：本次要转换的文件夹名称列表（如 A1, A2）

**② category_map_txt_path**

- 手动创建的缺陷列表 TXT 文件
- 将所有缺陷名称按行排列
- 行的 index 即为转换后的缺陷 index
- 顺序必须与 DataYaml 中 names 的顺序一致

**③ save_path**

- 转换结果保存路径
- 生成以下子目录：

| 目录/文件 | 说明 |
|-----------|------|
| `images/` | 图片文件（含训练集/测试集划分） |
| `labels/` | 从 JSON 转换而来的 TXT 标注文件 |
| `txt/` | 转换日志和错误日志 |
| `label_name.txt` | 缺陷名称对照文件 |

### 3.3 重要注意事项

- 分割模型（-segment）与检测模型（-detect）所需数据格式**不相同**
- 单日多次转换需区分时，可在 `lab2yoloseg_factor_implement.py` 的 `save_data` 方法中在 `curr_time` 后加后缀
- 覆写 TXT 后需删除对应的 `.cache` 文件
- 测试集转换出错时，会覆盖训练集的错误日志

### 3.4 数据集目录创建流程

```
data/
└── <项目文件夹>/           # 如 LY_B868TMM
    ├── <模型名_A>/         # 如 TMM_A
    │   └── 缺陷列表.txt
    ├── <模型名_B>/
    └── <模型名_CD>/
```

从零开始：在 data 下创建项目文件夹 → 创建以模型为单位的细分文件夹 → 在每个细分文件夹中创建缺陷列表 TXT。

---

## 4. 模型划分方法论

> 划分模型是基本功，划分结果浓缩体现在缺陷对照表上。

### 4.1 划分依据

| 考量维度 | 说明 |
|----------|------|
| 光源信息 | 光源一致 → 成像有一致可能 |
| 检测类型 | 缺陷类型 + 光源都一致 → 可合并 |
| 图片尺寸 | 尺寸接近 → 有合并可能 |
| **根本原则** | **缺陷成像特征一致性** |

### 4.2 操作要点

- 使用 DFM 的标定最小 NG 尺寸计算缺陷像素块个数
- 图片数量、检测类型需均衡分配到各模型
- 无法确定缺陷检测方式时，查询光学报告并与光学工程师沟通

---

## 5. DFM 设计文档分析

### 5.1 重点关注内容

- 光源信息
- 拍照图片数量
- Station condition 的详细说明

### 5.2 分析流程

1. 查看检测区域设计部分
2. 使用多个 station 的信息判断模型合并可能性
3. 用 DFM 标定最小 NG 尺寸 × 单像素精度 计算缺陷像素块大小

---

## 6. 模型检出分析及优化

### 6.1 好模型的三要素

1. **数据质量** — 标注准确、噪声可控
2. **缺陷明确定义** — 形态边界清晰、标准统一
3. **缺陷数量分布均衡** — 各类别样本量接近

### 6.2 过杀与漏检处理

#### 缺失部件检测

```
缺陷检测模型（定位） → ROI 裁剪 → 分类模型（判定缺料与否）
```

两个模型串行运行。

#### 特征重叠误检

将误检部位打上标注加入训练，让模型主动学会区分。通过负样本建模，使 backbone 学到特征差异，分类头即可区分。

### 6.3 常见缺陷类型

| 类型 | 处理方式 |
|------|----------|
| 废料残留（多出部分） | 可直接标注 |
| 卷边折角 | 可直接标注 |
| 特征缺失型 | 核心是结构完整性对比 |
| 形态异常型 | 正品中不存在，出现即可疑 |

---

## 7. 项目推进流程

### 7.1 前期准备工作

1. **模型训练框架**
   - 确保能够正确运行
   - 制作模板训练框架压缩包，实现一键移植
   - *注：YOLOv5 在工业检测场景下，同等条件下性能优于 YOLOv8*

2. **数据增强工程**
   - 使用外置数据转换工具（非训练工程内的 `data_conversion_utils`）
   - 确保数据格式转换、标签统计、增强工具正确使用

### 7.2 评估报告产出

结合 DFM（PPT/PDF 格式均可）评估各缺陷类型，重点是：

- 认清缺陷特征
- 确定检测方法（AI / 传统算法介入）
- 给出三级风险标准（Low / Mid / High）
- Mid/High 风险需备注理由

### 7.3 总览表格制作

- 在企业微信智能表格中创建 overview 模板
- 算法主导表格框架，按模型划分确定结构
- 各项指标沿用历史指标
- 框架划分完成后，交光学等部门填充

---

## 8. 缺陷评估与报告

### 8.1 图片查看要点

- 重点关注**轻微缺陷** — 大部分漏检源于此
- PVD 前后的图片成像及缺陷类型有差别，需分别判断
- 若缺陷标注为"无成像"→ 图中无有效图像信息
- 若缺陷与表面相似 → 有过杀风险

**评估标准三要素：**

| 标准 | 说明 |
|------|------|
| 成像效果 | 缺陷在图中是否可见 |
| 混淆可能性 | 是否与正常纹理/特征相似 |
| 特征显式表达 | 缺陷是否有明确视觉特征 |

### 8.2 工控机配置

根据划分的模型及工位信息确定主副机承载方案：

- 图片量均衡
- 所分配机器模型量均衡

---

## 9. 模型训练实操

### 9.1 训练前数据准备

原始数据存放结构对标注组不友好时，使用脚本将其转换为以模型划分文件夹存放的形式。

### 9.2 训练模板工程配置

1. 生成训练模型对应的 PY 文件
2. 修改预训练权重路径
3. 修改数据 YAML（缺陷类型、数量、路径）
4. 修改 TXT 标签（缺陷名称与数据增强部分保持一致）

---

## 10. Alpha Vision 部署

### 10.1 操作规范

- 模型路径不能包含中文
- 模型转换参数需与训练参数对应（主要是 imgsz）
- 操作顺序：选算子 → 加载模型 → 选入图片路径

### 10.2 后处理配置

若前景背景值未显示，更换 AlphaVision 的四个文件（dll、lib、db 等）。

---

## 11. DRI 算法处理专项

### 11.1 工站分析

| 工站 | 说明 |
|------|------|
| 2F 正反面打光 | ROI 无配合、背面压伤、正印 |
| 3F 正反面打光 | ROI 尺寸、打标 |
| 4F | LK 正打检测字符（亮面）、背打检测字符（暗面） |
| 5F | 字符 |
| 6F 底拍 | 正面各尺寸检测 |
| 7F 侧拍 | 侧面各尺寸检测 |

### 11.2 检测组件说明

| 组件 | 检测内容 |
|------|----------|
| Camera_ROI_Measure | 测量 ROI 区域尺寸 |
| Crack_Detect | 检测压伤、刮伤等线性缺陷 |
| Defect_Detect | 通用缺陷检测 |
| OCR | 字符识别 |
| Align | 定位贴合 |

### 11.3 疑难缺陷分析

#### 1. 凹陷缺陷

- 凹陷在 7 个工站均无明显图像反应
- 深度小、面积大、光照变化不明显

**检测方法：** 结构光（激光轮廓仪）

- 激光线打到凹陷区域时，会在两侧形成倾斜的拐角
- 通过测量激光线的两个拐点的 X/Y 宽度判断是否凹陷
- 可以使用深度学习对激光图进行分类

#### 2. 碰刮伤／压伤

- 标准检测方法：Crack_Detect 组件
- 需根据实际情况设置阈值
- 配合 Align 定位可提高稳定性

#### 3. 侧面圆柱检测

- 打光方式：使用同轴光源 + 侧向光源组合
- 检测方式：搭配 Crack_Detect 或腐蚀分割

#### 4. 表面缺陷

- 对表面清洁度有较高要求
- 需优化预处理（去噪、增强）
- 若打光处理后仍难以解决，需与光学工程师沟通调整光源

---

## 12. 模型部署与 DLL 打包

### 12.1 部署流程

1. 使用 onnxruntime 部署 ONNX 模型
2. 使用 TensorRT 部署加速在 GPU 上运行的模型
3. 判断训练方式（seg / det）以匹配部署代码

### 12.2 工程配置要点

#### Visual Studio 配置

- 包含目录 → 头文件路径
- 库目录 → lib 路径
- 链接器 → 输入 → 附加依赖项

```
opencv_world460.lib
onnxruntime.lib
```

#### 注意事项

- CUDA 和 cuDNN 版本务必匹配；出现内存错误时，先检查版本兼容性
- 代码编写使用 **PImpl 设计模式**

### 12.3 DLL 打包

```cpp
#ifdef YOLOV11SEG_EXPORTS
#define YOLO_API __declspec(dllexport)
#else
#define YOLO_API __declspec(dllexport)
#endif

class YOLO_API YOLOV11Seg { ... };
```

- lib 为函数索引，可用目录 + 依赖项方式引用
- dll 建议放在 exe 同路径下

---

## 13. 项目实践记录

### 13.1 吉安·立讯（DRI 项目）

- 服务器：245（全部）、249（F2）
- 当前标注面：A / B / D / F
- 模型参数：`imgsz = 1088 × 1088`

#### D 面胶偏位缺陷

- 特征：包装薄膜贴合错位，两侧薄膜突出 + 未覆盖区域
- 处理方式：深度学习打标 → 数据均衡 → 模型训练
- 注意：胶偏位过杀较多，需重点考虑防过杀策略

### 13.2 东莞·领益 B25 iPhone Pro 卡针

- G 面为新增缺陷面，历史数据无需处理
- 历史模型分析结论：

| 对比项 | 结论 |
|--------|------|
| 侧面撕裂带 | 18 与 24 模型效果差别不大 |
| 冲压痕 | 检出效果较差，建议对这部分数据做增强 |
| 脏污 | 两者相近，24 偶有优势 |
| 边缘缺口 | 两者相差不大 |

### 13.3 Hinge

- 服务器：249
- 后处理异常：前景背景值未显示 → 更换 AlphaVision 的四个文件解决

---

# 第二部分：HALCON 传统算法

---

## 目录（第二部分）

14. [图像读取与显示](#14-图像读取与显示)
15. [ROI 感兴趣区域操作](#15-roi-感兴趣区域操作)
16. [颜色空间转换与图像信息](#16-颜色空间转换与图像信息)
17. [图像增强与预处理](#17-图像增强与预处理)
18. [边缘检测](#18-边缘检测)
19. [阈值分割与区域处理](#19-阈值分割与区域处理)
20. [区域生长与分水岭分割](#20-区域生长与分水岭分割)
21. [形状特征提取](#21-形状特征提取)
22. [灰度特征提取](#22-灰度特征提取)
23. [纹理分析](#23-纹理分析)
24. [形态学操作](#24-形态学操作)
25. [霍夫变换与直线检测](#25-霍夫变换与直线检测)
26. [骨架化与轮廓提取](#26-骨架化与轮廓提取)
27. [频域处理](#27-频域处理)
28. [算子选择思维导图](#28-算子选择思维导图)

---

## 14. 图像读取与显示

### `read_image`

```halcon
read_image(Image, "LSC.jpg")
```

| 项目 | 说明 |
|------|------|
| 算子说明 | 从磁盘读取图像，支持 BMP/JPEG/PNG/TIFF 等格式 |
| 使用场景 | 所有视觉任务的起点 |
| 选择理由 | 最基础的输入算子，扩展名可省略自动匹配 |

### 显示窗口相关

| 算子 | 说明 |
|------|------|
| `dev_open_window_fit_image` | 自动适配图像尺寸打开窗口 |
| `dev_open_window` | 手动指定位置和大小 |
| `dev_display` | 在活动窗口中显示图像/区域 |
| `dev_close_window` | 关闭窗口 |
| `dev_set_color("red")` | 设置显示颜色 |
| `dev_set_draw("fill"/"margin")` | 设置填充/轮廓模式 |
| `set_display_font` | 设置窗口字体 |
| `stop()` | 暂停调试（HALCON 中代替断点） |

---

## 15. ROI 感兴趣区域操作

> ROI 是机器视觉最重要的概念——缩小处理范围、排除背景干扰、提升速度和精度。

### 矩形 ROI

```halcon
* 平行矩形
gen_rectangle1(Reg, 281, 1060, 395, 1385)
reduce_domain(Image, Reg, ImageReduced)

* 旋转矩形
draw_rectangle2(WindowHandle, Row, Col, Phi, w, h)
gen_rectangle2(Rect, Row, Col, Phi, w, h)
reduce_domain(Image, Rect, ImageReduced2)

* 一步到位（平行矩形专用）
rectangle1_domain(Image, ImgReduced, 6, 529, 290, 1606)
```

| 算子 | 作用 | 适用场景 |
|------|------|----------|
| `gen_rectangle1` | 生成平行于坐标轴的矩形 | 简单裁切、固定 ROI |
| `draw_rectangle2` | 交互式画旋转矩形 | 需要人工定位的检测区域 |
| `gen_rectangle2` | 程序化生成旋转矩形 | 已知中心+角度的规则 ROI |
| `reduce_domain` | 用区域裁剪图像范围 | 所有 ROI 操作的核心步骤 |
| `rectangle1_domain` | 一步完成矩形裁切 | 快速平行矩形裁切 |

### 圆形 ROI

```halcon
gen_circle(Circle1, 100, 200, 50.5)
gen_circle(Circle2, 200, 300, 50.5)
union2(Circle1, Circle2, ROI)
reduce_domain(Image, ROI, ImageReduced)
```

当需要多个不相连区域组成一个 ROI 时，用 `union2` 合并。

---

## 16. 颜色空间转换与图像信息

### `rgb1_to_gray`

| 项目 | 说明 |
|------|------|
| 算子说明 | 将 RGB 三通道彩色图转为单通道灰度图 |
| 使用场景 | 绝大多数 HALCON 算子要求输入灰度图 |
| 选择理由 | 彩色图信息冗余、处理慢，灰度化后速度快且算法兼容性最好 |

### 图像信息查询

| 算子 | 作用 |
|------|------|
| `get_image_size` | 获取图像的宽高（像素） |
| `get_image_type` | 获取图像数据类型 |
| `get_image_pointer1` | 获取图像内存指针（用于外部接口） |

---

## 17. 图像增强与预处理

> 预处理的目标：让目标更明显、让噪声更弱、让后续分割更简单。

### `emphasize`

```halcon
emphasize(GrayImage, ImageEmphasize, 7, 7, 1)
```

自适应增强：均值滤波 + 原始图像加权叠加，突出细节。适合图像对比度不足、边缘模糊的场景。参数：滤波器宽度、高度、因子。

### `scale_image`（线性拉伸）

```halcon
scale_image(GrayImage, ImageScale, 1.5, -30)
```

线性灰度变换：`dst = src × Mult + Add`。Mult 增益 > 1 拉大差异，Add 偏移调整亮度。

### `invert_image`（取反）

```halcon
invert_image(Image, ImageInvert)
```

灰度取反：`dst = 255 - src`。某些算子对"暗背景亮目标"效果更好（如分水岭）。

### 高斯滤波

```halcon
gauss_filter(Image, ImageGauss, 5)
```

平滑噪声的同时保留边缘结构，比均值滤波更自然。

---

## 18. 边缘检测

### `sobel_amp`

```halcon
sobel_amp(Image, EdgeAmplitude, "sum_abs", 3)
```

Sobel 算子计算梯度幅值，速度快，适合初步定位。

### `sobel_dir`

```halcon
sobel_dir(Image, EdgeAmplitude, EdgeDirection, "sum_abs", 3)
```

同时输出梯度幅值 + 方向，适合 Hough 直线检测等需要方向信息的场景。

### `laplace_of_gauss` + `zero_crossing`

```halcon
laplace_of_gauss(Image, ImageLaplace, 3)
zero_crossing(ImageLaplace, RegionZeroCrossing)
```

LoG 算子（高斯拉普拉斯联合滤波）抗噪强，零交叉对应真实边缘。

### `edges_image`（Canny）

```halcon
edges_image(Img, Amp, Dir, "canny", 1, "nms", 20, 40)
```

高级边缘检测，支持 Canny/Deriche/Shen 等滤波器，是目前最稳定的边缘检测方法。

---

## 19. 阈值分割与区域处理

### `threshold`

```halcon
threshold(Image, Region, MinGray, MaxGray)
```

根据灰度范围进行二值化分割。目标和背景灰度有明显差异时的首选方法。

### `connection`（连通域分析）

```halcon
connection(Region, ConnectedRegions)
```

将相连的像素点分组为独立区域。threshold 后把多个目标拆成单个对象。

### `select_shape`（形状筛选）

```halcon
select_shape(Regions, SelectedRegions, 'area', 'and', 3000, 3300)
```

| 特征 | 说明 |
|------|------|
| `'area'` | 面积 |
| `'anisometry'` | 各向异性（长宽比） |
| `'width'` / `'height'` | 宽 / 高 |
| `'circularity'` | 圆度 |
| `'convexity'` | 凸度 |

---

## 20. 区域生长与分水岭分割

### `regiongrowing`

```halcon
regiongrowing(Image, Regions, 1, 1, 5, 200)
```

从种子点出发，合并灰度相似的邻域像素。不需要预设灰度阈值，适合复杂纹理、缺陷检测。

参数：RowDist, ColDist, MaxDist, MaxGrayDiff

### `regiongrowing_mean`

```halcon
regiongrowing_mean(Image, Regions, 5, 5, 5, 100)
```

带均值约束的区域生长，结果更均匀。

### `watersheds_threshold`

```halcon
watersheds_threshold(Image, Basins, 50)
```

分水岭算法，适合接触/粘连物体的分割（细胞、颗粒、焊点）。

### 辅助算子

| 算子 | 作用 |
|------|------|
| `shape_trans(Region, InnerCircle, "inner_center")` | 获取区域最大内切圆 |
| `area_center(Regions, Area, Row, Column)` | 计算区域面积和质心 |
| `inner_circle(Region, Row, Column, Radius)` | 返回内切圆 |

---

## 21. 形状特征提取

### 最小外接矩形

```halcon
* 平行外接矩形
smallest_rectangle1(Regions, Row1, Column1, Row2, Column2)
gen_rectangle1(Rects, Row1, Column1, Row2, Column2)

* 旋转外接矩形（最小面积）
smallest_rectangle2(Regions, Row, Column, Phi, Length1, Length2)
gen_rectangle2(Rects, Row, Column, Phi, Length1, Length2)
```

| 算子 | 特点 | 使用场景 |
|------|------|----------|
| `smallest_rectangle1` | 平行于坐标轴 | 粗略框选、显示用 |
| `smallest_rectangle2` | 可旋转、面积最小 | 精确描述目标方向 |

### `area_holes`

```halcon
area_holes(Regions, Area)
```

计算区域内部空洞的总面积，用于检测目标内部是否有空洞（如 PCB 焊盘空缺）。

---

## 22. 灰度特征提取

### `gray_features`

```halcon
gray_features(SelectedRegions, Image, 'min', MinDisp)
gray_features(SelectedRegions, Image, 'max', MaxDisp)
```

| 项目 | 说明 |
|------|------|
| 算子说明 | 计算区域内的灰度统计特征 |
| 支持特征 | `'min'`、`'max'`、`'mean'`、`'deviation'`、`'plane_deviation'` |
| 使用场景 | 评估区域亮度、区分亮暗不同的目标 |
| 联想法 | 形状差不多但有的亮有的暗？→ 用 gray_features 看灰度差异 |

### `area_center_gray`

```halcon
area_center_gray(SelectedRegions, Image, Area, Row, Column)
```

基于灰度值计算区域的"加权"面积和中心（灰度重心）。目标亮度不均匀时，比几何质心更准确。

### `select_gray`

```halcon
select_gray(SelectedRegions, Image, SelectedRegions1, 'mean', 'and', 100, 250)
```

基于灰度特征筛选区域（形状筛选的"灰度版"）。与 `select_shape` 互补。

---

## 23. 纹理分析

### `gen_cooc_matrix`

```halcon
gen_cooc_matrix(SelectedRegions, Image, Matrix, 6, 0)
```

生成灰度共生矩阵（GLCM），统计相邻像素的灰度对出现频率。参数：区域、图像、输出矩阵、灰度级数、方向（0° 水平 / 45° 对角 / 90° 垂直 / 135° 反对角）。

### `cooc_feature_image`

```halcon
cooc_feature_image(SelectedRegions, Image, 6, 0, Energy, Correlation, Homogeneity, Contrast)
```

从 GLCM 计算 4 个纹理特征：

| 特征 | 含义 |
|------|------|
| Energy（能量） | 纹理越均匀 → 能量越高 |
| Correlation（相关性） | 纹理有方向性 → 相关性强 |
| Homogeneity（同质性） | 局部纹理越一致 → 同质性越高 |
| Contrast（对比度） | 灰度差异越大 → 对比度越高 |

**联想法：** 目标亮度和形状都差不多，但表面粗糙度不同？→ GLCM 纹理分析。

---

## 24. 形态学操作

### `erosion_circle`

```halcon
erosion_circle(SelectedRegions, RegionErosion, 21)
```

用圆形结构元素对区域进行腐蚀操作，消除细小噪声连接，分离粘连目标。

### 形态学操作对照

| 算子 | 效果 | 场景 |
|------|------|------|
| `erosion_circle` | 收缩区域、消除细小突起 | 断开粘连、去毛刺 |
| `dilation_circle` | 膨胀区域、填充小孔 | 填补断裂、扩大区域 |
| `opening` | 先腐蚀后膨胀（开运算） | 移除小物体 + 平滑轮廓 |
| `closing` | 先膨胀后腐蚀（闭运算） | 填充小孔 + 桥接缝隙 |

### 区域逻辑运算

| 算子 | 作用 |
|------|------|
| `intersection` | 区域求交 |
| `difference` | 区域求差 |
| `union2` | 区域合并 |

---

## 25. 霍夫变换与直线检测

```halcon
sobel_dir(Img, Amp, Dir, "sum_abs", 3)       * ① 边缘检测（带方向）
threshold(Amp, R2, 59, 179)                   * ② 筛选边缘点
reduce_domain(Dir, R2, DirReduced)            * ③ 只保留边缘点的方向
hough_lines_dir(DirReduced, HImg, Lines, 2, 4, "mean", 5, 50, 5, 5, "true", Angle, Dist)
                                                * ④ 霍夫变换检测直线
gen_region_hline(R3, Angle, Dist)              * ⑤ 画直线验证
```

| 算子 | 作用 |
|------|------|
| `hough_lines_dir` | 利用方向信息更快更准地检测直线 |
| `gen_region_hline` | 将检测到的直线画出来验证 |

---

## 26. 骨架化与轮廓提取

```halcon
edges_image(Img, Amp, Dir, "canny", 1, "nms", 20, 40)
threshold(Amp, Region, 1, 255)
skeleton(Region, Skeleton)                    * 细化为单像素骨架
gen_contours_skeleton_xld(Skeleton, Contours, 1, "filter")  * 转亚像素轮廓
```

- **骨架化** → 提取区域的"中心线"，分析拓扑结构
- **转 XLD** → 支持亚像素精度和几何拟合（直线/圆拟合、曲率计算）

---

## 27. 频域处理

> 空间域搞不定的周期性噪声，频域轻松解决。

```halcon
fft_generic(Img, FFT, "to_freq", -1, "sqrt", "dc_center", "complex")    * ① 空间→频域
gen_lowpass(LP, 0.1, "none", "dc_center", w, h)                         * ② 生成低通滤波器
convol_fft(FFT, LP, Filtered)                                            * ③ 频域滤波
fft_generic(Filtered, Result, "from_freq", 1, "sqrt", "dc_center", "complex")  * ④ 频域→空间
```

**什么时候用频域？**
- 图像有周期性纹理噪声（如网格、条纹）
- 需要精确的频率截止（空间域难以做到）

---

## 28. 算子选择思维导图

```
输入图像
│
├─ 光照均匀 ────────────── threshold（简单高效）
│
├─ 光照不均 ────────────── dyn_threshold（动态补偿）
│
├─ 需要边缘检测 ──
│   ├─ 快速定位 ────────── sobel_amp / sobel_dir
│   ├─ 抗噪检测 ────────── laplace_of_gauss + zero_crossing
│   └─ 精确提取 ────────── edges_image（Canny）
│
├─ 需要尺寸测量 ──
│   ├─ 矩形 ────────────── gen_measure_rectangle2 + measure_pairs
│   └─ 圆弧 ────────────── gen_measure_arc + measure_pairs
│
├─ 需要找直线 ──────────── hough_lines / fit_line_contour_xld
│
├─ 需要形态学处理 ──
│   ├─ 去噪断连 ────────── opening / erosion_circle
│   ├─ 填补桥接 ────────── closing / dilation_circle
│   └─ 分离粘连 ────────── watersheds / erosion_circle
│
├─ 需要区域筛选 ──
│   ├─ 按形状 ──────────── select_shape（面积/长度/圆度）
│   └─ 按灰度 ──────────── select_gray（均值/方差）
│
└─ 需要特征提取 ──
    ├─ 灰度特征 ────────── gray_features / area_center_gray
    ├─ 纹理特征 ────────── gen_cooc_matrix + cooc_feature_image
    └─ 形状特征 ────────── smallest_rectangle1/2 / area_holes
```

---

> **文档维护** 本文档基于内部项目实战经验编写，将随项目推进持续更新。
