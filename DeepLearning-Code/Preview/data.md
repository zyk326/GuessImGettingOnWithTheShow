```
import torch

x = torch.arange(12)
```
tensor([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11])
```
print(x.shape)
```
torch.Size([12])

### number of element
```
print(x.numel())
```
12    
```
x.reshape(3, 4)
```
tensor([[ 0,  1,  2,  3],   
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 4,  5,  6,  7],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 8,  9, 10, 11]])  
```
y = torch.zeros((2, 3, 4))
```
tensor([[[0., 0., 0., 0.],   
&emsp;&emsp;&emsp;&nbsp;&nbsp;[0., 0., 0., 0.],    
&emsp;&emsp;&emsp;&nbsp;&nbsp;[0., 0., 0., 0.]],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[[0., 0., 0., 0.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[0., 0., 0., 0.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[0., 0., 0., 0.]]])
```
z = torch.ones((2, 3, 4))
```
tensor([[[1., 1., 1., 1.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[1., 1., 1., 1.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[1., 1., 1., 1.]],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[[1., 1., 1., 1.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[1., 1., 1., 1.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[1., 1., 1., 1.]]])

### the element number of outside to inside   
```
k = torch.tensor([[[2,1,3], [5,6,4]],[[2,6,4],[2,3,6]]])  
```
tensor([[[2, 1, 3],   
&emsp;&emsp;&emsp;&nbsp;&nbsp;[5, 6, 4]],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[[2, 6, 4],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[2, 3, 6]]])


### exp(x) = e^x
```
torch.exp(k)
```
tensor([[[  7.3891,   2.7183,  20.0855],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[148.4132, 403.4288,  54.5981]],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[[  7.3891, 403.4288,  54.5981],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[  7.3891,  20.0855, 403.4288]]])
### cat : merge with dim = ? , which lay to merge by the number with outside to inside 
```
x = torch.arange(12, dtype = torch.float32).reshape((3, 4))
y = torch.tensor([[1.0,2,5,6],[1,2,3,4],[4,5,6,7]])
z = torch.cat((x, y), dim = 0)
```
tensor([[ 0.,  1.,  2.,  3.],   
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 4.,  5.,  6.,  7.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 8.,  9., 10., 11.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 1.,  2.,  5.,  6.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 1.,  2.,  3.,  4.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 4.,  5.,  6.,  7.]])
```
z = torch.cat((x, y), dim = 1)
```
tensor([[ 0.,  1.,  2.,  3.,  1.,  2.,  5.,  6.],   
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 4.,  5.,  6.,  7.,  1.,  2.,  3.,  4.],  
&emsp;&emsp;&emsp;&nbsp;&nbsp;[ 8.,  9., 10., 11.,  4.,  5.,  6.,  7.]])


### the sum of the elements in x
```
print(x.sum())
```
tensor(66.)

### create a document named test.csv at ./src,then write content to ./src/test.csv
```
import os

os.makedirs(os.path.join('.', 'src',), exist_ok=True)
data_file = os.path.join('.', 'src', 'test.csv') # Comma-Separated Values
with open(data_file, 'w') as f:
    f.write('NumRooms,Alley,Price\n')
    f.write('NA,Pave,127500\n')
    f.write('2,NA,106000\n')
    f.write('4,NA,178100\n')
    f.write('NA,NA,140000\n')
```
### format the data
```
import pandas as pd

data = pd.read_csv('./src/test.csv')
print(data)

inputs, inputs1, outputs = data.iloc[:, 0], data.iloc[:,1], data.iloc[:, 2]

inputs = inputs.fillna(inputs.mean())
print(inputs)

inputs1 = pd.get_dummies(inputs1, dummy_na = True, dtype=int)
print(inputs1)

import torch
X, y, z = torch.tensor(inputs.values), torch.tensor(inputs1.values), torch.tensor(outputs.values)
X, y, z
```
&emsp;NumRooms&emsp;Alley&emsp;Price  
0&emsp;&emsp;NaN&emsp;&emsp;Pave&emsp;&emsp;127500  
1&emsp;&emsp;2.0&emsp;&emsp;NaN&emsp;&emsp;106000  
2&emsp;&emsp;4.0&emsp;&emsp;NaN&emsp;&emsp;178100    
3&emsp;&emsp;NaN&emsp;&emsp;NaN&emsp;&emsp;140000    

0&emsp;&emsp;3.0  
1&emsp;&emsp;2.0   
2&emsp;&emsp;4.0  
3&emsp;&emsp;3.0    

Name: NumRooms, dtype: float64  

&emsp;Pave&emsp;NaN  
0&emsp;1&emsp;&emsp;0  
1&emsp;0&emsp;&emsp;1  
2&emsp;0&emsp;&emsp;1  
3&emsp;0&emsp;&emsp;1  

(tensor([3., 2., 4., 3.], dtype=torch.float64),

 tensor([[1, 0],  
&emsp;&emsp;&emsp;[0, 1],  
&emsp;&emsp;&emsp;[0, 1],  
&emsp;&emsp;&emsp;[0, 1]], dtype=torch.int32),  

 tensor([127500, 106000, 178100, 140000]))  