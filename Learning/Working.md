# Yolo项目-垒石石墨卷

## 前置内容
pycharm，anoconda，git  

### nvidia环境配置  

nvidia-smi (查看GPU)(linux)  
```
@echo off
:loop
cls
nvidia-smi
timeout /t 1 >nul
goto loop
```
^←windows，bat文件内容  

### 实施步骤  
1. 数据集分割  
2. git下载yolov12，安装torch以及依赖包  

## 你的训练日志位置：  
主要日志目录：**runs/detect/train12/**  
训练结果：**runs/detect/train12/results.csv** - 包含每个epoch的详细指标  
模型权重：**runs/detect/train12/weights/** - 包含 best.pt 和 last.pt  
训练参数：**runs/detect/train12/args.yaml** - 记录所有训练配置  
查看 **runs/detect/train12/weights/best.pt** 获取当前最佳模型。  


## 部署的前置要求  
1. pt转ort转trt(他们的关系，含义，转换方法)  
2. 安CUDA  **C:\Users\Administrator\AppData\Local\Temp\cuda**   
3. 安cudnn 
4. 使用训练脚本训练模型，拿官方的直接转ort，使用trtexec来ort转换trt  
5. 使用trtexec需要TensorRT，到官网安装  
6. 编onnxruntime库，用c++   
7. 需要知道模型部署时，模型的训练方式是seg还是det    
8. visual studio需要修改VC++目录和链接器中的输入    

##  试运行总结
1. 在visual studio里配置库的链接  

```
包含放包含，库放库（路径）

在链接器里放对应的lib
opencv_world460.lib
onnxruntime.lib
```

2. cuda和cudnn的版本要匹配，如果出现内存错误的问题，看控制台，大概率是版本没有匹配  

## 打包DLL
1. 添加宏，添加include，添加lib，添加链接器中输入的附加依赖项。  

#ifdef YOLOV11SEG_EXPORTS  
#define YOLO_API __declspec(dllexport)  
#else  
#define YOLO_API __declspec(dllexport)  

在类前加class YOLO_API YOLOV11Seg{}  

生成即可。  

2. 在使用dll的时候，要添加链接器，包括  
常规：添加库目录（lib path）  
输入：附加依赖项（.lib）   
也就是说，lib是一个函数内容的索引，dll是一个包含函数内容的文件。  
lib可以放在别处，用添加库目录和依赖项的方式找到它，而dll最好是放在exe同路径下。    

# 训练曲线说明  

## 看两张图  
### F1-Confidence  
置信控制过杀，漏检。    
置信降低，过杀控制不住。  
置信升高，漏检控制不住。  

### Instance  
看缺陷的分布情况，数据平衡。   

# BOHR DFM设计文档  

## 划分模型秘籍  
主要看检测区域设计部分，在那里有主要的检测内容，包括以下内容：  

光源信息  
拍照点  
拍照图片数量  
产品移动数量  
拍照+存储耗时  
Station condition的详细说明  

使用多个station的信息，来判断模型合并的可能性。  
一看光源，光源一样，那么成像就有一致的可能性。  
二看检测类型，缺陷类型一样，且光源一样，那么就有缺陷成像一致的可能性；如果光源不一样而缺陷类型一样，成像一致性不能保证，一定不能合并。    
三看图片尺寸（很有说法），图片尺寸接近有合并的可能性。   

使用DFM的标定最小NG尺寸来计算图片中的缺陷区域大小，使用每个图片的单像素精度计算缺陷像素块个数，使用缺陷像素块计算缩放后像素块个数，缩放后像素块不能低于9个。   

划分模型更像是一个工程定量的过程，是接下来的模型训练的总体方针，为待处理数据划定不同的处理方式，细化处理过程，落定到每个资源上。所以划分讲究合理性，资源承接性，任务量充实性，训练可行性。  

