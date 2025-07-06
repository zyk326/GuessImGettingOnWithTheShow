# import torch 
# import torch.nn as nn
# import torch.nn.functional as F
# from torch.utils.data import DataLoader
# from torchvision import datasets, transfroms
# from torch.optim import Adam

# batch_size = 32
# learn_rate = 0.001
# epoches = 100

# class Net(nn.Module):
#     def __init__(self):
#         super(Net, self).__init__()
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
#     transforms.Resize((64, 64)),
#     transforms.ToTensor()
# ])

# train_data = datasets.ImageFolder(root='./train_data', transform=transform)
# train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

# test_data = datasets.ImageFolder(root='./test_data', transform=transform)
# test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

# model = Net()
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model = model.to(device)

# criterion = nn.BCELoss()
# optimizer = Adam(model.parameter(), lr=learn_rate)

# for epoch in range(epoches):
#     model.train()
#     train_loss = 0.0
#     for images, labels in train_loader:
#         images, labels = images.to(device), labels.to(device).float()
#         labels = labels.unqueeze(1)

#         optimizer.zero_grad()
#         output = model(images)
#         loss = criterion(output, labels)
#         train_loss += loss.item()
#         loss.backward()
#         optimizer.step()
#     print(f'Epoch:[{epoch+1/epoches}], Loss:{train_loss/len(train_loader):.4f}')

# model.eval()
# total = 0
# ac = 0
# with torch.no_grad():
#     for images, labels in test_loader:
#         images, labels = images.to(device), labels.to(device).float()
#         labels = labels.unsqueeze(1)

#         output = model(images)
#         predicted = (output > 0.5).float()
#         total += labels.item().size(0)
#         ac += (predicted == labels).sum()
#     print(f'ac is {ac/total:.4f}')


# def qk_sort(nums, left, right):
#     if left >= right:
#         return
#     l, r = left, right
#     while l != r:
#         while(l < r and nums[r] >= nums[left]):
#             r -= 1
#         while(l < r and nums[l] < nums[left]):
#             l += 1
#         if l < r:
#             nums[l], nums[r] = nums[r], nums[l]
#     nums[left], nums[l] = nums[l], nums[left]
#     qk_sort(nums, left, l - 1)
#     qk_sort(nums, l + 1, right)
#     return nums

# print(qk_sort([4,2,1,3,7,4,6], 0, 6))