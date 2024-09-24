# 这里是PyTorch入门  

[用一个分类的模型来说明PyTorch和代码结构](https://www.bilibili.com/video/BV1zfp4eoEAy/?share_source=copy_web&vd_source=9f676f17c5917ccaa93f01729ffd0b8e)

统一用conda来管理环境.  
使用**conda info -e**来查看当前conda管理的环境.  
使用**torch.cuda.is_available()**查看cuda的可用状态.  

使用conda ： **conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia**来安装torch.  
删除conda虚拟环境 ： **conda env remove -n d2l-zh **.  

代码中一些没有返回值的.()动作大概率是将xx置于.xx()状态.  

with torch.no_grad():上下文管理器,让推理过程不改变模型参数,对中间的代码进行限制.  

优化器optm部分的逻辑:我先把模型中可以学习的参数拿到,然后调用优化器并把这些参数传给优化器,这样一个优化逻辑就完成了.   

loss.backword实际上是对损失求导.  

optimizer.step()是对优化器进行更新. 

一轮epoch可以有很多组数据,这取决于dataloader.  