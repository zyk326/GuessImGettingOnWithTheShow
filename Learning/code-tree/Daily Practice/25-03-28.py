def qk_sort(nums, left, right):
    if left >= right:
        return
    l, r = left, right
    while l != r:
        while l < r and nums[left] <= nums[r]:
            r -= 1
        while l < r and nums[left] > nums[l]:
            l += 1
        if l < r:
            nums[l], nums[r] = nums[r], nums[l]
    nums[left], nums[l] = nums[l], nums[left]
    qk_sort(nums, left, l - 1)
    qk_sort(nums, l + 1, right)
    return nums
print(qk_sort([3,2,6,4,9,0,1], 0, 6))

import torch 
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision import transforms, datasets

batch_size = 32
learning_rate = 0.001
epoches = 100

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(128*8*8, 128)
        self.fc2 = nn.Linear(128, 1)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = torch.sigmoid(fc2(x))
        return x

transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor()
])

train_data = datasets.ImageFolder(root='./train_data', transform=transform)
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

test_data = datasets.ImageFolder(root='/test_data', transform=transform)
train_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

model = Net()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

criterion = nn.BCELoss()
optimizer = Adam(model.parameters(), lr=learning_rate)

for epoch in range(epoches):
    model.train()
    train_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device).float()
        labels = labels.unsqueeze(1)

        optimizer.zero_grad()
        output = model(images)
        loss = criterion(output, labels)
        train_loss += loss.item()
        loss.backward()
        optimizer.step()
    print(f'Eopch[{epoch+1/epoches}], Loss:{train_loss/len(train_loader)}')

model.eval()
total = 0
ac = 0

for images, labels in test_loader:
    images , labels = images.to(device), labels.to(device).float()
    labels = labels.unsqueeze(1)

    output = model(images)
    predicted = (output > 0.5).float()
    total += labels.item().size(0)
    ac += (labels == predicted).sum()
print(f'ac is{ac/total:.4f}')