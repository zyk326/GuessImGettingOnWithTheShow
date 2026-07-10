# AlphaAnomaly 工程解构文档

> 文档生成日期：2026-06-29  
> 项目路径：`G:\笔记本上的文件\开发\AlphaAnomaly-master`

---

## 一、工程概览

**AlphaAnomaly** 是一个基于 **C++17** 的工业异常检测推理 SDK，支持 **ONNX Runtime（ORT）** 和 **TensorRT（TRT）** 双后端，具备 GPU 加速、模型加密、多格式可视化等能力，适用于工业质检中的缺陷检测场景。

| 元数据 | 说明 |
|---|---|
| 开发语言 | C++17 |
| 构建系统 | Visual Studio 2019/2022 (v142/v143) |
| 依赖框架 | OpenCV、ONNX Runtime 1.12.1、TensorRT 8.5.3.1、CUDA 11.4 |
| 平台 | Windows x64 |
| 输出类型 | Release 下为动态库(DLL)，Debug 下为控制台应用(EXE) |

---

## 二、目录结构

```
AlphaAnomaly-master/
├── app/                          # 对外公开的 API 头文件
│   ├── AlphaAnomaly.h            # 主 API 接口（核心数据结构 + 类声明）
│   └── bohrtype.h                # 通用基础类型定义（Box、BohrData、ResultType 等）
├── src/                          # 核心实现源码
│   ├── AlphaAnomaly.cpp          # 外观类实现（模型加载分发、预测委托）
│   ├── AnomalyBase.h / .cpp      # 抽象基类（定义统一的推理接口）
│   ├── OrtAnomaly.h / .cpp       # ONNX Runtime 后端实现
│   ├── TrtAnomaly.h / .cpp       # TensorRT 后端实现
│   ├── crypto/                   # 模型加解密模块（静态链接 .lib + .dll）
│   │   ├── AlphaCrypto.h         # 加解密 API 头文件
│   │   ├── AlphaCrypto.dll       # 运行时动态库
│   │   ├── AlphaCrypto.lib       # 导入库
│   │   └── AlphaCrypto.exp       # 导出符号文件
│   └── utils/                    # 工具函数
│       ├── anomalyUtil.h / .cpp  # 异常检测后处理工具（掩码、热力图、可视化）
│       └── opencvUtils.h / .cpp  # 通用 OpenCV 图像处理工具
├── test/                         # 测试工程
│   ├── main.cpp                  # 测试主入口（批量模型推理性能测试）
│   ├── testUtils.h               # 测试工具函数（图像保存、文件遍历）
│   ├── alphaTimer.h              # 高性能计时器封装
│   ├── test.vcxproj              # 测试工程配置
│   ├── images/                   # 测试图片
│   └── model/
│       └── main.cpp              # 另一套独立性能基线测试（含 GPU 监控）
├── 解构/                          # （空）用于存放解构分析文档
├── AlphaAnomaly.sln              # Visual Studio 解决方案文件
├── AlphaAnomaly.vcxproj          # 主工程配置（动态库）
├── AlphaAnomaly.vcxproj.filters  # 工程文件筛选器
└── readme.md                     # 工程说明文档
```

---

## 三、核心架构设计

### 3.1 设计模式

项目巧妙组合了三种设计模式：

| 模式 | 位置 | 作用 |
|---|---|---|
| **策略模式 (Strategy Pattern)** | `AnomalyBase` → `OrtAnomaly` / `TrtAnomaly` | 不同的推理后端可互相替换 |
| **外观模式 (Facade Pattern)** | `AlphaAnomaly` | 对外提供统一的 `LoadModel` + `Predict` 接口，屏蔽内部后端差异 |
| **简单工厂方法 (Simple Factory Method)** | `createImpl()` 函数 | 根据 `BackendType` 创建对应的后端实例 |

**关于工厂模式的深入解读**：`createImpl()` 虽然只是一个独立函数而非工厂类，但它是标准的简单工厂方法。它将所有后端的实例化逻辑集中到一处管理——调用方只依赖 `AnomalyBase` 抽象基类，无需知道 `OrtAnomaly` 或 `TrtAnomaly` 的存在。这就是**依赖倒置原则**的实践。如果不抽这个函数，每处需要创建后端的代码都得自己写 switch 分支，新增后端时就要改多个地方。

对比完整工厂模式家族：

| 特征 | 简单工厂（本工程） | 工厂方法 | 抽象工厂 |
|---|---|---|---|
| 定义位置 | 一个独立普通函数 | 基类纯虚函数，子类各自实现 | 专门工厂类，生产一族产品 |
| 调用方式 | `createImpl(type)` | `factory->Create()` | `factory->CreateProductA/B()` |
| 本工程场景 | 一个 switch 管所有后端 | 每个后端子类自己管创建 | N/A |
### 3.2 命名空间解耦：为什么 typedef Box = BohrInfer::Box

在 `AlphaAnomaly.h` 中可以看到这样一行：

```cpp
typedef BohrInfer::Box Box;   // C++03 风格，等价于 C++11 的 using Box = BohrInfer::Box;
```

从编译角度看，直接写 `BohrInfer::Box` 完全能通过，但这里用 typedef 有三层设计意图：

| 层面 | 说明 |
|---|---|
| **命名空间快捷方式** | `Alpha::Anomaly` 下所有代码直接写 `Box`，不用到处写 `BohrInfer::Box`，提升了数千行代码中的可读性 |
| **抽象解耦** | 如果未来替换底层库，只需改这一行 typedef，所有 `Box` 引用自动适配新类型，编译器会在改完后检查所有使用处是否兼容 |
| **API 语义自描述** | `Alpha::Anomaly::Box` 对外传达"这是 SDK 自己的 Box 类型"，不暴露底层实现细节 |

### 3.3 类关系图

```
AlphaAnomaly (外观类)
  │
  ├── std::unique_ptr<AnomalyBase> m_impl  (Pimpl 模式)
  │
  └── AnomalyBase (抽象基类)
       │
       ├── OrtAnomaly   ──── ONNX Runtime 推理
       │
       └── TrtAnomaly   ──── TensorRT 推理
```

### 3.4 核心数据流

```
                        ┌──────────────┐
                        │  模型文件      │
                        │ (.alphaengine │
                        │  /.onnx/.engine)│
                        └──────┬───────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  AlphaAnomaly         │
                    │  ::LoadModel()        │
                    │                      │
                    │  1. 解密加密模型       │
                    │  2. 匹配后端           │
                    │  3. 创建 ORT/TRT 实例  │
                    └──────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
            ┌──────────────┐    ┌──────────────┐
            │  OrtAnomaly   │    │  TrtAnomaly   │
            │  LoadModel()  │    │  LoadModel()  │
            └──────┬───────┘    └──────┬───────┘
                   │                   │
                   ▼                   ▼
            ┌──────────────┐    ┌──────────────┐
            │  Predict()    │    │  Predict()    │
            │               │    │               │
            │ 1. Preprocess │    │ 1. Preprocess │
            │ 2. Run()      │    │ 2. enqueueV2  │
            │ 3. 解析输出    │    │ 3. 解析输出   │
            └──────┬───────┘    └──────┬───────┘
                   │                   │
                   ▼                   ▼
            ┌──────────────────────────────┐
            │      AnomalyResult            │
            │  { anomalyMap, score }        │
            └──────────────┬───────────────┘
                           ▼
            ┌──────────────────────────────┐
            │      postProcess()            │
            │                               │
            │ 1. 二值化 Mask (阈值 0.5)     │
            │ 2. 连通域分析 → 检测框        │
            │ 3. 计算异常面积                │
            │ 4. (可选) 生成可视化图像       │
            └──────────────┬───────────────┘
                           ▼
            ┌──────────────────────────────┐
            │      AnomalyOutput            │
            │  { result, info, visuals }    │
            └──────────────────────────────┘
```

---

## 四、核心数据结构详解

### 4.1 `AnomalyResult` — 原始推理结果

```cpp
struct AnomalyResult {
    cv::Mat anomalyMap;   // 32FC1, 模型直接输出的异常热力图
    float score = 0.0f;   // 整图异常得分 (0~1，越高越异常)
};
```

### 4.2 `AnomalyVisuals` — 可视化图像集

```cpp
struct AnomalyVisuals {
    cv::Mat heatmap;     // 纯热力图（CV_8UC3，伪彩色 JET）
    cv::Mat mask;        // 二值化 Mask（CV_8UC1，非零=异常区域）
    cv::Mat maskEdge;    // 异常轮廓绘制在原图上（CV_8UC3）
    cv::Mat blended;     // 全图热力图叠加（含检测框，CV_8UC3）
    cv::Mat overlay;     // 仅异常区域热力图叠加（CV_8UC3）

    AnomalyVisuals() = default;          // 默认构造
    AnomalyVisuals(...) { ... }          // 带参构造
};
```

**深入 `= default`**：这个 struct 有 5 个 `cv::Mat` 成员，每个 Mat 的默认构造会把自己置为 empty 状态（`data = nullptr`）。但这里不能省略 `= default`，原因很微妙：

**隐式默认构造被抑制了**。一旦手工写了任何一个构造函数（这里的带参构造），编译器就不再隐式生成默认构造。如果没有这行，代码中写 `AnomalyVisuals v;` 或 `std::vector<AnomalyVisuals> vec(10);` 都会编译失败——它们都需要默认构造。

**那为什么不用 `AnomalyVisuals() {}`？** 两者技术上都能工作，但有区别：

- `= default` 保持构造函数 **trivial**（POD 特性保留），编译器可以做更激进的优化，且 `std::is_trivially_constructible_v` 为 true
- `{}` 使构造函数变为 non-trivial，编译器认为"这里有用户自定义逻辑"，即使函数体是空的
- 语义信号上，`= default` 传达"我就是要编译器默认行为"，`{}` 则是"我写了个空函数体"

**C++20 的另一种选择**：如果删除所有用户声明的构造函数，这个 struct 会变回 aggregate，可以用聚合初始化：

```cpp
AnomalyVisuals v;                        // 聚合初始化，全成员默认值
AnomalyVisuals v2{heatmap, mask, ...};  // 聚合初始化
```

但 C++17 及以前，一旦有用户声明的构造函数（`= default` 也算），struct 就不再是 aggregate 了。
### 4.3 `AnomalyInfo` — 业务信息

```cpp
struct AnomalyInfo {
    std::vector<Box> boxes;   // 异常检测框数组（name="anomaly", id=20260415）
    int anomalyArea = 0;      // 异常区域总像素数
};
```

### 4.4 `AnomalyOutput` — 完整输出

```cpp
struct AnomalyOutput {
    AnomalyResult result;    // 原始推理结果
    AnomalyInfo info;        // 业务核心信息
    AnomalyVisuals visuals;  // 可视化图像集
};
```

### 4.5 `Box` — 检测框

```cpp
struct Box {
    int id;                // 结果类别 ID
    float confidence;      // 置信度
    cv::Rect box;          // 矩形框
    cv::RotatedRect rotbox;// 旋转框（OBB 场景）
    cv::Mat boxMask;       // 框内精确 Mask
    std::string name;      // 类别名称
};
```

### 4.6 后端类型枚举

```cpp
enum class BackendType : int {
    ONNX = 0,       // ONNX Runtime
    TENSORRT = 1    // TensorRT
};
```

---

## 五、模型加载逻辑 (`AlphaAnomaly::LoadModel`)

### 5.1 支持的模型文件格式

| 扩展名 | 说明 |
|---|---|
| `.onnx` | 原生 ONNX 模型，直接使用 ORT 后端 |
| `.engine` | 原生 TensorRT 引擎，直接使用 TRT 后端 |
| `.alphaengine` | 加密模型包，需先解密再按指定/优先级选择后端 |

### 5.2 加载流程

```
LoadModel(enginePath, backend, useGPU, deviceId, warmUp)
  │
  ├── 扩展名 = .onnx → 创建 OrtAnomaly → LoadModel(文件路径)
  │
  ├── 扩展名 = .engine → 创建 TrtAnomaly → LoadModel(文件路径)
  │
  └── 扩展名 = .alphaengine
       │
       ├── 读取文件到内存
       ├── 用密钥 "Zhouzg0226@163.com" 解密 → 得到 ModelInfo
       │
       ├── 按优先级列表选取模型数据
       │   ├── 指定 ORT → [ortModel, trtModel]
       │   ├── 指定 TRT → [trtModel, ortModel]
       │   └── 默认 → [trtModel, ortModel]
       │
       └── 尝试加载（跳过空 buffer），成功后停止
```

### 5.3 关键代码片段

```cpp
// AlphaAnomaly.cpp
std::unique_ptr<AnomalyBase> createImpl(BackendType backend) {
    switch (backend) {
        case BackendType::ONNX:     return std::make_unique<OrtAnomaly>();
        case BackendType::TENSORRT: return std::make_unique<TrtAnomaly>();
        default:                    return nullptr;
    }
}
```

加密模型使用独立 `AlphaCrypto` 库（.lib + .dll），加密密钥硬编码为 `"Zhouzg0226@163.com"`。

关于工厂函数 `createImpl()` 的工程价值：这个函数集中管理了所有后端的实例化逻辑。如果不抽它，`AlphaAnomaly::LoadModel` 中创建模型实例的地方就得直接写：

```cpp
if (...) m_impl = std::make_unique<OrtAnomaly>();
else       m_impl = std::make_unique<TrtAnomaly>();
```

这本身看似没问题，但如果未来 `LoadModel` 中还有第二处、第三处需要创建后端实例（比如重载测试中的反复创建），每处都得写同样的分支。工厂模式改一处，散落版每处都要改。---

## 六、推理后端详解

### 6.1 ONNX Runtime 后端 (`OrtAnomaly`)

#### 初始化
- 创建 ORT 环境（日志级别 WARNING）
- 创建 CPU MemoryInfo（ArenaAllocator）
- 根据 `m_useGPU` 检测并启用 CUDA Execution Provider
- 设置优化级别 `ORT_ENABLE_ALL`，线程数 `IntraOp=4, InterOp=2`

#### 模型加载

```
LoadModel(...)
  ├── checkGPUInfo(useGPU, deviceId)
  ├── updateSessionOption()     // 配置 CUDA EP + 优化选项
  ├── 创建 Ort::Session
  └── InitModelFromSession()
       ├── 读取输入节点信息（名称、数据类型、shape）
       ├── 自动补全动态 batch/height/width
       ├── 读取输出节点（要求 2 或 4 个输出）
       └── GPU 预热（3 次 dummy 推理）
```

**补充：AnomalyBase 构造函数的 CUDA 检测**。基类构造函数中有这样一段代码：

```cpp
AnomalyBase() {
    auto flag = cudaGetDeviceCount(&m_deviceCount);
}
```

这里 `m_deviceCount` 通过指针参数**输出**拿到了显卡数量；而 `flag` 是函数返回值（`cudaError_t` 类型），代表调用状态——可能的取值有 `cudaSuccess`（成功）、`cudaErrorNoDevice`（没检测到设备）、`cudaErrorInsufficientDriver`（驱动版本不够）。这段代码定义 `flag` 但从未检查它。如果调用失败（比如没装 CUDA 驱动），`m_deviceCount` 不会被写入，后续 `checkGPUInfo()` 基于未写入的值做判断，行为不可预期。正确的防御写法应该是：

```cpp
AnomalyBase() {
    auto err = cudaGetDeviceCount(&m_deviceCount);
    if (err != cudaSuccess) {
        m_deviceCount = 0;  // 安全降级
    }
}  
```
#### 前处理 (`Preprocess`)
```
BGR图像
  ├── cvtColor(BGR→RGB)
  ├── resize(到模型输入尺寸, INTER_LINEAR)
  ├── convertTo(float32, 1/255.0)   // 归一化到 [0,1]
  ├── split(HWC→CHW)
  └── 组装为 4D blob [1,3,H,W]
```

#### 推理 (`Predict`)
```
输入 blob
  ├── 创建 Ort::Value 张量
  ├── session.Run()
  ├── 输出[0] → score
  ├── 输出[1] → label
  ├── 输出[2] → anomaly_map (resize到原图尺寸)
  └── 输出[3] → (如果存在 4 个输出，则使用)
```

### 6.2 TensorRT 后端 (`TrtAnomaly`)

#### 初始化
- 自定义 `TRTLogger`（静默日志）
- 设置 CUDA 设备
- 创建 `IRuntime` → `deserializeCudaEngine` → `createExecutionContext`

#### Binding 解析
```
遍历所有 binding:
  ├── 输入 binding → 记录 dims (C/H/W) + 计算 inputSize
  └── 输出 binding → 记录索引 + 计算对应 size
```

#### 内存分配
- 为 input binding 分配显存
- 为每个 output binding 分配显存 + 对应的 Host 内存

#### 推理 (`Predict`)
```
输入图像
  ├── Preprocess (同 ORT)
  ├── cudaMemcpyAsync (Host→Device)
  ├── context.enqueueV2() (异步推理)
  ├── cudaMemcpyAsync (Device→Host, 每个输出)
  ├── cudaStreamSynchronize()
  └── 按 binding name 解析输出 (score/label/map)
```

**与 ORT 不同**：TRT 必须使用 GPU，不支持纯 CPU 推理。

---

## 七、后处理管线 (`postProcess`)

```
postProcess(image, result, threshold, isVisual)
  │
  ├── 1. compute_mask_hybrid()
  │    ├── 阈值二值化 (threshold, 默认 0.5)
  │    ├── 形态学开运算（去除噪点）
  │    └── 缩放到 0/255
  │
  ├── 2. 计算业务信息
  │    ├── anomalyArea = countNonZero(mask)
  │    └── boxes = getConnectedRegions(mask, anomalyMap)
  │         ├── 连通域分析 (connectedComponentsWithStats)
  │         ├── 面积过滤 (< 50 像素跳过)
  │         └── 返回 Box 数组 (id=20260415, name="anomaly")
  │
  └── 3. (可选) 生成可视化 genImages()
       ├── heatmap: anomalyMap → 8UC1 → COLORMAP_JET
       ├── mask: 二值化 + 形态学处理
       ├── maskEdge: Canny 边缘 + 叠加原图
       ├── blended: heatmap + 原图(0.6/0.4) + 检测框
       └── overlay: 异常区域伪彩色叠加
```  

### 可视化效果描述

| 图像 | 内容 |
|---|---|
| `heatmap` | 纯伪彩色热力图，蓝色=正常 → 红色=异常 |
| `mask` | 黑白二值图，白色=异常区域 |
| `maskEdge` | 原图上绘制红色异常轮廓 |
| `blended` | 热力图半透明叠加 + 绿色/黄色/红色检测框 |
| `overlay` | 仅异常区域有伪彩色，其余保持原图 |

检测框颜色规则：
- 置信度 > 0.85 → 绿色
- 置信度 > 0.70 → 黄绿色
- 置信度 > 0.50 → 黄色
- 置信度 <= 0.50 → 红色

---  

## 八、工具函数库

### 8.1 `anomalyUtil.h/.cpp`

| 函数 | 功能 |
|---|---|
| `getImagePaths()` | 遍历文件夹获取所有图片路径 |
| `readImage()` | 读取 BGR 图像 |
| `saveScoreAndImages()` | 保存得分和图像 |
| `cvNormalizeMinMax()` | 热力图归一化（阈值裁剪 + 缩放） |
| `superimposeAnomalyMap()` | 热力图叠加到原图（归一化 + JET + addWeighted） |
| `addLabel()` | 在图像左上角添加置信度标签 |
| `compute_mask()` | 二值化 Mask + 形态学开运算 |
| `gen_mask_border()` | 计算 Mask 边缘并叠加原图 |
| `getConnectedRegions()` | 连通域分析 → 转检测框 |
| `genImages()` | 生成完整可视化图像集 |
| `postProcess()` | 后处理主函数（整合以上所有步骤） |

### 8.2 `opencvUtils.h/.cpp`

| 函数 | 功能 |
|---|---|
| `Resize()` | 支持多种插值方式的缩放 |
| `Crop()` | 图像裁剪 |
| `Divide()` | 像素值归一化（0~255 → 0~1） |
| `Normalize()` | 均值-标准差归一化（含 BGR→RGB） |
| `Transpose()` | HWC → CHW 维度转置 |
| `Pad()` | 图像填充 |
| `Compare()` | 两幅图像比较 |

---

## 九、测试工程结构

测试项目 `A_testAlphaAnomaly` 与主项目 `AlphaAnomaly` 在解决方案管理器中并列、构建后出现在同级目录，这是三层机制协作的结果：

**1. `.sln` 注册了两个工程**

```xml
Project("...") = "AlphaAnomaly", "AlphaAnomaly.vcxproj", "{BF6C...}"
Project("...") = "A_testAnomaly", "test\test.vcxproj", "{C962...}"
```

**2. 工程名 ≠ .vcxproj 文件名**

`test.vcxproj` 中通过 `<ProjectName>A_testAlphaAnomaly</ProjectName>` 指定了产出名称，与物理文件名无关。

**3. 输出目录指向同一个文件夹**

| 工程 | `.vcxproj` 中的 OutDir | 产出 |
|---|---|---|
| AlphaAnomaly（DLL） | `../AlgDLLs/` | `AlphaAnomaly.dll` + `.lib`（导入库） |
| A_testAlphaAnomaly（EXE） | `../../AlgDLLs/` | `A_testAlphaAnomaly.exe` |

计算相对路径后，两个产出都落在 `AlgDLLs/` 目录中，所以看上去是"同级的"。

**4. 测试工程引用的 `AlphaAnomaly.h` 与主工程是同一份**

`test.vcxproj` 的 IncludePath 包含 `../app`（从 `test/` 目录上跳一级到根目录的 `app/`），所以 `#include "AlphaAnomaly.h"` 找到的是磁盘上唯一的 `app/AlphaAnomaly.h`。同一个头文件在两个编译语境中——DLL 工程定义了 `DLL_EXPORTS`，EXE 工程没有——分别走不同的 `dllexport/dllimport` 分支。

**5. `#pragma comment(lib, "AlphaAnomaly.lib")`**

`test/main.cpp` 顶部的这一行在 .obj 文件中嵌入一条链接器指令，等价于在工程属性 → 链接器 → 输入 → 附加依赖项里手工添加 `AlphaAnomaly.lib`。这个 .lib 文件不是普通静态库（只有几十 KB），而是 **Import Library（导入库）**——不包含函数代码，只包含一层跳板记录，告诉链接器"这些符号在 `AlphaAnomaly.dll` 里，去那里找"。运行时，Windows PE 加载器在 EXE 启动时找到 DLL、映射到进程地址空间、把函数地址填入 IAT（Import Address Table），完成最终链接。
### 9.1 主测试 (`test/main.cpp`)

批量测试框架，流程如下：

```
main()
  ├── 1. 初始化 AlphaAnomaly 实例
  ├── 2. 配置参数（模型路径、图像路径、阈值等）
  ├── 3. 遍历模型文件夹，对每个模型：
  │    ├── LoadModel()
  │    ├── (可选) 释放/重载测试
  │    ├── warmup()
  │    └── 遍历测试图像：
  │         ├── Predict()
  │         ├── postProcess()
  │         └── 保存可视化结果
  └── 4. 输出性能统计（平均推理时间）
```

支持功能：
- 白名单/黑名单模型过滤
- 反复释放重载测试
- GPU 预热
- 性能计时统计（跳过首张 warmup）
- 可视化结果分级保存到子目录

### 9.2 独立性能测试 (`test/model/main.cpp`)

另一套独立的基线测试，功能：
- 使用 `NVML` 监控 GPU 利用率
- 使用 `cudaMemGetInfo` 监控显存占用
- 分别支持 ORT 和 TRT 独立测试
- 统计平均延迟、FPS、GPU 显存增量、CPU 占用率

### 9.3 辅助工具

| 文件 | 功能 |
|---|---|
| `alphaTimer.h` | 基于 `chrono::high_resolution_clock` 的高精度计时器 |
| `testUtils.h` | 保存检测结果（6 种图像分目录保存）、文件遍历、日志追加 |

保存目录结构：
```
results/
├── 00_original/          # 原始图像
├── 01_mask/              # 二值 Mask
├── 02_border/            # 边缘轮廓
├── 03_superimposed/      # 全图叠加（含检测框）
├── 04_mask_heatmap/      # 异常区域热力图覆盖
└── 05_heatmap_color/     # 纯热力图
```

---

## 十、构建配置要点

### 10.1 主工程 (`AlphaAnomaly.vcxproj`)

| 配置项 | Debug | Release |
|---|---|---|
| 配置类型 | 应用 (.exe) | 动态库 (.dll) |
| 平台工具集 | v142 (VS2019) | v142 |
| CUDA | CUDA 11.4 | CUDA 11.4 |
| 输出目录 | (默认) | `../AlgDLLs/` |
| 预定义宏 | `WIN32;WIN64;_DEBUG;_CONSOLE` | `WIN32;WIN64;NDEBUG;_CONSOLE;DLL_EXPORTS` |
| C++标准 | (默认) | C++17 |
| 禁用警告 | — | `/wd4819 /wd4251 /wd4267 /wd4244` |

### 10.2 DLL 导出/导入机制详解

`ALPHA_DLL_EXPORTS` 宏是理解整个工程跨 DLL 调用链的关键。它定义在 `bohrtype.h` 中：

```cpp
#ifdef DLL_EXPORTS
    #define ALPHA_DLL_EXPORTS __declspec(dllexport)   // 编译 DLL 时：开门
#else
    #define ALPHA_DLL_EXPORTS __declspec(dllimport)   // 编译 EXE 时：搭跳板
#endif
```

**一个宏如何同时管两个工程？** 核心在于 `DLL_EXPORTS` 这个开关在两个 `.vcxproj` 中的定义状态不同：

| 工程 | 是否定义 `DLL_EXPORTS` | `ALPHA_DLL_EXPORTS` 展开为 |
|---|---|---|
| `AlphaAnomaly.vcxproj`（生成 DLL） | ✅ 是（Release 配置） | `__declspec(dllexport)` → 将符号发布到 DLL 导出表 |
| `test.vcxproj`（生成 EXE） | ❌ 否 | `__declspec(dllimport)` → 生成间接跳转指令 |

**到底是什么原理？** 完整调用链路如下：

```
阶段 1 — 编译时
  EXE 中用 dllimport 声明的函数调用 → 编译器生成"间接 call"（通过指针跳转），
  而非"直接 call"（写死地址）

阶段 2 — 链接时
  链接器在 EXE 的导入表（IAT, Import Address Table）中预留槽位，
  记录"需要 AlphaAnomaly.dll 的 LoadModel 符号"

阶段 3 — 加载时（运行时 main() 之前）
  Windows PE 加载器读取 EXE 的导入表 → 找到 AlphaAnomaly.dll →
  将其映射到进程地址空间 → 把 LoadModel 的地址填入 IAT 槽位

阶段 4 — 运行时
  call [IAT 槽位] → 通过跳板指针一跳进入 DLL 的函数体
```

**核心概念区分**：
- `__declspec(dllexport)` → 给 DLL 开门，函数符号写入导出表
- 不加导出宏 → 函数代码仍在 DLL 中，但没写入导出表，外部找不到入口
- `__declspec(dllimport)` → 给 EXE 搭跳板，编译器生成间接 call 指令
- 结构体不需要导出宏 → 结构体是纯数据布局协议，不涉及跨 DLL 的符号查找，调用方通过头文件知道内存布局即可

### 10.3 外部依赖

- OpenCV（通过 `C:\ProgramData\bohr\` 下的 props 文件配置）
- ONNX Runtime 1.12.1（Release 下导入）
- TensorRT 8.5.3.1（Release 下导入）
- CUDA 11.4（编译 CUDA 代码，sm_80 架构）
- AlphaCrypto 静态链接库

### 10.3 编译后事件

```powershell
powershell -ExecutionPolicy Bypass -File "$(ProjectDir)update_version_info.ps1"
```

自动更新版本信息到 `.rc` 资源文件。

---

## 十一、业务逻辑总结

### 端到端使用示例

```cpp
#include "AlphaAnomaly.h"
using namespace Alpha::Anomaly;

// 1. 创建检测器
AlphaAnomaly detector;

// 2. 加载模型（自动识别后端）
detector.LoadModel("model.alphaengine", BackendType::ONNX, true, 0, true);

// 3. 读取图像
cv::Mat image = cv::imread("test.jpg");

// 4. 推理
AnomalyResult result;
detector.Predict(image, result);

// 5. 后处理（获取业务信息和可视化）
AnomalyOutput output = postProcess(image, result, 0.5f, true);

// 6. 使用结果
std::cout << "异常得分: " << output.result.score << std::endl;
std::cout << "异常面积: " << output.info.anomalyArea << " 像素" << std::endl;
std::cout << "检测框数: " << output.info.boxes.size() << std::endl;

// 7. 查看可视化结果
cv::imshow("Mask", output.visuals.mask);
cv::imshow("Blended", output.visuals.blended);
```

### 关键设计决策

1. **双后端解耦**：通过抽象基类 `AnomalyBase` 隔离推理框架差异，新增后端只需继承该类
2. **模型加密保护**：自定义 `.alphaengine` 格式，打包 ORT/TRT 双模型，运行时按需解密
3. **延迟可视化**：`postProcess()` 的 `isVisual` 参数允许业务场景下跳过可视化生成以提高性能
4. **GPU 自动适配**：`AnomalyBase` 构造函数自动检测显卡数量，`checkGPUInfo()` 安全降级
5. **异步推理**：TRT 后端使用 CUDA Stream 实现异步 Host↔Device 传输 + 推理

---

## 十二、潜在扩展点

- **新增推理后端**：继承 `AnomalyBase`，实现纯虚接口，在 `createImpl()` 中注册
- **OpenVINO 支持**：`AlphaCrypto::ModelInfo` 已预留 `ovModel` 字段
- **动态 batch 推理**：`OrtAnomaly::Predicts` 目前是循环单张，可优化为批量张量推理
- **模型热更新**：`LoadModel()` 已内置 `m_impl.reset()` 逻辑，支持运行时切换模型
- **更多可视化风格**：可在 `anomalyUtil.cpp` 的 `genImages()` 中添加新可视化类型
- **远程推理**：抽象推理层后，可将 `Predict` 实现替换为 gRPC/REST 调用

---

*文档结束*






