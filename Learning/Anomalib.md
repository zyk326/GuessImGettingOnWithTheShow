# 这是Anomalib平台C++、onnx、trt、openvino部署的笔记

### 环境搭建说明

**一个visual studio2019、下载好的onnx（分CPU，GPU版）库、下载好的opencv库**

在工程属性中添加opencv和onnx：

=》VC++目录 =》包含目录 =》添加-/opencv/build/include

=》VC++目录 =》库目录 =》添加-/opencv/build/x64/vc15/lib

=》链接器 =》附加依赖项 =》opencv_world460.lib

=》VC++目录 =》包含目录 =》添加-/onnxruntime-win-x64/include

=》VC++目录 =》库目录 =》添加-/onnxruntime-win-x64/lib

=》链接器 =》输入 =》附加依赖项 =》onnxruntime.lib;onnxruntime_providers_shared.lib

=》复制onnxruntime.dll、onnxruntime_providers_shared.dll、opencv_world460.dll到C++工程/x64/Release下

完成环境搭建，即可开始编写C++代码。



### 工程大小的调优

**处理visual studio的.vs的空间占用太大的问题**
在导航栏：
=》工具 =》选项 =》文本编辑器 =》C/C++ =》高级 =》回退位置
=》始终使用回退位置 =》True
=》回退位置已在使用时，不警告 =》true
=》回退位置 =》找一个临时目录，随时删除



### C++编写说明

**整体采用PImpl设计模式**



1.各个onnx模型的跑通测试。

3.trt的版本，openvino的版本。

4.c++的基础。