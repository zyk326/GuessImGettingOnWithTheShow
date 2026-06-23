---
---

# 算法 DRI-Cover 实战攻略

> **版本** v5.0 (VisionMaster 专题扩充版)  
> **来源** 内部项目经验总结  
> **适用范围** 涵盖深度学习算法、HALCON 传统算法及 VisionMaster 视觉平台三大技术路线

---

## 总目录

- [**第一部分：深度学习算法**](#第一部分深度学习算法)
- [**第二部分：HALCON 传统算法**](#第二部分halcon传统算法)
- [**第三部分：综合案例实战**](#第三部分综合案例实战)
- [**第四部分：VisionMaster 专题**](#第四部分visionmaster-专题)

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

### 13.4 机加工件

| 表面类型 | 检测难度 | 原因 |
|---------|---------|------|
| **毛坯面** | 困难 | 点位多、检测速度慢；大量正常表面纹理与缺陷特征相似，误检率高 |
| **加工面** | 容易 | 表面一致性高，缺陷与正常区域的对比度明显，检出率高 |

**实践建议**：

- 毛坯面的缺陷检测优先考虑**传统图像处理**（差分法、灰度比对），深度学习在此类表面容易过杀
- 加工面则适合**深度学习**方案（YOLO / 分类网络），一致性好的背景能充分发挥模型的特征提取能力
- 若毛坯面必须使用深度学习，建议增加**数据增强**（光照变化、旋转、仿射变换）提升泛化能力，同时适当降低置信度阈值并配合二次筛选



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
19. [孔洞检测案例（HALCON）](#19-孔洞检测案例halcon)


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
## 19. 孔洞检测案例（HALCON）

### 19.1 项目背景与需求

USB 接口的毛边/异物检测，需要在孔洞区域内检出残留毛边或异物，并输出其位置、面积和外接矩形参数。本案例使用 HALCON 实现，包含主程序（.hdev）和可复用外部函数（.hdvp）。

**检测目标**：检测孔洞内是否残留毛边/异物，输出异物面积和包裹矩形参数。

---

### 19.2 算法流程概览

```
读取图像 → 灰度转换 → 中值滤波 → 阈值分割(48-255) → 取反 → 连通域分析
    → 按面积筛选(70000-85000) → 闭运算 → 腐蚀 → 凸包转换 → 裁剪
    → 非线性灰度放大(pow_image,2) → 阈值(1000-999999) → 连通域
    → 合并 → 计算面积与中心 → 最小外接矩形 → 输出结果
```

核心思路：先定位孔洞区域（粗定位），再在孔洞内部通过非线性增强放大微弱异物信号，最后分割提取。

---

### 19.3 代码实现

主程序 `D7.hdev` 遍历图像文件夹，调用外部函数执行检测：

```hdevelop
* 引用外部函数
import 'D:/项目/孔洞检测/Usb_Process.hdvp'

* 遍历图像
list_files ('.../USB毛边D7', ['files','follow_links'], ImageFiles)
tuple_regexp_select (ImageFiles, ['\\.(tif|tiff|gif|bmp|jpg|jpeg|jp2|png|pcx|pgm|ppm|pbm|xwd|ima|hobj)$','ignore_case'], ImageFiles)

for Index := 0 to |ImageFiles| - 1 by 1
    read_image (Image, ImageFiles[Index])

    * ===== 孔洞定位 =====
    rgb1_to_gray (Image, GrayImage)
    median_image (GrayImage, ImageMedian, 'circle', 3, 'mirrored')
    threshold (ImageMedian, Regions, 48, 255)
    complement (Regions, RegionComplement)         * 取反得到暗区（孔洞）
    connection (RegionComplement, ConnectedRegions)
    select_shape (ConnectedRegions, SelectedRegions, 'area', 'and', 70000, 85000)
    closing_circle (SelectedRegions, RegionClosing, 3.5)
    erosion_circle (RegionClosing, RegionErosion, 3)
    shape_trans (RegionErosion, RegionErosion1, 'convex')
    reduce_domain (GrayImage, RegionErosion1, ImageReduced)

    * ===== 异物检测 =====
    pow_image (ImageReduced, PowImage, 2)           * 非线性增强
    threshold (PowImage, RegionHigh, 1000, 999999)  * 提取高亮异物
    connection (RegionHigh, ConnectedRegions1)
    union1 (ConnectedRegions1, RegionUnion)
    area_center (RegionUnion, Area, Row, Column)
    smallest_rectangle2 (RegionUnion, Row1, Column1, Phi, Length1, Length2)
    gen_rectangle2 (Rectangle, Row1, Column1, Phi, Length1, Length2)

    stop()
endfor
```

外部函数 `Usb_Process.hdvp` 封装了上述完整的孔洞检测逻辑，并加入了异常处理：

```hdevelop
try
    * ... 检测逻辑同上 ...
catch (Exception)
    Area := -1   * 异常时返回 -1 标识
endtry
return ()
```

---

### 19.4 涉及的算子汇总

| 类别 | 算子 | 在本案例中的作用 |
|------|------|----------------|
| 引用 | `import` | 引用外部函数文件（.hdvp） |
| 预处理 | `rgb1_to_gray` | 彩色图像转灰度 |
| 滤波 | `median_image('circle', 3)` | 中值去噪，保留边缘 |
| 全局阈值 | `threshold(48, 255)` | 提取亮区域（背景），后取反得孔洞 |
| 区域筛选 | `select_shape('area', 70000-85000)` | 按面积过滤孔洞区域 |
| 形态学 | `closing_circle(3.5)`, `erosion_circle(3)` | 闭运算填充断裂，腐蚀去毛刺 |
| 凸包 | `shape_trans('convex')` | 将区域转为凸包，得到完整孔洞 |
| 灰度增强 | `pow_image(2)` | 非线性放大，使微弱异物信号显著 |
| 二次阈值 | `threshold(1000, 999999)` | 提取放大后的高亮异物区域 |
| 区域分析 | `union1`, `area_center`, `smallest_rectangle2` | 合并异物、计算面积、输出外接矩形 |
| 异常处理 | `try` / `catch` | 检测异常时返回 Area=-1，避免崩溃 |

---

### 19.5 关键参数调优

| 参数 | 当前值 | 调优方向 |
|------|--------|---------|
| `threshold` 范围 | 48~255 | 根据打光效果调整，确保亮区与暗区分明 |
| `select_shape('area')` | 70000~85000 | 根据孔洞实际面积调整 |
| `pow_image` 指数 | 2 | 指数越高增强越明显，但噪声也会放大 |
| 二次 `threshold` | 1000~999999 | 放大后背景值通常 < 500，目标 > 1000 |

---




# 第四部分：VisionMaster 专题

---

## 目录（第四部分）

1. [九点标定与坐标系对应关系](#1-九点标定与坐标系对应关系)
2. [VisionMaster 标定文件体系](#2-visionmaster-标定文件体系)
3. [MVS 与 VisionMaster 的关系与分工](#3-mvs-与-visionmaster-的关系与分工)
4. [卡尺工具与边缘检测](#4-卡尺工具与边缘检测)
5. [快速匹配（Fast Matching）](#5-快速匹配fast-matching)
6. [位置修正（Position Correction）](#6-位置修正position-correction)
7. [距离测量（点与点的距离 / 点与线的距离）](#7-距离测量点与点的距离--点与线的距离)
8. [条件分支（Condition Branch）](#8-条件分支condition-branch)
9. [格式化（Formatting）](#9-格式化formatting)
10. [输出保存图像（Output Save Image）](#10-输出保存图像output-save-image)
11. [变量计算（Variable Calculation）](#11-变量计算variable-calculation)
12. [协议解析（Protocol Parsing）](#12-协议解析protocol-parsing)
13. [文本保存（Text Save）](#13-文本保存text-save)
14. [组合模块（Combination Module）](#14-组合模块combination-module)
15. [通讯与标定流程（TCP + 全局触发）](#15-通讯与标定流程tcp--全局触发)
16. [自动化生产流程案例](#16-自动化生产流程案例)

---
## 1. 九点标定与坐标系对应关系
### 1.1 核心理解

九点标定（手眼标定中的"九点法"）的核心原则是**像素坐标与机器人坐标必须严格对应物理上的同一点**。

| 坐标系 | 来源 | 含义 |
|--------|------|------|
| **像素坐标 (u, v)** | 相机图像中通过找轮廓确定的物料中心点 | 图像上的位置 |
| **机器人坐标 (X, Y)** | 机械手实际运动到该物料中心时记录的值 | 物理空间的位置 |

### 1.2 变换矩阵原理

九点标定的本质是通过求解仿射变换矩阵 M，建立像素与物理坐标的映射关系：

```
[ X ]   [ a  b  c ] [ u ]
[ Y ] = [ d  e  f ] [ v ]
[ 1 ]   [ 0  0  1 ] [ 1 ]
```

如果相机识别的是物料几何中心，而机器人抓取的是边缘偏移点，这对点不对应，标定结果会产生系统性偏差。

### 1.3 操作注意事项

| 要点 | 说明 |
|------|------|
| **标定物选择** | 使用轮廓清晰的圆点或十字标记，确保两端都能精确定位同一几何中心 |
| **找轮廓算法** | 需要稳定可靠（建议亚像素精度），避免光照/噪声导致中心偏移 |
| **机器人示教** | 手动将机器人末端精确移动到相机识别到的中心点（可用针尖或激光笔对齐） |
| **偏移补偿** | 若相机与抓取点存在固定偏移，需在标定前补偿或标定后额外添加偏移量 |

---
### 1.4 九点标定的完整理解

#### 标定的本质

九点标定建立的不仅仅是"像素偏移 → 物理偏移"的简单比例关系，而是一个包含**平移、旋转、缩放、切变**的完整映射矩阵。

| 理解维度 | 简化理解 | 完整理解 |
|---------|---------|---------|
| **映射关系** | 像素偏移 → 物理偏移（线性缩放） | 包含旋转、缩放、平移、切变的仿射变换 |
| **作用区域** | 标定覆盖的那片区域 | 仅对标定时同一平面有效，Z 轴变化会失效 |
| **实际案例** | 像素移动 100 → 物理移动 5mm | 像素移动 100 → 物理移动 4.98mm + 0.1mm（倾斜耦合偏移） |

#### 为什么必须用矩阵而非简单比例

| 影响因素 | 说明 |
|---------|------|
| **旋转** | 相机安装相对于机械手坐标轴可能存在微小偏角（1~2°） |
| **畸变** | 镜头边缘的像素缩放比例与中心不同，广角镜头尤其明显 |
| **切变** | 相机与标定平面不绝对平行时产生梯形变形 |

如果只用单一比例计算，会越抓越偏。九点标定通过 9 个点拟合出 2×3 或 3×3 变换矩阵，同时修正所有上述因素。

#### 修正后的正确表述

> 通过九点标定，建立图像平面到物理平面的完整映射关系。之后只要物体位于标定时的同一平面，通过视觉系统得到图像中任意点坐标，就能用该映射关系准确计算机械手应移动到的物理坐标。

### 1.5 九点标定与匹配方式选择

在 VisionMaster 中，九点标定通常搭配**高精度匹配**使用，原因如下：

| 匹配方式 | 定位精度 | 适用场景 |
|---------|---------|---------|
| **快速匹配** | 像素级，速度快 | 产线上实时定位、跟踪，对速度要求高的场景 |
| **高精度匹配** | 亚像素级，精度更高 | 九点标定、高精度测量、对位引导等需要极高定位精度的场景 |

**为什么九点标定要用高精度匹配**：
- 九点标定的核心是建立像素坐标与物理坐标的精确映射关系
- 如果标定过程中使用的匹配本身就有较大误差（像素级），标定出的变换矩阵也会带有系统性偏差
- 高精度匹配的**亚像素定位能力**可以将标定点提取误差控制在 0.1 像素以内，确保标定精度

> **建议**：九点标定使用高精度匹配采集标定点，产线运行时根据实际节拍要求选择快速匹配或高精度匹配。

---

## 2. VisionMaster 标定文件体系

### 2.1 文件总览

| 文件 | 全称 | 用途 | 生成方式 |
|------|------|------|---------|
| **.iccal** | Internal Camera Calibration | 相机内参标定（畸变校正） | 相机内参标定流程生成 |
| **.iwcal** | World Calibration | 映射标定（图像坐标→物理坐标） | 映射标定流程生成 |
| **.xml** | Hand-Eye Calibration | 手眼标定结果（像素→机器人坐标） | N 点标定流程生成 |

### 2.2 标定流程

```
第一步：相机内参标定（准备基石）
  标定板拍照 → 计算畸变参数 → 生成 .iccal
  作用：校准镜头畸变，确保图像真实反映物理世界

第二步：N 点标定（建立联系）
  加载 .iccal → 记录 N 个点的 (图像坐标, 机器人坐标) 对 → 生成 .xml
  作用：建立"像素 ↔ 物理坐标"的翻译词典
```

### 2.3 .iccal 文件（畸变校正）

- 描述相机镜头的**内部畸变参数**（焦距、主点、畸变系数等），消除镜头畸变（桶形 / 枕形失真）
- 在 N 点标定前必须完成，作为标定的"前置条件"
- 与具体场景无关，同一相机更换场景后通常可复用
- **生成工具**：VisionMaster "畸变校正"（Distortion Calibration）模块
  - 放置 VisionMaster 支持的棋盘格或圆点阵标定板 → 拍摄图像 → 配置畸变类型和中心位置 → 运行工具 → 生成 .iccal

### 2.4 .iwcal 文件（多相机坐标统一）

- **作用**：统一多个相机之间的坐标系，或建立相机与外部设备（机器人 / PLC）的坐标转换关系
- **生成工具**：VisionMaster "相机映射"（Camera Mapping）模块
  - 准备数据：至少两个相机拍摄同一场景，获取多对一一对应的物理点坐标（如圆心或角点）
  - 配置模块：在"相机映射"模块中填入对应点坐标对（如将"相机二"的点映射到"相机一"）
  - 运行并生成标定文件
- **典型场景**：双相机 / 多相机视觉系统需要将各自坐标统一到同一基准坐标系下

### 2.5 .xml 文件（手眼标定产物）

- **作用**：封装 N 点标定的最终结果——像素坐标 ↔ 机器人物理坐标的转换矩阵
- 包含内容：标定矩阵、旋转中心、标定误差、像素精度、坐标系信息等
- **使用方**：VisionMaster 内部与坐标转换相关的算法模块（如定位模块）加载执行
- 工作流程：方案运行时，定位模块读取 .xml → 将相机识别的像素坐标 → 实时转换为机器人物理坐标

### 2.6 标定文件对比总结

| 特性 | .iccal | .iwcal | .xml |
|------|--------|--------|------|
| **核心目标** | 认识"相机"自身 | 校准"相机间"关系 | 连接"像素→物理" |
| **主要作用** | 消除单个相机的镜头畸变 | 统一多相机或相机与外部设备的坐标系 | 将图像像素坐标转换为机器人物理坐标 |
| **生成工具** | 畸变校正模块 | 相机映射模块 | N 点标定模块 |
| **核心输入** | 高精度标定板 | 至少 2 对或更多对应点（不同相机下的同一物理点） | .iccal + N 组(像素坐标, 机器人坐标)对 |
| **管理平台** | VisionMaster | VisionMaster | VisionMaster |

> **类比**：.iccal 是"校准相机镜头"（内功），.iwcal 是"对齐多相机关系"（沟通），.xml 是"建立翻译词典"（像素→物理坐标）。

---
## 3. MVS 与 VisionMaster 的关系与分工

### 3.1 角色定位

| 软件 | 角色 | 专注领域 | 类比 |
|------|------|---------|------|
| **MVS** | 工业相机客户端 | 相机硬件配置与图像采集 | "视觉神经" |
| **VisionMaster** | 算法平台 | 图像处理与逻辑判断 | "大脑" |

### 3.2 MVS 职责（负责"看"）

- 连接并调试相机硬件
- 调整曝光、增益、触发方式等参数
- 确认相机工作正常，获取清晰、稳定的原始图像
- **项目落地后通常不直接参与运行**

### 3.3 VisionMaster 职责（负责"分析"）

- 搭建视觉方案流程（.sol 方案文件）
- 通过"图像源"模块实时采集 MVS 已配置好的相机图像
- 调用定位、测量、检测、识别等算法
- 输出坐标、OK/NG 等决策结果
- 管理标定流程（.iccal / .xml）

### 3.4 典型协作流程

```
┌──────────┐     原始图像     ┌──────────────┐     坐标/结果     ┌────────┐
│  相机     │ ─────────────→ │ VisionMaster  │ ──────────────→ │ 机器人  │
│ (硬件)    │                │ (算法大脑)     │                 │ (执行)  │
└──────────┘                └──────────────┘                 └────────┘
       ↑                          ↑
       │ MVS 配置驱动              │ 加载 .sol / .iccal / .xml
       │ (项目前期)                │ (运行时独立执行)
```

> **总结**：MVS 是硬件驱动 + 配置工具（项目前期使用），VisionMaster 是解决核心视觉问题的开发平台和运行时大脑。

---

## 4. 卡尺工具与边缘检测

### 4.1 基本原理

直线查找通过**卡尺工具（Caliper）**在图像中定位直线边缘，核心步骤：

```
设定 ROI 区域 → 卡尺扫描 → 灰度梯度分析 → 边缘点提取 → 直线拟合
```

### 4.2 关键参数

| 参数 | 含义 | 说明 |
|------|------|------|
| **灰度差值** | 边缘两侧的灰度变化幅度 | 差值越大边缘越明显，需合理设定阈值排除噪声 |
| **阈值** | 判定为边缘的灰度梯度门槛 | 低于阈值忽略，高于阈值判定为边缘点 |
| **极性** | 边缘方向（由明→暗 或 由暗→明） | 可选：正向 / 负向 / 任意 |
| **卡尺个数** | 沿边缘方向投影的卡尺数量 | 越多精度越高，但计算量增大 |
| **剔除点数** | 拟合直线时排除的离群点数量 | 剔除过多边缘噪声点，提升直线拟合稳定性 |
| **边缘点选择** | 每条卡尺内选哪个点作为边缘 | 可选：第一个 / 最后一个 / 最强 / 最弱 |

### 4.3 极性说明

| 极性类型 | 灰度变化方向 | 适用场景 |
|----------|-------------|---------|
| **正向（由暗→明）** | 从低灰度跳变到高灰度 | 黑背景上的亮线 / 亮边 |
| **负向（由明→暗）** | 从高灰度跳变到低灰度 | 亮背景上的暗线 / 暗边 |
| **任意** | 两种方向都检测 | 不确定边缘方向时使用 |

### 4.4 直线拟合方法

所有卡尺提取到的边缘点集合，通过以下方法拟合为一条直线：

- **最小二乘法**：对所有点进行拟合，受离群点影响较大
- **RANSAC**：迭代去除离群点，拟合更鲁棒，适合有噪声的场景

### 4.5 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 找不到直线 | 灰度差过小 / 阈值过高 / 极性选择错误 | 降低阈值 / 切换极性 / 增强图像对比度 |
| 直线角度不准 | 卡尺数量过少 / 边缘点噪声大 | 增加卡尺数 / 调整 ROI 范围 / 使用 RANSAC |
| 结果不稳定 | 光照变化导致边缘位置波动 | 增加光源稳定性 / 使用亚像素精度提取 |

---

### 4.6 圆查找（Circle Finding）

圆查找原理与直线查找相同，区别在于**卡尺方向沿径向由内到外**排列。

```
设定 ROI 圆环区域 → 径向卡尺扫描 → 边缘点提取 → 圆拟合
```

#### 与直线查找的主要区别

| 对比项 | 直线查找 | 圆查找 |
|--------|---------|--------|
| **卡尺方向** | 垂直于直线方向平行排列 | 沿径向由内到外排列 |
| **拟合目标** | 直线（最小二乘法 / RANSAC） | 圆（最小二乘法 / RANSAC） |
| **输出结果** | 直线起点、终点、角度 | 圆心坐标 (Row, Col)、半径 Radius |
| **应用场景** | 直线边缘定位、尺寸测量 | 圆形工件定位、孔径测量、环形区域检测 |

---
## 5. 快速匹配（Fast Matching）

VisionMaster 中的快速匹配模块用于在图像中快速定位目标。

### 5.1 关键参数

| 参数 | 说明 |
|------|------|
| **分数** | 匹配得分阈值，高于该值才认为匹配成功 |
| **匹配个数** | 最多输出的匹配结果数量 |
| **极性** | 匹配时是否考虑灰度极性（同向 / 任意） |
| **角度范围** | 允许目标旋转的角度搜索范围 |
| **尺度范围** | 允许目标缩放的范围（适应远近变化） |

### 5.2 快速匹配 vs 高精度匹配

| 对比项 | 快速匹配 | 高精度匹配 |
|--------|---------|-----------|
| **定位精度** | 像素级 | **亚像素级**（0.1 像素以内） |
| **处理速度** | 快 | 相对较慢 |
| **适用场景** | 产线实时定位、跟踪、对速度要求高的场景 | 九点标定、高精度对位、尺寸测量、需要极高精度的场景 |
| **抗噪能力** | 一般 | 更强（通过更多采样点平均噪声） |
| **模板要求** | 特征明显的目标 | 对对比度较弱或形状复杂的目标仍有较好效果 |

> **选型建议**：
> - **速度优先**（节拍 < 200ms）→ 快速匹配
> - **精度优先**（定位误差 < 0.5 像素）→ 高精度匹配
> - 可在同一项目中混合使用：九点标定用高精度匹配，运行时用快速匹配

---

## 6. 位置修正（Position Correction）

### 6.1 功能概述

位置修正是 VisionMaster 中用于**补偿工件位置偏差**的核心工具模块。在实际产线中，工件到达检测工位时往往存在位置偏移和角度旋转，位置修正模块通过参考位置与实际位置的对比，计算出偏移量并将其补偿到后续的检测/测量区域中。

### 6.2 工作原理

```
模板位置（参考位置）
     ↓ 匹配定位
实际位置（当前检测到的位置）
     ↓ 计算偏移
获取 ΔX, ΔY, Δθ（偏移与旋转量）
     ↓ 补偿
将偏移量应用到 ROI、测量工具等下游模块
```

### 6.3 关键参数

| 参数 | 说明 |
|------|------|
| **参考位置** | 模板训练时记录的标准位置坐标 |
| **匹配方式** | 选择用于定位的匹配模块（快速匹配 / 高精度匹配 / 形状匹配等） |
| **偏移量输出** | 输出的 X/Y 偏移和角度旋转量 |
| **补偿模式** | 平移补偿 / 旋转补偿 / 平移+旋转全补偿 |
| **坐标系** | 像素坐标系 / 物理坐标系（需配合标定结果） |

### 6.4 应用场景

- **引导定位**：机械手抓取前修正工件位置偏差
- **ROI 自适应**：根据工件实际位置动态调整检测区域
- **多工位协同**：同一工件在不同工位之间传递时的位置补偿

---

## 7. 距离测量（点与点的距离 / 点与线的距离）

### 7.1 功能概述

VisionMaster 中的距离测量工具用于计算几何元素之间的距离，支持两种基本模式：

| 模式 | 说明 | 计算公式 |
|------|------|---------|
| **点与点的距离** | 计算图像中两个点之间的欧氏距离 | $d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$ |
| **点与线的距离** | 计算点到直线的垂直距离 | $d = \frac{|Ax_0 + By_0 + C|}{\sqrt{A^2 + B^2}}$ |

### 7.2 典型应用

| 应用场景 | 使用模式 | 说明 |
|---------|---------|------|
| **孔径测量** | 点与点的距离 | 测量圆孔直径（取圆上两点或圆心到边缘点） |
| **间隙测量** | 点与线的距离 | 测量两个零件之间的装配间隙 |
| **尺寸检测** | 点与点的距离 | 测量产品长、宽等外形尺寸 |
| **偏移检测** | 点与线的距离 | 检测引脚是否在允许的偏移范围内 |

### 7.3 精度影响因素

| 因素 | 影响 | 优化方法 |
|------|------|---------|
| **边缘提取精度** | 直接影响点坐标的准确性 | 使用亚像素边缘提取 |
| **标定精度** | 像素距离转物理距离的转换误差 | 确保九点标定质量 |
| **光照稳定性** | 影响边缘定位的一致性 | 稳定光源、增加平均帧 |

---

## 8. 条件分支（Condition Branch）

### 8.1 功能概述

条件分支是 VisionMaster 中的**流程控制**模块，相当于编程语言中的 `if-else` 或多路分支 `switch`。它根据输入条件（匹配结果、测量值、OK/NG 状态等）将执行流程导向不同的分支路径，是实现视觉方案"决策能力"的核心模块。

```
                    ┌── 条件成立 → 执行分支 A
    输入条件 ──────┤
                    └── 条件不成立 → 执行分支 B
```

### 8.2 分支模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| **二分支（if-else）** | 根据条件成立与否，走"成立"或"不成立"两条路径 | OK/NG 判断、阈值判定 |
| **多分支（switch）** | 根据条件的多个取值，路由到不同分支 | 多型号切换、多级分选 |
| **空分支** | 条件不成立时不做任何操作，继续后续流程 | 仅需在特定条件下执行额外处理 |
| **条件跳转** | 满足条件时跳转到流程中的指定步骤 | 重试逻辑、异常恢复流程 |

### 8.3 条件类型

| 条件类型 | 输入来源 | 判断逻辑 |
|---------|---------|---------|
| **分数/置信度** | 匹配模块、分类模块 | 匹配分数 > 阈值 → OK，否则 NG |
| **数值范围** | 测量模块、变量计算 | 测量值 ∈ [下限, 上限] → 合格，否则不合格 |
| **状态标志** | 各模块执行状态 | 模块执行成功/失败 |
| **字符串匹配** | 协议解析、文本识别 | 识别结果是否等于目标字符串 |
| **逻辑组合** | 多个条件的与/或/非组合 | (条件A && 条件B) ‖ 条件C |

### 8.4 典型应用

| 应用场景 | 分支逻辑 | 分支A | 分支B |
|---------|---------|------|------|
| **缺陷判定** | 缺陷检测结果 == NG | 触发报警 + 保存 NG 图像 | 继续正常流程 |
| **多型号切换** | 产品型号 == A/B/C | 切换到对应型号的检测参数 | 报未知型号 |
| **重试机制** | 定位分数 < 阈值 | 调整光源/位置后重新拍照 | 继续执行抓取 |
| **多级分选** | 尺寸等级 1/2/3 | 分别路由到不同的分选出口 | 不合格品出口 |
| **异常兜底** | 测量值超出合理范围 | 跳过该工位，记录异常日志 | 正常输出测量结果 |

### 8.5 使用建议

| 建议 | 说明 |
|------|------|
| **分支完备性** | 始终覆盖所有可能的分支路径，避免流程卡死 |
| **嵌套层级** | 避免过深的条件嵌套（建议不超过 3 层），可用多个条件分支模块串联替代 |
| **条件可观测** | 将分支条件的关键阈值设为可调参数，方便现场调试 |
| **异常分支兜底** | 每个条件分支都应设计"异常/不满足"分支的处理逻辑（如重拍、报警、跳过） |
| **调试标注** | 在分支路径上添加调试输出（如图像标注、文本日志），便于追溯流程走向 |

---


## 9. 格式化（Formatting）
### 9.1 功能概述

格式化模块用于将 VisionMaster 中的各种数据（坐标、测量值、字符串等）按照指定的格式输出，是**数据输出前的重要预处理步骤**。

### 9.2 常用格式化操作

| 操作 | 说明 | 示例 |
|------|------|------|
| **数字格式化** | 设置小数位数、补齐位数 | 3.14159 → 3.14 |
| **字符串拼接** | 将多个变量拼接为指定格式的字符串 | X:123.45, Y:67.89 |
| **坐标格式化** | 将坐标数据格式化为通讯协议所需格式 | (123.45, 67.89) |
| **时间戳格式化** | 将当前时间格式化为文件名/日志格式 | 2026-06-16_143052 |
| **模板字符串** | 使用占位符生成固定模板的输出 | "Result: ${score}, Pos: (${x}, ${y})" |

### 9.3 典型应用

- **通讯输出**：将视觉结果格式化为 PLC/机器人需要的报文格式
- **数据记录**：将测量结果格式化为 CSV/TXT 的写入格式
- **结果显示**：在界面上以友好的格式显示检测结果

---

## 10. 输出保存图像（Output Save Image）

### 10.1 功能概述

输出保存图像模块用于**将当前图像保存到指定路径**，在调试、追溯、数据收集等场景中非常实用。

### 10.2 关键参数

| 参数 | 说明 |
|------|------|
| **保存路径** | 图像文件的存储目录 |
| **文件命名** | 支持自定义文件名或使用自动命名（时间戳、序号） |
| **图像格式** | BMP / JPG / PNG / TIFF 等 |
| **保存条件** | 全部保存 / 仅 NG 保存 / 按条件触发保存 |
| **覆盖策略** | 覆盖旧文件 / 自动递增文件名 / 按日期分目录 |

### 10.3 应用场景

| 场景 | 保存策略 | 用途 |
|------|---------|------|
| **调试阶段** | 全部保存 | 分析算法效果，积累样本 |
| **产线运行** | 仅 NG 保存 | 缺陷追溯，减少存储开支 |
| **定期抽检** | 按帧率采样保存 | 产线状态监控 |
| **工艺验证** | 连续保存一批次 | 做 GR&R 分析 |

> **注意**：频繁保存图像会占用大量存储空间和 I/O 带宽，建议产线运行时仅在需要时保存，或仅保存 NG 图像。

---

## 11. 变量计算（Variable Calculation）

### 11.1 功能概述

变量计算模块是 VisionMaster 中的**数学运算工具箱**，用于对测量结果、坐标数据等进行算术运算、逻辑运算和函数计算。

### 11.2 支持的计算类型

| 计算类型 | 说明 | 示例 |
|---------|------|------|
| **算术运算** | 加、减、乘、除、取余 | 坐标偏移量计算、平均值计算 |
| **三角函数** | sin、cos、tan、atan2 等 | 根据角度计算 X/Y 分量 |
| **比较运算** | 大于、小于、等于、范围判断 | 尺寸合格性判断 |
| **逻辑运算** | 与、或、非 | 多条件复合判断 |
| **数值函数** | 绝对值、取整、开方、取最大值/最小值 | 计算距离的绝对值 |
| **单位换算** | 像素 ↔ 物理单位 | 配合标定结果进行单位转换 |

### 11.3 典型应用

- **偏移计算**：计算当前坐标与参考坐标的差值
- **均值滤波**：连续多帧测量结果的平滑处理
- **坐标变换**：在不同坐标系之间转换（配合标定矩阵）
- **阈值计算**：根据测量结果动态计算判定阈值

---

## 12. 协议解析（Protocol Parsing）

### 12.1 功能概述

协议解析模块用于 VisionMaster 与外部设备（PLC、机器人、上位机等）之间的**数据通讯与解析**，是实现视觉系统与自动化系统集成的关键模块。

### 12.2 支持的通讯方式

| 通讯方式 | 适用场景 | 特点 |
|---------|---------|------|
| **TCP/IP** | 与上位机、MES 系统通讯 | 通用性强，支持跨平台 |
| **UDP** | 高速数据广播 | 速度快但不保证可靠 |
| **串口（RS232/485）** | 与 PLC、老设备通讯 | 简单可靠，速度较慢 |
| **Modbus TCP/RTU** | 与工业设备通讯 | 工业标准协议 |
| **EtherCAT** | 与高端运动控制器通讯 | 实时性极高 |

### 12.3 关键参数

| 参数 | 说明 |
|------|------|
| **协议类型** | TCP 客户端/服务端、UDP、串口、Modbus 等 |
| **IP 地址/端口** | 目标设备的网络地址 |
| **波特率/数据位** | 串口通讯参数 |
| **报文格式** | 帧头、数据区、校验、帧尾的定义 |
| **解析规则** | 从报文中提取有效数据的方式（按字节偏移、按分隔符等） |
| **发送触发** | 条件触发 / 周期发送 / 请求-应答模式 |

### 12.4 典型通讯流程

```
Vision Master                 外部设备（PLC/机器人）
     │                                │
     │  ── 发送结果报文 ─────────→     │  接收坐标/OK/NG
     │                                │
     │  ←── 接收请求/触发 ──────────   │  发送拍照请求/参数
     │                                │
```

### 12.5 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| **通讯超时** | 网络不通 / IP 端口错误 / 防火墙拦截 | 检查网络连通性（ping 测试） |
| **数据解析错误** | 报文格式不匹配 / 字节序不对 | 确认双方协议文档一致，检查大端/小端 |
| **数据粘包** | TCP 连续发送时数据合并 | 使用固定长度报文或添加帧头帧尾分隔 |
| **通讯断开** | 物理连接异常 / 设备重启 | 添加心跳机制和自动重连逻辑 |

---

## 13. 文本保存（Text Save）

### 13.1 功能概述

文本保存模块用于将视觉检测结果、测量数据等**保存到文本文件**（TXT / CSV / Excel 等），实现数据追溯和报表生成。

### 13.2 关键参数

| 参数 | 说明 |
|------|------|
| **保存路径** | 文件存储目录 |
| **文件格式** | TXT / CSV / 自定义格式 |
| **保存模式** | 覆盖写 / 追加写 / 按日期分文件 |
| **内容格式** | 分隔符（逗号、制表符、空格）、固定列宽 |
| **保存触发** | 每次检测保存 / 按条件保存 / 批次结束时保存 |

### 13.3 典型应用

| 应用场景 | 格式 | 用途 |
|---------|------|------|
| **测量数据记录** | CSV | 导入 Excel 做统计分析 |
| **检测日志** | TXT | 产线运行状态追踪 |
| **追溯报表** | CSV | 每件产品的完整检测记录 |
| **SPC 数据** | CSV | 制程能力分析（CPK/GR&R） |

### 13.4 使用建议

- **文件命名**：建议包含时间戳和批次号，避免重名覆盖
- **存储周期**：定期清理历史数据，或按日期自动分目录
- **写入性能**：高频检测时建议使用缓存批量写入，避免频繁磁盘 I/O
- **编码选择**：与下游系统对接时注意编码一致性（UTF-8 / GBK）

---

## 14. 组合模块（Combination Module）

### 14.1 功能概述

组合模块是 VisionMaster 中**将多个基础模块封装为一个可复用的模块单元**的功能，用于简化复杂方案的搭建和维护。

### 14.2 主要作用

| 作用 | 说明 |
|------|------|
| **逻辑封装** | 将一组固定流程的模块打包，外部只需关注输入/输出 |
| **复用性** | 同一套处理流程可在多个方案中重复使用 |
| **简化界面** | 减少主流程中的模块数量，提高可读性 |
| **标准化** | 将常用的检测逻辑固化为标准模块，便于团队协作 |

### 14.3 典型使用场景

- **标准定位流程**：图像预处理 → 匹配定位 → 位置修正，封装为一个"定位组合"
- **测量模板**：边缘提取 → 卡尺测量 → 结果判断，封装为一个"测量组合"
- **通讯处理**：协议解析 → 数据校验 → 变量赋值，封装为一个"通讯组合"

### 14.4 使用建议

| 建议 | 说明 |
|------|------|
| **接口清晰** | 明确定义组合模块的输入参数和输出结果 |
| **命名规范** | 使用有意义的名称，方便他人理解和复用 |
| **文档说明** | 在组合模块内添加注释说明流程和参数含义 |
| **适度拆分** | 一个组合模块不要包含过多子模块，保持可维护性 |

---

## 15. 通讯与标定流程（TCP + 全局触发）

### 15.1 上位机触发 VM 标定流程

在 VisionMaster 的实际项目中，常需要从上位机（PC/PLC）发送指令触发 VM 执行标定流程，典型通讯方式为 **TCP 通讯 + 字符串触发**。

#### 标准配置步骤

| 步骤 | 操作 | 说明 |
|------|------|------|
| **① TCP 服务端** | 在 VM 中开启 TCP 服务端（接收数据模块） | 本机 IP 设为 `0.0.0.0`（远程连接时），端口与上位机约定 |
| **② 字符串触发** | 在"流程全局触发"中配置字符串触发，使用**部分匹配**模式 | 上位机发送 `Calib` 即可触发对应流程，无需完全匹配 |
| **③ 数据解析** | 在脚本中使用 `Split` 函数分割接收到的字符串 | 提取出需要的变量值（如标定点坐标） |
| **④ 变量映射** | 脚本中的输入变量**初始值**链接到"接收数据"模块的 Out 端口 | 确保数据正确流入脚本 |
| **⑤ 全局变量** | 在全局变量中添加需要用到的变量名 | 注意变量名称与脚本中定义的一致 |
| **⑥ 标定执行** | VM 执行标定流程，生成标定文件 | 如果传入的物理坐标有问题，最后一步会计算出错，导致无法生成标定文件（仅标定点存在） |

#### 典型流程图

```
上位机                          VisionMaster
  │                                  │
  │ ── TCP 发送 "Calib,x1,y1,..." ──→│  接收数据模块
  │                                  │   ↓
  │                                  │  全局触发（字符串匹配 "Calib"）
  │                                  │   ↓
  │                                  │  脚本解析（Split 提取坐标）
  │                                  │   ↓
  │                                  │  执行标定 → 生成 .iccal / .xml
  │ ←── TCP 返回结果 ────────────────│
```

### 15.2 关键配置细节

#### 远程连接：本机 IP 设为 0.0.0.0

当 VisionMaster 作为服务端、上位机作为客户端远程连接时：
- VM 端 IP 需设为 `0.0.0.0`（监听所有网络接口）
- 上位机连接 VM 主机的实际 IP 地址
- 确保防火墙允许对应端口的 TCP 连接

#### 全局触发：字符串触发与部分匹配

| 参数 | 说明 |
|------|------|
| **触发方式** | 字符串触发 |
| **匹配模式** | 部分匹配（上位机发送的字符串包含关键词即触发） |
| **触发关键词** | 如 `Calib`、`Start`、`Trigger` 等 |
| **优点** | 无需完全匹配，可在同一报文中携带额外参数（如坐标值） |

#### 脚本解析：Split 提取变量

```
接收数据: "Calib,100.5,200.3,150.8,250.6,..."
                  ↓
脚本 Split(',') 分割
                  ↓
arr[0] = "Calib"     → 触发标识
arr[1] = "100.5"     → X1 坐标
arr[2] = "200.3"     → Y1 坐标
arr[3] = "150.8"     → X2 坐标
arr[4] = "250.6"     → Y2 坐标
...                  → 依次赋值给全局变量
```
#### 脚本代码示例（C#）

以下是在 VM 脚本中解析上位机标定指令的完整示例：

```csharp
public bool Process()
{
    //You can add your codes here, for realizing your desired function
    
    // 调试：把 recStr 的真实内容写入日志文件
	System.IO.File.WriteAllText(@"D:\debug_recStr.txt", recStr);
    
    string[] rec = recStr.Split(',');
    
    if (rec[0]=="Calib")
    {
    	GlobalVariableModule.SetValue("MX", rec[1]);
		GlobalVariableModule.SetValue("MY", rec[2]);        	
    }
    
    //out0 = Convert.ToInt32(rec[0]);
    out1 = Convert.ToInt32(rec[1]);
    out2 = Convert.ToInt32(rec[2]);
    
    return true;
}
```

**代码说明**：

| 行 | 作用 |
|----|------|
| `File.WriteAllText` | 将接收到的原始字符串写入日志文件，用于调试排查 |
| `recStr.Split(',')` | 按逗号分割接收到的字符串为数组 |
| `rec[0]=="Calib"` | 判断触发指令是否为标定请求 |
| `GlobalVariableModule.SetValue` | 将解析出的坐标值写入 VM 全局变量（MX, MY） |
| `out1 / out2` | 将坐标值赋给流程输出端口，供下游模块使用 |

> **提示**：调试完成后建议注释或删除 `File.WriteAllText` 行，避免频繁磁盘 I/O 影响产线性能。


### 15.3 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| **标定文件生成失败** | 传入的物理坐标数据异常（格式错误/数值越界） | 检查上位机发送的坐标值是否在合理范围内 |
| **流程未触发** | 字符串匹配模式配置错误 / TCP 未连接 | 确认全局触发中的关键词与上位机发送的一致 |
| **变量值为空** | 脚本输入变量未链接到接收数据 Out | 检查脚本输入变量的"初始值"链接是否正确 |
| **连接失败** | IP 未设 0.0.0.0 / 端口冲突 / 防火墙拦截 | 确认 VM 端 IP 配置，检查端口占用和防火墙规则 |

### 15.4 耗时统计

VisionMaster 提供**耗时统计**功能，用于分析每个模块的执行时间，是排查性能瓶颈的重要工具。

| 统计项 | 说明 |
|--------|------|
| **单模块耗时** | 每个模块的单次执行耗时（ms） |
| **总流程耗时** | 整个视觉方案的单次执行总耗时 |
| **最大/最小/平均** | 多次运行的统计数据 |
| **耗时占比** | 各模块耗时占总耗时的百分比 |

**使用场景**：
- 定位节拍瓶颈（哪个模块最耗时）
- 对比不同参数设置的性能差异
- 优化前/后的效果验证

### 15.5 默认软件界面打开

在 VM 方案配置中，可以设置**默认打开的软件界面**，方便操作员使用：

| 设置项 | 说明 |
|--------|------|
| **默认界面** | 启动 VM 运行时自动显示的界面（如结果展示、调试视图） |
| **界面布局** | 可预设多个窗口布局方案 |
| **权限控制** | 操作员界面 / 工程师界面 / 管理员界面分权限配置 |

---

## 16. 自动化生产流程案例

### 16.1 案例概述

从**获取图像 → 标定转换 → 计算偏移 → 返回数据**的完整自动化生产流程，是视觉引导机械手的典型应用。本节以一个实际案例梳理完整的环节和关键配置。

### 16.2 完整流程

```
获取图像
    ↓
高精度匹配 + 位置修正
    ↓
在 ROI 区域做目标查找
    ↓
┌─── 标定转换① ───┐
│ 图像坐标 → 物理坐标 │  图像基准坐标转换
└─────────────────┘
    ↓
┌─── 标定转换② ───┐
│ 图像坐标 → 物理坐标 │  查找目标坐标转换
└─────────────────┘
    ↓
┌─── 计算① ───┐
│ 基准物理坐标    │
│ - 目标物理坐标  │  →  物理偏移量（应移动的距离）
└──────────────┘
    ↓
┌─── 计算② ───┐
│ 机械手坐标      │
│ + 物理偏移量    │  →  实际抓取位置
└──────────────┘
    ↓
结构化数据 → 发送给上位机
```

### 16.3 各环节详解

#### ① 图像获取与匹配定位

| 步骤 | 模块 | 说明 |
|------|------|------|
| **获取图像** | 图像源 | 从相机获取待处理图像 |
| **高精度匹配** | 高精度匹配 | 在图像中定位目标，输出匹配位置和分数 |
| **位置修正** | 位置修正 | 根据匹配结果修正后续 ROI 区域的位置偏移 |

#### ② 标定转换（两个独立的转换）

| 标定转换 | 输入 | 输出 | 用途 |
|---------|------|------|------|
| **① 图像基准转换** | 图像基准点坐标（像素） | 图像基准物理坐标 | 代表产品在理想位置时的物理坐标 |
| **② 目标转换** | 查找到的目标坐标（像素） | 目标物理坐标 | 代表当前产品实际位置的物理坐标 |

#### ③ 偏移计算

```
计算①：物理偏移量 = 目标物理坐标 - 基准物理坐标
       →  机械手应移动的距离（X/Y 方向的差值）

计算②：实际抓取位置 = 机械手当前坐标 + 物理偏移量
       →  发送给上位机的最终目标位置
```

#### ④ 数据发送

将计算得到的目标位置进行**结构化处理**，然后通过 TCP/串口等通讯方式发送给上位机（PLC/机器人控制器）。

### 16.4 关键变量说明

| 变量 | 来源 | 说明 |
|------|------|------|
| **机械手坐标** | 全局变量（可通过网络通讯接收 + 脚本赋值） | 机械手当前在物理空间中的位置 |
| **图像基准坐标** | 全局变量 | 产品在理想位置时对应的图像坐标 |
| **目标坐标** | 高精度匹配 + 目标查找的输出 | 当前产品在图像中的实际位置 |
| **物理偏移量** | 计算①的结果 | 两个物理坐标的差值，即机械手需要移动的距离 |
| **最终位置** | 计算②的结果 | 结构化输出后发送给上位机 |

### 16.5 注意事项

| 要点 | 说明 |
|------|------|
| **标定一致性** | 两个标定转换必须使用同一组标定参数（同一个 .iwcal 或 .xml 文件），否则坐标系统一会导致偏移计算错误 |
| **机械手坐标更新** | 机械手坐标作为全局变量，每次抓取后需从上位机更新，或在脚本中根据运动模型推算 |
| **结构化输出** | 发送给上位机的数据建议采用固定格式（如 `OK,X,Y,Angle` 或 `NG,ErrorCode`），方便上位机解析 |
| **坐标防呆** | 在计算①之后加入条件判断：若物理偏移量超出合理范围（如 > 10mm），说明定位异常，应触发重拍或报警 |
| **调试手段** | 可使用"输出保存图像"模块保存每次检测的图像，配合"文本保存"模块记录坐标数据，便于追溯 |

---


