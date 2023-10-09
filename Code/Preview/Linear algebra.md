```
import torch

x = torch.tensor(3.0)
y = torch.tensor(2.0)

print(x + y, x * y, x / y, x ** y)

z = torch.arange(20).reshape(4, 5)
print(z)
z = z.T
print(z)

print(z.sum())

a = torch.ones([2, 4, 5])
print(a.shape)
print(a)

print(a.sum(axis = [0,2], keepdim=True))
```

tensor(5.) tensor(6.) tensor(1.5000) tensor(9.)    
tensor([[ 0,  1,  2,  3,  4],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 5,  6,  7,  8,  9],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[10, 11, 12, 13, 14],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[15, 16, 17, 18, 19]])  
tensor([[ 0,  5, 10, 15],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 1,  6, 11, 16],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 2,  7, 12, 17],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 3,  8, 13, 18],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 4,  9, 14, 19]])  
tensor(190)  
torch.Size([2, 4, 5])  
tensor([[[1., 1., 1., 1., 1.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[1., 1., 1., 1., 1.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[1., 1., 1., 1., 1.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[1., 1., 1., 1., 1.]],    
&emsp;&emsp;&emsp;&nbsp;&nbsp;[[1., 1., 1., 1., 1.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[1., 1., 1., 1., 1.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[1., 1., 1., 1., 1.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[1., 1., 1., 1., 1.]]])    
tensor([[[10.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[10.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[10.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[10.]]])