---
---

# 算法 DRI-Cover 实战攻略

> **版本** v4.0 (案例扩充版)  
> **来源** 内部项目经验总结  
> **适用范围** 涵盖深度学习算法与 HALCON 传统算法两大技术路线

---

## 总目录

- [**第一部分：深度学习算法**](#第一部分深度学习算法)
- [**第二部分：HALCON 传统算法**](#第二部分halcon传统算法)
- [**第三部分：综合案例实战**](#第三部分综合案例实战)

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

为规范工程组织、防止文件混杂，建议采用三级目录结构进行管理：

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

文件对应原则：每个模型 PY 文件与一个 DataYaml 一一对应，每个 DataYaml 映射 data 目录下的一个数据区块。

---

## 2. 训练脚本配置说明

### 2.1 关键参数一览

| 参数 | 用途 | 说明 |
|------|------|------|
| `project` | 结果保存目录 | 所有训练产物均保存至此路径 |
| `name` | 结果文件夹名称 | 建议附加时间戳后缀以区分不同训练批次 |
| `weights` | 模型架构/预训练权重 | 可传 .pt 文件或模型 yaml 路径；使用 `-p6` 后缀时 imgsz 需为 64 的倍数 |
| `data` | 数据集 YAML 路径 | 指向 DataYaml 文件 |
| `epochs` | 训练轮次 | 默认值为 300，实际取值应根据数据集规模动态调整 |
| `batch` | 批次大小 | 影响 Batch Normalization 统计特性、显存占用、训练速度及泛化能力；默认值为 16 或 32 |
| `imgsz` | 输入图片尺寸 | 影响检测精度与显存占用；对于非 -p6 模型，输入尺寸应为 32 的整数倍 |
| `device` | 推理设备 | 显卡编号，逗号分隔 |
| `workers` | 数据加载进程数 | 默认 8/16 |
| `resume` | 断点续训 | 自动读取 last.pt 继续训练 |

### 2.2 训练产物

| 产物 | 路径 | 说明 |
|------|------|------|
| 训练指标 | `[project]/results.csv` | 每个 epoch 的详细指标 |
| 模型权重 | `[project]/weights/best.pt` / `last.pt` | 通常情况下优先选用 best.pt 权重文件 |
| 训练配置 | `[project]/args.yaml` | 用于训练参数的完整溯源与审计 |
| BoxPR 曲线 | — | 反映目标检测框在测试集上的拟合程度与泛化性能 |
| MaskPR 曲线 | — | 反映实例分割掩码在测试集上的拟合程度与泛化性能 |

### 2.3 超参数调整

默认超参数配置详见 `ultralytics/cfg/default.yaml` 中。修改时只需在 `model.train()` 的参数列表中传入 `<超参数名=指定值>` 即可。

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

- 手动构建的缺陷类别列表（TXT 格式）
- 将各缺陷名称逐行排列
- 行号（从 0 开始）即为转换后的缺陷类别索引
- 该顺序必须与 DataYaml 中 names 字段的顺序严格一致

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


# 第二部分：HALCON传统算法

---

## 目录（第二部分）

1. [HALCON 基础语法](#1-halcon-基础语法)
2. [图像读取与 ROI 操作](#2-图像读取与-roi-操作)
3. [图像预处理与增强](#3-图像预处理与增强)
4. [边缘检测](#4-边缘检测)
5. [频域滤波](#5-频域滤波)
6. [图像分割](#6-图像分割)
7. [形状特征提取](#7-形状特征提取)
8. [灰度特征与纹理分析](#8-灰度特征与纹理分析)
9. [形态学操作](#9-形态学操作)
10. [灰度形态学](#10-灰度形态学)
11. [边界提取与孔洞填充](#11-边界提取与孔洞填充)
12. [模板匹配（NCC + 形状匹配）](#12-模板匹配ncc--形状匹配)
13. [霍夫直线检测](#13-霍夫直线检测)
14. [HALCON 导出 C++](#14-halcon-导出-c)
---

## 1. HALCON 基础语法

### 变量与赋值

HALCON 使用 `:=` 进行赋值，支持动态类型：

```halcon
a := 2
b := 1
c := a + b       // c = 3
c[2] := 3        // 数组索引赋值
```

> **应用场景**：HALCON 程序的基础构成单元，用于变量定义与中间结果存储。

### 条件语句

```halcon
if (a > 0)
    y := 2
elseif (a == 1)
    y := 3
else
    y := 4
endif
```

> **应用场景**：需根据运行时条件分支执行不同逻辑时使用，例如判定检测区域有效性、依据面积阈值选择处理分支。

### 循环语句

```halcon
// for 循环
for i := 0 to 9 by 1
    su := su + i
endfor

// while 循环
while (x < 10)
    x := x + 1
endwhile
```

> **应用场景**：图像列表遍历、检测结果区域迭代访问、批量图像处理等场景。

### 元组操作

```halcon
tuple2 := [0:100]          // 生成 0~100 的等差序列
tuple3 := [3:3:100]        // 从 3 到 100，步长为 3
tuple4 := [1, 2, 3]        // 手动构造元组
tuple4 := [tuple4, 4]      // 追加元素
tp := gen_tuple_const(10, 5)  // 生成 10 个 5 的常量元组
```

> **应用场景**：批量索引生成、参数列表构造、多结果组织与存储。

### Switch 语句

```halcon
switch(Index)
case 1:
    result := result + '1'
    break
case 2:
case 3:
    result := result + '23'
    break
default:
    result := result + '444'
endswitch
```

> **应用场景**：多分支选择逻辑，例如依据缺陷类型编码切换不同处理流程。

---

## 2. 图像读取与 ROI 操作

### 读取单张图像

```halcon
read_image(Image, 'group_photo.jpg')
```

> **应用场景**：加载待处理的图像文件，支持 JPEG、PNG、TIFF 等常见图像格式。

### 批量读取文件夹图像

```halcon
list_files('图片文件夹路径', ['files', 'follow_links'], ImageFiles)
tuple_regexp_select(ImageFiles, ['\\.(tif|tiff|gif|bmp|jpg|jpeg|jp2|png|pcx|pgm|ppm|pbm|xwd|ima|hobj)$', 'ignore_case'], ImageFiles)

for Index := 0 to |ImageFiles| - 1 by 1
    read_image(Image, ImageFiles[Index])
    * 处理每张图片
endfor
```

> **应用场景**：批量处理目录下所有图像，适用于大规模检测任务或批量预处理流程。

### ROI 手动框选

```halcon
draw_rectangle2(WindowHandle, Row, Col, Phi, width, height)
gen_rectangle2(Rectangle, Row, Col, Phi, width, height)
reduce_domain(Image, Rectangle, ImageReduced)
```

> **应用场景**：通过人机交互方式选取感兴趣区域（ROI），适用于模板截取、局部检测等需要人工参与的环节。

### ROI 矩形区域

```halcon
gen_rectangle1(Region, Row1, Col1, Row2, Col2)
reduce_domain(Image, Region, ImageReduced)
// 或
rectangle1_domain(Image, ImageReduced, Row1, Col1, Row2, Col2)
```

> **应用场景**：在已知坐标条件下直接生成矩形 ROI，适用于固定工位检测区域定义。

### ROI 圆形区域与联合

```halcon
gen_circle(ROI_0, 877.503, 1934.77, 246.08)
gen_circle(TMP_Region, 1240.32, 1895.79, 322.284)
union2(ROI_0, TMP_Region, ROI_0)     // 两个圆形区域合并
```

> **应用场景**：当检测区域由多个圆形子区域构成时，分别生成后执行合并操作。

### 十字标记

```halcon
gen_cross_contour_xld(Crosses, X, Y, 10, 0.78)
```

> **应用场景**：在图像上标记特定坐标点，用于检测结果可视化或参考点标注。

---

## 3. 图像预处理与增强

### RGB 转灰度

```halcon
rgb1_to_gray(Image, GrayImage)
```

> **策略依据**：HALCON 中绝大多数算子要求输入灰度图像，因此彩色图像必须先经灰度转换。此为图像预处理流程中的首要步骤。

### 图像取反

```halcon
invert_image(GrayImage, InvertImage)
```

> **应用场景**：当目标区域灰度低于背景灰度时，取反操作可改善后续分割效果。

### 图像增强

```halcon
emphasize(GrayImage, ImageEmphasize, Width, Height, 2)
```

> **应用场景**：增强图像局部对比度以突出细节信息，适用于光照不足或对比度偏低的图像。

> **策略依据**：当图像整体对比度偏低、细节表现不足时 -> 调用 `emphasize` 提升对比度。

### 灰度拉伸

```halcon
scale_image(GrayImage, ImageScaled, 2.5, -40)
```

> **参数说明**：Mult（乘数因子），Add（偏移量）-> 新像素 = 原像素 x Mult + Add

> **应用场景**：通过线性变换手动调整灰度分布范围，扩大目标区域与背景区域的灰度差异。

> **策略依据**：当目标灰度范围狭窄且背景灰度分布混杂时 -> 用 `scale_image` 拉开距离。

### 均值滤波（中值滤波）

```halcon
median_image(Image, ImageMedian, 'circle', 2, 'mirrored')
```

> **应用场景**：在去除噪声的同时保留边缘信息，较高斯滤波具备更优的边缘保持特性。

### 高斯滤波

```halcon
gauss_filter(Image, ImageGauss, 5)
```

> **应用场景**：图像平滑与去噪处理，常用于分割操作前的预处理阶段。

---

## 4. 边缘检测

### Sobel 边缘

```halcon
sobel_amp(Image, EdgeAmplitude, 'sum_abs', 3)
sobel_dir(ImageReduced, EdgeAmplitude, EdgeDirection, 'sum_abs', 3)
```

> **参数说明**：`'sum_abs'` 表示取水平和垂直方向的绝对值之和，`3` 为滤波器大小。

> **应用场景**：快速获取边缘强度响应图，适用于边缘特征显著的目标。`sobel_dir` 不仅得到幅度还得到方向，可用于后续霍夫变换。

> **策略依据**：当需要快速获取边缘响应时 -> `sobel_amp`；需要边缘方向信息 -> `sobel_dir`。

### Canny 边缘

```halcon
edges_image(Image, ImaAmp, ImaDir, 'canny', 1, 'nms', 20, 40)
```

> **参数说明**：`'canny'` 算法，`1` 是平滑尺度，`'nms'` 非极大值抑制，`20` 低阈值，`40` 高阈值。

> **应用场景**：高精度边缘检测，相较 Sobel 算子具备更细且更连续的边缘响应，适用于精确定位需求。配合 `skeleton` 可得到单像素骨架，配合 `gen_contours_skeleton_xld` 可得到亚像素轮廓。

```halcon
threshold(ImaAmp, Region, 1, 255)
skeleton(Region, Skeleton)
gen_contours_skeleton_xld(Skeleton, Contours, 1, 'filter')
```

> **策略依据**：当需求为精确且连续的边缘时 -> Canny；需要亚像素级边缘 -> `edges_sub_pix`。

### 亚像素边缘

```halcon
edges_sub_pix(GrayImage, Edges, 'canny', 2, 12, 22)
```

> **应用场景**：高精度尺寸测量场景，如几何量测、缺陷边界的亚像素级定位。

### Laplace 边缘 + 过零点检测

```halcon
laplace_of_gauss(GrayImage, ImageLaplace, 0.5)
zero_crossing(ImageLaplace, EdgeZeroCrossing)
```

> **应用场景**：检测图像灰度函数的过零点位置，边缘定位精度较高，但受噪声影响较为显著。

> **策略依据**：当需求为精准的过零点边缘定位时 -> Laplace of Gauss + Zero Crossing。

---

## 5. 频域滤波

```halcon
gen_lowpass(I1LP, 0.1, 'none', 'dc_center', Width, Height)
fft_generic(Image, ImageFFT, 'to_freq', -1, 'sqrt', 'dc_center', 'complex')
convol_fft(ImageFFT, I1LP, ImageConvol)
fft_generic(ImageConvol, ImageFFT1, 'from_freq', 1, 'sqrt', 'dc_center', 'complex')
```

> **流程说明**：时域 -> 频域（FFT）-> 频域滤波 -> 频域 -> 时域（逆 FFT）

> **应用场景**：滤除周期性噪声（如纹理背景干扰），保留图像主体结构轮廓。

> **策略依据**：当图像存在周期性纹理干扰或摩尔纹时 -> 想到频域滤波，构造滤波器在频域中抑制特定频率。

---

## 6. 图像分割

### 阈值分割

```halcon
threshold(GrayImage, Regions, MinGray, MaxGray)
```

> **应用场景**：当目标区域与背景存在显著灰度差异时，阈值分割是最为高效的图像分割方式。

> **策略依据**：当目标灰度显著高于或低于背景时 -> 先转灰度 -> `threshold` 设定灰度区间直接分割。

### 区域生长

```halcon
regiongrowing(Image, Regions, 1, 1, 5, 500)
```

> **参数说明**：第 1、2 个参数为行列邻域半径，第 3 个为灰度容差，第 4 个为最小区域面积。

> **应用场景**：当目标灰度分布不均匀但局部区域灰度连续时，区域生长算法能够有效分割出完整目标区域。

> **策略依据**：当阈值分割无法一次性获取完整目标区域时 -> 用 `regiongrowing` 基于局部相似性生长。

### 带种子点的区域生长

```halcon
regiongrowing_mean(Image, Regions, Row, Column, 25, 100)
```

> **应用场景**：在已知目标大致位置（种子点）的前提下，以此为起始点向外生长以获取完整区域。

### 连通域分析

```halcon
connection(Regions, ConnectedRegions)
```

> **应用场景**：将阈值分割后得到的多个分离区域拆分为独立区块，便于后续逐一分析与筛选。

> **策略依据**：分割后获取多个区域时 -> `connection` 把它们拆开 -> 逐个分析。

### 分水岭分割

```halcon
watersheds(Image, Basins, Watersheds)
watersheds_threshold(Image, Basins, 60)
```

> **应用场景**：分割相互接触或粘连的目标对象，广泛应用于细胞分割、颗粒计数等领域。

> **策略依据**：当多个目标粘连难以分离时 -> 用分水岭算法从灰度低谷处分割。

---

## 7. 形状特征提取

### 形状选择

```halcon
select_shape(ConnectedRegions, SelectedRegions, 'area', 'and', Min, Max)
```

> **常用特征**：`'area'` 面积、`'anisometry'` 各向异性（非等轴性）、`'circularity'` 圆度、`'compactness'` 紧凑度、`'convexity'` 凸度、`'rectangularity'` 矩形度。

```halcon
// 多条件筛选
select_shape(ConnectedRegions, SelectedRegions, ['area', 'anisometry'], 'and', [500, 1], [2000, 1.7])
```

> **应用场景**：根据预设的形状特征阈值筛选目标区域，例如保留面积在 500~2000 像素区间且各向异性适中的区域。

> **策略依据**：分割后得到大量候选区域时 -> 用 `select_shape` 筛选出真正关心的目标 -> 基于面积、长宽比、圆度等特征。

### 最小外接矩形

```halcon
smallest_rectangle1(Regions, Row1, Column1, Row2, Column2)
gen_rectangle1(Rectangle, Row1, Column1, Row2, Column2)

smallest_rectangle2(Regions, Row3, Column3, Phi, Length1, Length2)
gen_rectangle2(Rectangle1, Row3, Column3, Phi, Length1, Length2)
```

> **应用场景**：计算目标区域的最小外接矩形，`rectangle1` 输出轴对齐矩形，`rectangle2` 输出带旋转角度的最小包围盒。

### 内接圆

```halcon
inner_circle(Regions, Row, Column, Radius)
disp_circle(WindowHandle, Row, Column, Radius)
```

> **应用场景**：计算区域的最大内接圆，适用于圆形目标检测及内径测量。

### 孔洞面积

```halcon
area_holes(Regions, Area)
```

> **应用场景**：统计区域内部孔洞的总面积，用于缺陷检测中孔洞类缺陷的判定。

---

## 8. 灰度特征与纹理分析

### 灰度特征

```halcon
gray_features(SelectedRegions, Image, 'min', MinDisp)
gray_features(SelectedRegions, Image, 'max', MaxDisp)
area_center_gray(SelectedRegions, Image, Area, Row, Column)
select_gray(SelectedRegions, Image, SelectedRegions1, 'mean', 'and', 100, 250)
```

> **常用特征**：`'min'` 最小灰度、`'max'` 最大灰度、`'mean'` 平均灰度、`'deviation'` 灰度标准差。

> **应用场景**：基于灰度统计量进行区域筛选，例如保留平均灰度在 100~250 区间内的区域。

> **策略依据**：当形状特征相似但灰度特征不同时 -> 用 `gray_features` 提取灰度特征区分；需要按灰度筛选 -> `select_gray`。

### 纹理分析（灰度共生矩阵）

```halcon
gen_cooc_matrix(Region, Image, Matrix, 6, 0)
cooc_feature_image(Region, Image, 6, 0, Energy, Correlation, Homogeneity, Contrast)
```

> **输出特征说明**：
> - `Energy` - 能量（ASM）：纹理的均匀程度
> - `Correlation` - 相关性：灰度线性依赖关系
> - `Homogeneity` - 同质性：纹理的局部均匀性
> - `Contrast` - 对比度：灰度差异大小

> **应用场景**：区分不同纹理特征类型，适用于光滑表面与粗糙表面区分、纹理类缺陷检测等场景。

> **策略依据**：当目标与背景灰度接近但纹理存在差异时 -> 构建灰度共生矩阵 -> 提取纹理特征分类。

---

## 9. 形态学操作

### 腐蚀

```halcon
erosion_circle(Region, RegionErosion, Radius)
```

> **应用场景**：去除微小噪点区域、断开粘连区域、收缩目标区域边界。

> **策略依据**：当区域边缘存在不规则突起或毛刺时 -> 腐蚀；区域间有细连接 -> 腐蚀断开。

### 膨胀

```halcon
dilation_circle(Region, RegionDilation, Radius)
```

> **应用场景**：填充目标内部孔洞、连接断裂区域、外扩目标边界。

> **策略依据**：当区域内部存在孔洞时 -> 膨胀填充；目标断裂成多段 -> 膨胀连接。

### 开运算（先腐蚀后膨胀）

```halcon
opening_circle(Regions, RegionOpening, 5)
opening_rectangle1(Regions, RegionOpening1, 10, 10)
```

> **应用场景**：去除细小噪点、切断狭窄连接。`opening_rectangle1` 支持矩形结构元素，适用于特定方向上的去噪处理。

> **策略依据**：当区域周围存在离散噪点时 -> 开运算去除；区域间有细丝连接 -> 开运算断开。

### 闭运算（先膨胀后腐蚀）

```halcon
// 自定义结构元素
gen_ellipse(Ellipse, 100, 100, 0, 11, 13)
closing(Regions, Ellipse, RegionClosing)

// 或者直接使用圆形结构元素
closing_circle(Region, RegionClosing, Radius)
```

> **应用场景**：填充目标内部孔洞、闭合断裂轮廓线。

> **策略依据**：当目标内部存在孔洞或裂缝时 -> 闭运算填充；边缘断裂 -> 闭运算连接。

### 结构元素选择逻辑

| 结构元素形状 | 适用场景 | 算子 |
|------------|---------|------|
| 圆形 | 各向同性操作，通用 | `erosion_circle`, `dilation_circle`, `opening_circle`, `closing_circle` |
| 矩形 | 特定方向操作 | `opening_rectangle1`, `erosion_rectangle1` |
| 椭圆 | 各向异性 | `gen_ellipse` 创建后传入 `closing` / `opening` |

---

## 10. 灰度形态学

```halcon
gray_erosion_shape(GrayImage, ImageMin, 11, 11, 'octagon')
gray_dilation_shape(GrayImage, ImageMax, 11, 11, 'octagon')
gray_opening_shape(GrayImage, ImageOpening, 11, 11, 'octagon')
gray_closing_shape(GrayImage, ImageClosing, 11, 11, 'octagon')
```

> **参数说明**：`11, 11` 为结构元素大小，`'octagon'` 为八边形结构元素。

> **应用场景**：直接在灰度图像上执行形态学变换，适用于以下操作：
> - `gray_erosion`：去除亮区域中的暗细节
> - `gray_dilation`：去除暗区域中的亮细节
> - `gray_opening`：去除亮小点（白顶帽基础）
> - `gray_closing`：填充暗小孔（黑底帽基础）

> **策略依据**：当需要在形态学层面处理图像但避免二值化信息损失时 -> 直接在灰度图上做灰度形态学。

---

## 11. 边界提取与孔洞填充

### 边界提取

```halcon
boundary(Region, RegionBorder, 'inner')
```

> **参数说明**：`'inner'` 内边界，`'outer'` 外边界。

> **应用场景**：提取目标区域边界轮廓，用于周长计算与形状分析。

### 孔洞填充

```halcon
fill_up_shape(Regions, RegionFillUp, 'area', 0, 50000)
```

> **应用场景**：填充面积在指定阈值范围内的孔洞区域，常用于消除目标内部暗点干扰。

```halcon
// 综合示例：提取大目标的外边界
threshold(GrayImage, Regions, 0, 83)
connection(Regions, ConnectedRegions)
select_shape(ConnectedRegions, SelectedRegions, 'area', 'and', 2440000, 9999999)  // 选大目标
closing_circle(SelectedRegions, RegionClosing, 71)  // 闭运算填充内部空洞
boundary(RegionClosing, RegionBorder, 'inner')  // 提取内边界
```

---

## 12. 模板匹配（NCC + 形状匹配）

### NCC 灰度匹配（归一化积相关）

```halcon
* 创建模板
create_ncc_model(TemplateImage, 'auto', 0, 0, 'auto', 'use_polarity', ModelID)

* 执行匹配
find_ncc_model(SearchImage, ModelID, 0, 0, 0.5, 1, 0.5, 'true', 0, Row, Column, Angle, Score)

* 显示结果
gen_rectangle1(DetectionResult, Row-10, Column-10, Row+10, Column+10)

* 清理模型
clear_ncc_model(ModelID)
```

> **`find_ncc_model` 参数说明**：
> - 角度范围：`0` ~ `0`（不旋转搜索）
> - Score 阈值：`0.5`（匹配得分 >= 0.5 才认为匹配成功）
> - 最大匹配数：`1`（最多返回 1 个结果）
> - 金字塔层数：`0.5`
> - SubPixel 精度：`'true'`

> **应用场景**：适用于光照条件稳定的场景下的快速匹配，例如固定工位的产品定位任务。

> **策略依据**：在光照条件良好且目标纹理清晰的情况下 -> NCC 匹配又快又准。

### 交互式模板截取 + NCC 匹配（完整流程）

```halcon
* 读图转灰
read_image(Image, 'group_photo.jpg')
rgb1_to_gray(Image, GrayImage)

* 交互式框选模板
draw_rectangle2(WindowHandle, Row, Column, Phi, Length1, Length2)
gen_rectangle2(TemplateRect, Row, Column, Phi, Length1, Length2)
reduce_domain(GrayImage, TemplateRect, TemplateImage)

* 创建 NCC 模型
create_ncc_model(TemplateImage, 'auto', 0, 0, 'auto', 'use_polarity', ModelID)

* 匹配
find_ncc_model(GrayImage, ModelID, 0, 0, 0.5, 1, 0.5, 'true', 0, RowMatch, ColumnMatch, AngleMatch, Score)

* 绘制结果
dev_set_color('red')
dev_set_draw('margin')
for i := 0 to |Score| - 1 by 1
    gen_rectangle2(MatchRect, RowMatch[i], ColumnMatch[i], AngleMatch[i], Length1, Length2)
    dev_display(MatchRect)
    disp_message(WindowHandle, 'Score: ' + Score[i]$'.3f', 'window', RowMatch[i] - 40, ColumnMatch[i] - 40, 'red', 'false')
endfor
```

### 形状匹配（通用形状模型）

```halcon
* 创建模板区域
gen_rectangle1(ModelRegion, Row1, Col1, Row2, Col2)
reduce_domain(Image, ModelRegion, TemplateImage)

* 创建并训练形状模型
create_generic_shape_model(ModelID)
set_generic_shape_model_param(ModelID, 'metric', 'use_polarity')
train_generic_shape_model(TemplateImage, ModelID)

* 获取模型轮廓
get_shape_model_contours(ModelContours, ModelID, 1)
area_center(ModelRegion, ModelRegionArea, RefRow, RefColumn)
vector_angle_to_rigid(0, 0, 0, RefRow, RefColumn, 0, HomMat2D)
affine_trans_contour_xld(ModelContours, TransContours, HomMat2D)

* 执行匹配
find_generic_shape_model(TestImage, ModelID, MatchResultID, NumMatchResult)

* 获取匹配结果
for I := 0 to NumMatchResult - 1 by 1
    get_generic_shape_model_result_object(MatchContour, MatchResultID, I, 'contours')
    get_generic_shape_model_result(MatchResultID, I, 'row', Row)
    get_generic_shape_model_result(MatchResultID, I, 'column', Column)
    get_generic_shape_model_result(MatchResultID, I, 'angle', Angle)
    get_generic_shape_model_result(MatchResultID, I, 'score', Score)
    get_generic_shape_model_result(MatchResultID, I, 'scale_row', ScaleRow)
    get_generic_shape_model_result(MatchResultID, I, 'scale_column', ScaleColumn)
endfor
```

> **适用场景**：当目标具有明显形状特征且可能存在旋转或尺度变化时，形状匹配较 NCC 具有更强的鲁棒性。

> **策略依据**：当目标轮廓清晰且可能存在旋转或尺度变化时 -> 形状匹配；光照变化 -> 形状匹配也比 NCC 更稳定。

### 匹配方法选择对比

| 方法 | 优点 | 缺点 | 适用场景 |
|-----|------|------|---------|
| NCC（归一化积相关） | 速度快、实现简单 | 对光照变化敏感、不支持缩放 | 光照稳定的定位 |
| 形状匹配（Shape-Based） | 鲁棒性强、支持旋转/缩放 | 速度较慢、需要轮廓清晰 | 形状特征明显的目标 |

---

## 13. 霍夫直线检测

```halcon
* 先截取 ROI
rectangle1_domain(Image, ImageReduced, Row1, Col1, Row2, Col2)

* 提取边缘方向
sobel_dir(ImageReduced, EdgeAmplitude, EdgeDirection, 'sum_abs', 3)

* 从幅度图中提取兴趣区域
threshold(EdgeAmplitude, Regions, Min, Max)
reduce_domain(EdgeDirection, Regions, EdgeDirectionReduced)

* 霍夫直线检测（调整 threshold 控制直线数量）
hough_lines_dir(EdgeDirectionReduced, HoughImage, Lines, 2, 4, 'mean', 5, 50, 5, 5, 'true', Angle, Dist)

* 画线显示
gen_region_hline(Regions, Angle, Dist)
```

> **`hough_lines_dir` 参数说明**：
> - `2, 4`：角度分辨率相关
> - `'mean'`：角度计算方式
> - `5`：平滑尺度
> - `50`：阈值（控制检测到的直线数量，越大越少）
> - `5, 5`：最小线段长度/间隙

> **应用场景**：检测图像中的直线特征，适用于 PCB 板边缘检测、晶圆划痕定位、工件边缘提取等场景。

> **策略依据**：当任务涉及直线特征检测时 -> Sobel 提取边缘方向 -> Hough 变换检测直线。

---

## 14. HALCON 导出 C++

HALCON 代码可通过"导出"功能转为 C++ 代码，在 Visual Studio 中集成：

```halcon
* HALCON 端代码
read_image(Image, 'abcde.jpg')
get_image_size(Image, Width, Height)
dev_open_window(0, 0, Width, Height, 'black', WindowHandle)
dev_set_part(0, 0, Height-1, Width-1)
dev_display(Image)
```

### VS 配置要点

- **C/C++ -> 常规 -> 附加包含目录**：放 HALCON 的 include 路径
- **链接器 -> 常规 -> 附加库目录**：放 HALCON 的 lib 路径
- **链接器 -> 输入 -> 附加依赖项**：放 HALCON 的 .lib 文件
- **安装 MFC 工具**（如使用 MFC 界面）

> **应用场景**：将 HALCON 原型算法部署至上位机软件系统中，实现产线级自动化检测应用。

---

# 第三部分：综合案例实战

---

## 目录（第三部分）

15. [基于轮廓比较的大小边变形检测](#15-基于轮廓比较的大小边变形检测)
16. [K1 空料检测案例](#16-k1-空料检测案例)
17. [黑款物料检测案例](#17-黑款物料检测案例)
18. [脚仔变形检测案例（测量法）](#18-脚仔变形检测案例测量法)


## 15. 基于轮廓比较的大小边变形检测

### 15.1 项目背景与需求

在工业质检场景中，**大小边变形**是指产品边缘轮廓与标准轮廓之间存在局部或整体的偏移偏差，常见于冲压件、注塑件等制造工艺中。本案例通过比较产品**外轮廓**与**内轮廓**之间的距离分布，定量评估变形程度，并据此判定产品是否合格。

> **检测目标**：识别产品边缘是否存在局部凹陷/凸起（局部变形）或整体偏移（大小边缺陷）。

### 15.2 算法流程概览

```
输入图像
  |
  v
[预处理] RGB转灰度 -> 中值滤波
  |
  v
[外轮廓提取] 全局阈值分割(binary_threshold) -> 连通域分析 -> 形状筛选 -> 填充孔洞 -> 开运算
  |
  v
[内轮廓提取] 腐蚀外轮廓 -> 局部自适应阈值(var_threshold) -> 连通域分析 -> 闭运算 -> 填充孔洞 -> 开运算
  |
  v
[轮廓生成] gen_contour_region_xld (外轮廓 + 内轮廓)
  |
  v
[轮廓比较] distance_contours_xld (point_to_point) -> 提取距离属性
  |
  v
[变形评估] 计算距离的均值(Mean)与标准差(Deviation)
  |
  v
[判定逻辑] 均值超范围 -> 整体偏移；标准差超阈值 -> 局部变形
```

### 15.3 外轮廓提取

外轮廓提取的目标是获取产品的最外侧边界区域。

```halcon
* 灰度转换与中值滤波
rgb1_to_gray(Image, GrayImage)
median_image(GrayImage, ImageMedian, 'circle', 5, 'mirrored')

* 自动全局阈值分割 - 提取亮部区域
* 使用 smooth_histo 模式（平滑直方图）而非 Otsu，以适应更复杂的灰度分布
binary_threshold(ImageMedian, Region, 'smooth_histo', 'light', UsedThreshold)

* 连通域拆分
connection(Region, ConnectedRegions)

* 基于蓬松度(bulkiness)与面积筛选
* bulkiness = 面积 / 最接近椭圆的面积，值越大表示区域越不规则
select_shape(ConnectedRegions, SelectedRegions, ['bulkiness', 'area'], 'and', [0.5, 600000], [1.6, 2000000])

* 保留面积最大区域的 70%
select_shape_std(SelectedRegions, SelectedRegions3, 'max_area', 70)

* 孔洞填充 + 开运算去除毛刺
fill_up(SelectedRegions3, RegionFillUp)
opening_circle(RegionFillUp, RegionInner, 75)
```

> **算子组合逻辑**：
> - `binary_threshold('smooth_histo', 'light')`：自动计算全局阈值，提取亮色目标区域
> - `select_shape('bulkiness')`：**蓬松度**筛选可有效排除狭长或不规则的干扰区域
> - `select_shape_std('max_area', 70)`：保留最大区域及其 70% 的连通子区域，确保主区域完整
> - `fill_up + opening_circle`：填充内部孔洞后执行开运算，去除边缘微小突起

### 15.4 内轮廓提取

内轮廓提取是算法的核心——通过在外轮廓内部一定偏移距离处，用局部自适应阈值分割出内边界。

```halcon
* 将外轮廓向内腐蚀一定像素，确定内轮廓搜索区域
erosion_circle(RegionInner, RegionErosion, 5)

* 将搜索区域从原图中裁剪出来
reduce_domain(GrayImage, RegionErosion, ImageReduced)

* 中值滤波去噪
median_image(ImageReduced, ImageGauss, 'circle', 3, 'mirrored')

* 局部自适应阈值分割 - 提取暗部区域
* 在 5x5 邻域内计算均值与标准差，适用于光照不均匀场景
var_threshold(ImageGauss, Region3, 5, 5, 0.04, 2, 'dark')

* 连通域分析 + 面积筛选
connection(Region3, ConnectedRegions1)
select_shape(ConnectedRegions1, SelectedRegions1, 'area', 'and', 35, 99999)

* 合并、闭运算、填充孔洞、开运算
union1(SelectedRegions1, RegionUnion)
closing_circle(RegionUnion, RegionClosing, 500)
connection(RegionClosing, ConnectedRegions2)
fill_up(ConnectedRegions2, RegionFillUp)
select_shape(RegionFillUp, SelectedRegions3, 'area', 'and', 1000000, 9999999)
opening_circle(SelectedRegions3, RegionInner0, 355)
```

> **算子组合逻辑**：
> - `erosion_circle`：将外轮廓向内收缩，限定后续分析的搜索范围
> - `reduce_domain`：将图像域缩小到腐蚀后的区域内，减少计算量
> - `var_threshold(5, 5, 0.04, 2, 'dark')`：**局部自适应阈值**——在 5x5 窗内计算局部均值和标准差，提取比局部背景暗的区域
> - `closing_circle(500)`：大核闭运算连接断裂的内边缘，`500` 为较大半径，确保长距离断裂被桥接
> - **空区域检测**：如果 `fill_up` 后仍无有效区域，说明边缘断裂严重（边缘残缺），直接判 NG

### 15.5 轮廓生成与比较

```halcon
* 生成外轮廓的亚像素边缘
gen_contour_region_xld(RegionInner, ContoursInner, 'border')

* 生成内轮廓的亚像素边缘
gen_contour_region_xld(RegionInner0, ContoursInner0, 'border')

* 计算两个轮廓间的逐点距离（点到点模式）
distance_contours_xld(ContoursInner, ContoursInner0, ContourOut, 'point_to_point')

* 从结果轮廓中提取每个点的距离属性
get_contour_attrib_xld(ContourOut, 'distance', DisValue)
```

> **关键算子说明**：
> - `gen_contour_region_xld(, 'border')`：将区域边界转换为亚像素级 XLD 轮廓，精度高于像素级边界
> - `distance_contours_xld(, 'point_to_point')`：计算两条轮廓间对应点的欧氏距离，输出带有 'distance' 属性的新轮廓
> - `get_contour_attrib_xld('distance')`：提取每个轮廓点的距离值，得到一维距离数组

### 15.6 变形判定逻辑

```halcon
* 计算距离数组的标准差 —— 反映局部变形程度
tuple_deviation(DisValue, Deviation)

* 计算距离数组的算术平均值 —— 反映整体偏移程度
tuple_mean(DisValue, Mean)

* 判定规则
if (Mean < 15 or Mean > 30)
    * 整体偏移（大小边）—— 均值超出正常范围
    flagDis := 1
elseif (Deviation > 2.5)
    * 局部变形（凹凸）—— 标准差超过阈值
    flageDev := 1
endif
```

> **判定逻辑解读**：
> - **均值（Mean）**：内外轮廓间距离的平均值，反映**整体偏移量**。正常产品应在一个固定的工艺范围内（如 15~30 像素），超出此范围则为整体大小边缺陷
> - **标准差（Deviation）**：距离值的离散程度，反映**局部变形程度**。标准差小说明内外轮廓形态一致；标准差大说明存在局部凹陷或凸起

| 指标 | 物理含义 | 超出阈值代表 |
|------|---------|-------------|
| Mean（均值） | 轮廓整体间距 | 整体冲压偏移（大小边） |
| Deviation（标准差） | 轮廓间距波动 | 局部变形（凹陷/凸起） |

### 15.7 完整代码框架

```halcon
* 初始化
gen_empty_obj(EmptyObject)
gen_empty_region(EmptyRegion)

* 批量读取图像
list_files('图像文件夹路径', ['files', 'follow_links', 'recursive'], ImageFiles)
tuple_regexp_select(ImageFiles, ['\\.(tif|tiff|gif|bmp|jpg|jpeg|jp2|png|pcx|pgm|ppm|pbm|xwd|ima|hobj)$', 'ignore_case'], ImageFiles)

for Index := 0 to |ImageFiles| - 1 by 1
    * ---- 1. 读取与预处理 ----
    read_image(Image, ImageFiles[Index])
    rgb1_to_gray(Image, GrayImage)
    median_image(GrayImage, ImageMedian, 'circle', 5, 'mirrored')

    * ---- 2. 外轮廓提取 ----
    binary_threshold(ImageMedian, Region, 'smooth_histo', 'light', UsedThreshold)
    connection(Region, ConnectedRegions)
    select_shape(ConnectedRegions, SelectedRegions, ['bulkiness', 'area'], 'and', [0.5, 600000], [1.6, 2000000])
    select_shape_std(SelectedRegions, SelectedRegions3, 'max_area', 70)
    fill_up(SelectedRegions3, RegionFillUp)
    opening_circle(RegionFillUp, RegionInner, 75)

    * 空区域跳过
    if (EmptyRegion == RegionInner or EmptyObject == RegionInner)
        continue
    endif

    * ---- 3. 内轮廓提取 ----
    erosion_circle(RegionInner, RegionErosion, 5)
    reduce_domain(GrayImage, RegionErosion, ImageReduced)
    median_image(ImageReduced, ImageGauss, 'circle', 3, 'mirrored')
    var_threshold(ImageGauss, Region3, 5, 5, 0.04, 2, 'dark')
    connection(Region3, ConnectedRegions1)
    select_shape(ConnectedRegions1, SelectedRegions1, 'area', 'and', 35, 99999)
    union1(SelectedRegions1, RegionUnion)
    closing_circle(RegionUnion, RegionClosing, 500)
    connection(RegionClosing, ConnectedRegions2)
    fill_up(ConnectedRegions2, RegionFillUp)
    select_shape(RegionFillUp, SelectedRegions3, 'area', 'and', 1000000, 9999999)
    opening_circle(SelectedRegions3, RegionInner0, 355)

    * 边缘残缺跳过（无内轮廓区域）
    if (SelectedRegions3 == EmptyObject or SelectedRegions3 == EmptyRegion)
        * 记录 NG 并跳过
        continue
    endif

    * ---- 4. 轮廓生成与比较 ----
    gen_contour_region_xld(RegionInner0, ContoursInner0, 'border')
    gen_contour_region_xld(RegionInner, ContoursInner, 'border')
    distance_contours_xld(ContoursInner, ContoursInner0, ContourOut, 'point_to_point')
    get_contour_attrib_xld(ContourOut, 'distance', DisValue)

    * ---- 5. 变形判定 ----
    tuple_deviation(DisValue, Deviation)
    tuple_mean(DisValue, Mean)

    flagDis := 0
    flageDev := 0
    if (Mean < 15 or Mean > 30)
        flagDis := 1            * 整体偏移
    elseif (Deviation > 2.5)
        flageDev := 1           * 局部变形
    endif

    * ---- 6. 结果输出 ----
    if (flagDis or flageDev)
        * NG：输出带偏差数值的图片
        write_image(GrayImage, 'jpeg', 0, 'ng/' + StrIndex + '_' + StrDev + '_' + StrMean + '.jpeg')
    else
        * OK
        write_image(GrayImage, 'jpeg', 0, 'ok/' + StrIndex + '.jpeg')
    endif
endfor
```

### 15.8 涉及的算子汇总

| 类别 | 算子 | 在本案例中的作用 |
|------|------|----------------|
| 预处理 | `rgb1_to_gray`, `median_image` | 灰度转换与中值滤波去噪 |
| 全局阈值 | `binary_threshold('smooth_histo')` | 自动阈值分割提取亮部区域 |
| 局部阈值 | `var_threshold` | 自适应分割提取暗部内轮廓区域 |
| 区域分析 | `connection`, `select_shape`, `select_shape_std` | 连通域拆分与多条件形状筛选 |
| 形态学 | `erosion_circle`, `opening_circle`, `closing_circle` | 区域收缩、去噪、桥接断裂 |
| 区域填充 | `fill_up`, `union1` | 孔洞填充与区域合并 |
| 域操作 | `reduce_domain` | 限定处理区域，提高效率 |
| 轮廓生成 | `gen_contour_region_xld` | 区域边界转换为亚像素轮廓 |
| 轮廓比较 | `distance_contours_xld` | 计算两轮廓间的逐点距离 |
| 属性提取 | `get_contour_attrib_xld` | 提取轮廓距离属性 |
| 统计量 | `tuple_mean`, `tuple_deviation` | 计算距离数组的均值与标准差 |
| 判决逻辑 | `if/elseif/endif`, `continue` | 基于统计量的分级判定与流程控制 |
| 文件操作 | `list_files`, `tuple_regexp_select`, `write_image` | 批量图像读取与结果保存 |

### 15.9 案例要点总结

1. **双轮廓比较法**：通过比较同一产品的内、外轮廓来评估变形，不需要参考模板或标准图像，鲁棒性高
2. **局部阈值 vs 全局阈值**：外轮廓用全局阈值（`binary_threshold`），内轮廓用局部阈值（`var_threshold`），因为内轮廓区域存在光照不均匀
3. **均值与标准差联合判定**：均值反映整体偏移（大小边），标准差反映局部变形（凹凸），两者互补
4. **腐蚀偏移量设计**：`erosion_circle(5)` 决定了内轮廓的搜索起始位置，该参数需根据产品工艺尺寸确定
5. **空区域兜底**：`fill_up` 后仍无有效区域说明边缘断裂严重，直接判为边缘残缺缺陷
6. **形态学参数的意义**：`opening_circle(75)` 去除外轮廓毛刺，`closing_circle(500)` 桥接内轮廓长断裂，参数大小由缺陷尺度决定

---
---

> **总结**：HALCON 传统算法的核心技术路线可概括为 **"预处理 -> 分割 -> 特征提取 -> 判定"** 四阶段流程。
> 处理流程决策：首先评估是否需要灰度转换与图像增强；然后选择合适的分割策略（阈值分割、区域生长、分水岭算法）；最后依据分割结果决定后续形态学处理与特征筛选方案。
> 具体而言，需进一步确认是否引入形态学处理、选取何种特征进行筛选，以及最终判定方式（形状特征、灰度特征或模板匹配）。



---

## 16. K1 空料检测案例

---

### 16.1 项目背景与需求

K1 空料检测用于判断产品是否放置在检测工位上。核心需求是快速、可靠地判断有无物料，防止空料导致误报警或设备空跑。

**检测目标**：区分"有料"与"空料"两种状态。

---

### 16.2 算法流程概览

```
输入图像 → RGB转灰度 → 阈值分割(0-213) → 连通域分析 → 计算最大面积 → 面积>100000? → OK/NG
```

整体流程非常简洁，核心思想是：有料时图像中会出现大面积的低灰度区域，通过面积阈值即可区分。

---

### 16.3 代码实现

```hdevelop
* 读取图像
list_files ('D:/.../K1', ['files','follow_links'], ImageFiles)
tuple_regexp_select (ImageFiles, ['\\.(tif|tiff|gif|bmp|jpg|jpeg|jp2|png|pcx|pgm|ppm|pbm|xwd|ima|hobj)$','ignore_case'], ImageFiles)

for Index := 0 to |ImageFiles| - 1 by 1
    read_image (Image, ImageFiles[Index])

    * 灰度转换
    rgb1_to_gray (Image, GrayImage)

    * 全局阈值分割（0-213）：提取深色区域
    threshold (GrayImage, Regions, 0, 213)

    * 连通域分析
    connection (Regions, ConnectedRegions)

    * 计算所有连通域面积
    area_center (ConnectedRegions, Area, Row, Column)

    * 取最大面积
    tuple_max (Area, Max)

    * 面积判定：>100000 判为有料（OK），否则空料（NG）
    dev_display (Image)
    if (Max > 100000)
        disp_text (WindowHandle, 'ok', 'window', 12, 12, 'black', [], [])
    else
        disp_text (WindowHandle, 'ng', 'window', 12, 12, 'black', [], [])
    endif

    stop()
endfor
```

---

### 16.4 涉及的算子汇总

| 类别 | 算子 | 在本案例中的作用 |
|------|------|----------------|
| 预处理 | `rgb1_to_gray` | 彩色图像转灰度，简化处理 |
| 全局阈值 | `threshold(0, 213)` | 提取深色物料区域（有料时大面积深色） |
| 区域分析 | `connection`, `area_center`, `tuple_max` | 拆分连通域并计算最大面积 |
| 显示 | `dev_display`, `disp_text` | 显示图像和检测结果 |

---

### 16.5 案例要点总结

1. **极简流程**：本案例是目前最简洁的空料检测方案，仅用 6 个核心算子即可完成
2. **阈值选择**：`threshold(0, 213)` 的阈值需根据实际打光情况微调，建议在产线上用多张样本统计灰度分布
3. **面积阈值**：`100000` 是经验值，取决于图像分辨率与物料在画面中的占比，可根据实际测试调整
4. **局限性**：该方案假设有料时画面中大部分区域被物料覆盖；若物料尺寸较小或背景复杂，需增加 ROI 限定或改用其他方案
5. **部署建议**：空料检测通常作为前级安全校验，要求极高的可靠性，建议加上连续多帧确认逻辑，避免单帧误判

---

## 17. 黑款物料检测案例

---

### 17.1 项目背景与需求

黑款物料检测用于识别黑色橡胶/塑料类物料区域。黑色物料在图像中通常表现为特定灰度范围内的区域，但由于材质反光特性不同，区域可能呈现破碎不连续的特点。

**检测目标**：提取黑色物料区域，计算其面积/占比以判定物料是否存在、位置是否正确。

---

### 17.2 算法流程概览

```
输入图像 → RGB转灰度 → 阈值分割(90-103) → 闭运算(closing_circle 5) → 连通域分析 → 计算最大面积
```

核心思路：利用黑色物料在特定灰度范围内的特性进行分割，通过闭运算修复因反光导致的区域断裂。

---

### 17.3 代码实现

```hdevelop
* 读取图像
list_files ('D:/.../黑款物料', ['files','follow_links'], ImageFiles)
tuple_regexp_select (ImageFiles, ['\\.(tif|tiff|gif|bmp|jpg|jpeg|jp2|png|pcx|pgm|ppm|pbm|xwd|ima|hobj)$','ignore_case'], ImageFiles)

for Index := 0 to |ImageFiles| - 1 by 1
    read_image (Image, ImageFiles[Index])

    * 灰度转换
    rgb1_to_gray (Image, GrayImage)

    * 阈值分割：提取灰度值 90-103 的黑色物料区域
    threshold (GrayImage, Regions, 90, 103)

    * 闭运算（半径5）：填充物料表面的微小断裂
    closing_circle (Regions, RegionClosing, 5)

    * 连通域分析
    connection (RegionClosing, ConnectedRegions)

    * 计算各区域面积
    area_center (ConnectedRegions, Area, Row, Column)

    * 取最大面积（用于后续判定）
    tuple_max (Area, Max)

    stop()
endfor
```

---

### 17.4 涉及的算子汇总

| 类别 | 算子 | 在本案例中的作用 |
|------|------|----------------|
| 预处理 | `rgb1_to_gray` | 彩色转灰度，降低数据维度 |
| 全局阈值 | `threshold(90, 103)` | 提取特定灰度范围内的黑色物料区域 |
| 形态学 | `closing_circle(5)` | 闭运算填充物料表面反光导致的细小断裂 |
| 区域分析 | `connection`, `area_center`, `tuple_max` | 拆分连通域并计算最大区域面积 |

---

### 17.5 案例要点总结

1. **阈值针对性**：黑色物料在灰度图像中灰度值偏低（90-103），该范围需根据实际打光条件标定，不同光照下灰度分布会有偏移
2. **闭运算的关键作用**：`closing_circle(5)` 是本案例最关键的步骤——黑色物料表面常因反光出现高光点，导致分割后区域破碎，闭运算通过先膨胀后腐蚀桥接断裂区域
3. **结构元素大小**：`closing_circle(5)` 的半径 5 是针对细小断裂的经验值，若断裂较宽需增大半径，但过大会合并不应连接的相邻区域
4. **拓展应用**：可将此方案泛化用于黑色胶圈检测、黑色密封条定位、黑色塑料件缺陷检测等场景
5. **改进方向**：若光照不均匀导致同一物料上灰度值有较大差异，可考虑使用局部阈值（`var_threshold`）替代全局阈值

---

## 18. 脚仔变形检测案例（测量法）

---

### 18.1 项目背景与需求

脚仔（Leg）是产品上的支撑结构，变形会影响装配精度。本案例采用基于角度测量的方法替代传统骨架方向筛选，通过计算"本体底线"与"脚仔长边"之间的夹角来量化变形程度。

**检测目标**：检测脚仔是否变形，以本体底线与脚仔之间的夹角作为量化指标。

---

### 18.2 算法流程概览

```
输入图像 → 中值滤波 → 阈值分割(0-31) → 填充 → 闭运算 → 开运算分离本体
    ├─ 本体部分: 最小外接矩形 → 取底部最宽两点 → 生成底线
    └─ 脚仔部分: 连通域 → 形状筛选 → 最小外接矩形 → 取长边
                         ↓
              计算底线与脚仔长边的夹角 → 取锐角 → 判定
```

核心创新：从"找脚仔角度"转变为"算本体与脚仔的夹角"，通过几何测量量化变形。

---

### 18.3 代码实现

```hdevelop
gen_empty_obj (EmptyObject)
gen_empty_region (EmptyRegion)

* 读取图像
list_files ('D:/.../脚仔变形-1', ['files','follow_links'], ImageFiles)
tuple_regexp_select (ImageFiles, ['\\.(tif|tiff|gif|bmp|jpg|jpeg|jp2|png|pcx|pgm|ppm|pbm|xwd|ima|hobj)$','ignore_case'], ImageFiles)

for Index := 0 to |ImageFiles| - 1 by 1
    read_image (Image1, ImageFiles[Index])

    * ---- 1. 预处理 ----
    median_image (Image1, Image, 'circle', 1, 'mirrored')
    threshold (Image, Regions, 0, 31)
    fill_up (Regions, RegionFillUp)
    closing_circle (RegionFillUp, RegionClosing, 20)

    * ---- 2. 分离本体 ----
    opening_rectangle1 (RegionClosing, RegionOpening, 45, 45)
    select_shape (RegionOpening, RegionOpening, 'area', 'and', 100000, 99999999)

    * 空料判断
    if (RegionOpening == EmptyObject or RegionOpening == EmptyRegion)
        * 没有提取到本体，可能是空料
        stop()
        continue
    endif

    * 提取脚仔区域（总体 - 本体 = 脚仔）
    difference (RegionClosing, RegionOpening, RegionDifference)

    * ========== 处理本体部分 ==========
    * 获取最小外接矩形
    smallest_rectangle2 (RegionOpening, Row, Column, Phi, Length1, Length2)
    * 生成矩形轮廓并提取角点
    gen_rectangle2_contour_xld (Rect, Row, Column, Phi, Length1, Length2)
    get_contour_xld (Rect, Rows0, Cols0)
    * 按行坐标排序，取底部两个点（行坐标最大）
    tuple_sort_index (Rows0, Indices)
    BottomIdx := [Indices[|Indices| - 1], Indices[|Indices| - 2]]
    * 生成本体底线
    gen_contour_polygon_xld (BottomLine, [Rows0[BottomIdx[0]], Rows0[BottomIdx[1]]], [Cols0[BottomIdx[0]], Cols0[BottomIdx[1]]])

    * ========== 处理脚仔部分 ==========
    * 开运算去噪
    opening_rectangle1 (RegionDifference, RegionOpeningJ, 4, 4)
    connection (RegionOpeningJ, ConnectedRegions)
    * 筛选面积大于 1500 的区域
    select_shape (ConnectedRegions, SelectedRegions, 'area', 'and', 1500, 99999)

    * 未提取到脚仔则跳过
    if (SelectedRegions == EmptyObject or SelectedRegions == EmptyRegion)
        stop()
        continue
    endif

    * 获取脚仔的最小外接矩形
    smallest_rectangle2 (SelectedRegions, Row, Column, Phi, Length1, Length2)
    * 生成矩形轮廓并提取四个角点
    gen_rectangle2_contour_xld (Rect, Row, Column, Phi, Length1, Length2)
    get_contour_xld (Rect, Rows, Cols)
    FourRows := Rows[0:3]
    FourCols := Cols[0:3]

    * 计算四条边长，找到长边
    Edges := []
    for i := 0 to 3 by 1
        j := (i + 1) % 4
        dr := FourRows[i] - FourRows[j]
        dc := FourCols[i] - FourCols[j]
        distance := sqrt(dr*dr + dc*dc)
        Edges := [Edges, distance]
    endfor
    tuple_sort_index (Edges, Indices)
    LongEdgeIndex := Indices[2]  * 取第一条长边
    StartIdx := LongEdgeIndex
    EndIdx := (StartIdx + 1) % 4
    * 用长边端点生成方向线
    gen_contour_polygon_xld (DirectionLine, [FourRows[StartIdx], FourRows[EndIdx]], [FourCols[StartIdx], FourCols[EndIdx]])

    * ========== 计算夹角 ==========
    angle_ll (Rows0[BottomIdx[0]], Cols0[BottomIdx[0]], Rows0[BottomIdx[1]], Cols0[BottomIdx[1]], FourRows[StartIdx], FourCols[StartIdx], FourRows[EndIdx], FourCols[EndIdx], AngleRad)

    * 转为角度并取锐角
    AngleDeg := deg(abs(AngleRad))
    if (AngleDeg > 90)
        AngleDeg := 180 - AngleDeg
    endif

    stop()
endfor
```

---

### 18.4 涉及的算子汇总

| 类别 | 算子 | 在本案例中的作用 |
|------|------|----------------|
| 预处理 | `median_image` | 中值滤波去噪，保留边缘信息 |
| 全局阈值 | `threshold(0, 31)` | 提取深色区域（本体+脚仔） |
| 区域填充 | `fill_up` | 填充内部孔洞，获得完整区域 |
| 形态学 | `closing_circle(20)`, `opening_rectangle1` | 闭运算桥接断裂，开运算分离本体与脚仔 |
| 区域运算 | `difference` | 总体区域减本体区域 = 脚仔区域 |
| 形状筛选 | `select_shape('area')` | 按面积筛选本体和脚仔 |
| 几何分析 | `smallest_rectangle2` | 获取区域的最小外接矩形（带方向角） |
| 轮廓生成 | `gen_rectangle2_contour_xld`, `gen_contour_polygon_xld` | 生成矩形轮廓和直线轮廓 |
| 轮廓点提取 | `get_contour_xld` | 提取轮廓上的所有点坐标 |
| 元组操作 | `tuple_sort_index` | 排序找到底部点和长边 |
| 角度计算 | `angle_ll` | 计算两直线之间的夹角 |
| 角度转换 | `deg` | 弧度转角度 |
| 几何逻辑 | `if (AngleDeg > 90)` | 取锐角（补齐到 180 减去钝角） |
| 区域运算 | `connection` | 连通域拆分脚仔 |
| 循环 | `for` 循环遍历 | 计算四边形的四条边长 |

---

### 18.5 案例要点总结

1. **测量法替代骨架法**：与原始的脚仔.hdev（使用骨架 + 方向筛选）不同，本案例采用**几何测量法**，通过计算本体底线与脚仔长边的夹角来量化变形，结果更直观、可解释性更强

2. **本体分离策略**：使用 `opening_rectangle1(45, 45)` 将本体从更大的区域中分离出来，矩形核的大小取决于本体与脚仔之间的宽度差，需根据实际产品尺寸调整

3. **底线选取逻辑**：通过 `smallest_rectangle2` 获取最小外接矩形后，提取四个角点，按行坐标排序取最大的两个点作为底部两点。这假设了产品在图像中大致水平放置

4. **脚仔方向提取**：通过最小外接矩形的四条边计算长度，取最长边作为脚仔的方向线。这种方法的前提是脚仔近似矩形，且长边方向代表脚仔的延伸方向

5. **锐角处理**：`angle_ll` 计算的是有向角，可能为钝角，通过 `if (AngleDeg > 90) AngleDeg := 180 - AngleDeg` 补齐到锐角，使结果始终在 0-90 度范围内

6. **空料与严重变形兜底**：两处兜底检查（本体空料跳过和脚仔未检出跳过）确保算法在异常情况下不会崩溃

7. **部署优化**：代码注释中有提示"在部署的时候要把画线的部分注释掉"，说明显示操作用于调试，正式部署时应移除或条件编译

---

