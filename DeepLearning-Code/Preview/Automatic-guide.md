### Code view
```
import torch

x = torch.arange(4.0)
print(x)

x.requires_grad_(True) # 设置把x的梯度保存下来,y关于x的导数是放在这里的
print(x.grad)

y = 2 * torch.dot(x, x)
y.backward() #调用反向传播函数,意思是给你求个导
print(x.grad == 4 * x)

# x.grad.zero_() #下划线表示重写里面的内容 这里没有累计梯度,直接用会报错
y = x.sum()
y.backward()  
print(x.grad) #x.gard 是x的导数,对x求导

x.grad.zero_()
y = x * x # 这里乘出来是一个矩阵,下一行用sum就成了一个向量
y.sum().backward()
print('----  ',x.grad)

x.grad.zero_()
y = x * x
u = y.detach() # 把y当做一个常数,丢掉y跟x的函数关系,用u保存
z = u * x
z.sum().backward()    
print(x.grad == u) # z对x求导结果是常数u

def f(a):
    b = a * 2
    while b.norm() < 1000:
        b = b * 2
    if b.sum() > 0:
        c = b
    else:
        c = 100 * b
    return c

a = torch.randn(size = (), requires_grad=True)
d = f(a)
d.backward()

print(a.grad == d / a) # d是一个加系数的a的函数,记作k,则d = k * a,显然对a求导就是 d / a
```

tensor([0., 1., 2., 3.])  
None  
tensor([True, True, True, True])  
tensor([ 1.,  5.,  9., 13.])  
----   tensor([0., 2., 4., 6.])  
tensor([True, True, True, True])  
tensor(True)  