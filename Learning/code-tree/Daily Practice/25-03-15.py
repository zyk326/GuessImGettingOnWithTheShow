
# 代码
# 测试用例
# 测试结果
# 测试结果
# 3340. 检查平衡字符串
# 简单
# 相关标签
# 相关企业
# 给你一个仅由数字 0 - 9 组成的字符串 num。如果偶数下标处的数字之和等于奇数下标处的数字之和，则认为该数字字符串是一个 平衡字符串。

# 如果 num 是一个 平衡字符串，则返回 true；否则，返回 false。

 

# 示例 1：

# 输入：num = "1234"

# 输出：false

# 解释：

# 偶数下标处的数字之和为 1 + 3 = 4，奇数下标处的数字之和为 2 + 4 = 6。
# 由于 4 不等于 6，num 不是平衡字符串。
# 示例 2：

# 输入：num = "24123"

# 输出：true

# 解释：

# 偶数下标处的数字之和为 2 + 1 + 3 = 6，奇数下标处的数字之和为 4 + 2 = 6。
# 由于两者相等，num 是平衡字符串。
 

# 提示：

# 2 <= num.length <= 100
# num 仅由数字 0 - 9 组成。

# num = input()
# lenum = len(num)
# a1 = a2 = 0
# for i in range(0, lenum, 2):
#     a1 += int(num[i])
# for i in range(1, lenum, 2):
#     a2 += int(num[i])
# print(a1 == a2)


#-------------快速排序--------------------------------
# def qk_sort(nums, left, right):
#     if left >= right:
#         return
#     l, r = left, right
#     while l != r:
#         while (l < r and nums[left] <= nums[r]):
#             r -= 1
#         while (l < r and nums[left] > nums[l]):
#             l += 1
#         if l < r:
#             nums[l], nums[r] = nums[r], nums[l]
#     nums[left], nums[l] = nums[l], nums[left]
#     qk_sort(nums, left, l - 1)
#     qk_sort(nums, l + 1, right)
#     return nums

# print(qk_sort([3,2,6,8,3,1,4,6], 0, 7))


#--------------前缀和---------------------------
# nums = [3,2,6,8,3,1,4,6]
# fr_nums = [nums[0]]
# for i in range(1, len(nums)):
#     fr_nums.append(nums[i] + fr_nums[i - 1])
# print(fr_nums)
# print(fr_nums[5] - fr_nums[2])

# def qk_sort(nums, left, right):
#     if left >= right:
#         return 
#     l, r = left, right
#     while(l != r):
#         while(l < r and nums[left] <= nums[r]):
#             r -= 1
#         while(l < r and nums[left] > nums[l]):
#             l += 1
#         if l < r:
#             nums[l], nums[r] = nums[r], nums[l]
#     nums[left], nums[l] = nums[l], nums[left]
#     qk_sort(nums, left, l - 1)
#     qk_sort(nums, l + 1, right)
#     return nums
# print(qk_sort([3,6,3,4,7,8,2,7,5,9], 0, 9))

SVM的核心思想是通过找到一个超平面，将数据分为不同类别，并最大化支持向量到超平面之间的间隔。为了处理非线性问题，SVM使用核函数将低维数据映射到高维空间，使得在高维空间中数据线性可分。

# import torch.nn as nn
# import torch.nn.functional as F
# import torch
# from torchvision import transforms, datasets
# from torch.utils.data import DataLoader, Dataset

# batch_size = 32
# learn_rate = 0.001
# epoch = 100

# class CNN(nn.Module):
#     def __init__(self):
#         super(CNN, self).__init__()
#         self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1)
#         self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
#         self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
#         self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
#         self.fc1 = nn.Linear(128*8*8, 128)
#         self.fc2 == nn.Linear(128, 1)
    
#     def forward(self, x):
#         x = self.pool(F.relu(self.conv1(x)))
#         x = self.pool(F.relu(self.conv2(x)))
#         x = self.pool(F.relu(self.conv3(x)))
#         x = torch.flatten(x, 1)
#         x = F.relu(self.fc1(x))
#         x = torch.sigmoid(self.fc2(x))
#         return x

# transform = transforms.Compose([
#     transforms.Resize((64, 64)),
#     transforms.ToTensor()
# ])

# train_dataset = datasets.ImageFolder(root='./train_data', transform=transform)
# train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# test_dataset = datasets.ImageFolder(root='./test_data', transform=transform)
# test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# model = CNN()
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model = model.to(device)

# criterion = nn.BCELoss()
# optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# for epoch in range(epoch):
#     model.train()
#     running_loss = 0.0
#     for images, labels in train_loader:
#         images, labels = images.to(device), labels.to(device).float()
#         labels = labels.unsqueeze(1)

#         optimizer.zero_grad()
#         output = model(images)
#         loss = criterion(output, labels)
#         loss.backward()
#         optimizer.step()
#         running_loss += loss.item()
#     print(f'Epoch [{epoch + 1}/{epochs}], Loss:{running_loss/len(train_loader):.4f}')

# model.eval()
# correct = 0
# total = 0

# with torch.no_grad():
#     for images, labels in test_loader:
#         images, labels = images.to(device), labels.to(device).float()
#         labels = labels.unsqueeze(1)
#         output = model(images)
#         prediced = (output > 0.5).float()
#         total += labels.size(0)
#         correct += (predicted == labels).sum().item()

# print(f'Accuracy:{correct / total:.4f}')

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from torchvision import datasets, transforms
# from torch.utils.data import DataLoader

# batch_size=32
# learning_rate = 0.001
# epochs=100

# class CNN(nn.Model):
#     def __init__(self):
#         super.__init__(self, CNN)
#         self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1)
#         self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
#         self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
#         self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
#         self.fc1 = nn.Linear(128*8*8, 128)
#         self.fc2 = nn.Linear(128, 1)

#     def forward(self, x):
#         x = self.pool(F.relu(self.conv1(x)))
#         x = self.pool(F.relu(self.conv2(x)))
#         x = self.pool(F.relu(self.conv3(x)))
#         x = torch.flatten(x, 1)
#         x = F.relu(self.fc1(x))
#         x = torch.sigmoid(self.fc2(x))
#         return x

# transform = transforms.Compose([
#     transfroms.Resize((32,32)),
#     transforms.ToTensor()
# ])

# train_dataset = datasets.Imagefloder(root='./train_data', transform=transform)
# train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# test_dataset = datasets.Imagefloder(root='./test_datat', transform=transform)
# test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# model = CNN()
# device = torch.device('cuda' if torch.cuda.is_avaliable() else 'cpu')
# model = model.to(device)

# criterion = nn.BCELoss()
# optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# for epoch in range(epochs):
#     model.train()
#     running_loss = 0.0
#     for images, labels in train_loader:
#         images, labels = images.to(device), labels.to(device).float()
#         labels.unsqueeze(1)

#         optimizer.zero_grad()
#         output = model(images)
#         loss = criterion(output, images)
#         loss.backward()
#         optimizer.step()
#         running_loss += loss.item()
#     print(f'Epoch[{epoch+1}/{epochs}], Loss:{running_loss/len(train_loader):.4f}')

# model.eval()
# correct = 0
# total = 0

# with torch.no_grad():
#     for images, labels in test_loader:
#         images, labels = images.to(device), labels.to(device).float()
#         labels.unsqueeze(1)

#         output = model(images)
#         predicted = (output > 0.5).float()
#         total += labels.size(0)
#         correct += (predicted == lables).sum().item()
# print(f'Accuracy:{correct / total:.4f}')

# import pandas as pd

# data = pd.read_csv('dataset.csv')

# column_data = data['target_column'].fillna(data['target_column'].mean())

# scaler = MinMaxScaler()
# normalized_data = scaler.fit_transform(column_data.values.reshape(-1,1))

# print(normalized_data)


import pandas as pd
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv('./dataset.csv')

column_data = data['target_column'].fillna(data['target_column'].mean())

scaler = MinMaxScaler()
normalized_data = scaler.fit_transform(column_data.value.reshape(-1, 1))


SELECT product_id, COUNT(*) AS purchase_count FROM purchase GROUP BY product_id ORDER BY purchase_count DESC LIMIT 5;