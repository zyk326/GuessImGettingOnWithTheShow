# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from torch.optim import Adam
# from torch.utils.data import DataLoader, Dataset
# from torchvision import transforms, datasets

# batch_size = 32
# epoches = 100
# lr = 0.001

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
#         x = torch.flatten(x)
#         x = F.relu(self.fc1(x))
#         x = torch.sigmoid(self.fc2(x))
#         return x

# transform = transforms.Compose([
#     transforms.Resize((64, 64)),
#     transforms.ToTensor()
# ])

# train_data = datasets.ImageFolder(root='./train_data', transform=transform)
# train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

# test_data = datasets.ImageFolder(root='/test_data', transform=transform)
# test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

# model = Net()
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model = model.to(device)

# cirterion = nn.BCELoss()
# optimizer = Adam(model.parameters(), lr=lr)

# for epoch in range(epoches):
#     model.train()
#     train_loss = 0.0
#     for images, labels in train_loader:
#         images, labels = images.to(device), labels.to(device).float()
#         labels = labels.unsqueeze(1)

#         optimizer.zero_grad()
#         outputs = model(images)
#         loss = criterion(outputs, labels)
#         loss.backward()
#         optimizer.step()
#         train_loss += loss.item()
#     print(f"Epoch[{epoch+1}/{epoches}], Loss:{train_loss/len(train_loader):.4f}")


# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from torch.utils.data import DataLoader, Dataset
# from torchvision import transforms, datasets
# from torch.optim import Adam

# epoches = 100
# batch_size = 32
# learn_rate = 0.001

# class Net(nn.Module):
#     def __init__(self):
#         super(Net, self).__init__()
#         self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1)
#         self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
#         self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
#         self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
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

# test_data = datasets.ImageFloader(root='./test_data', transform=transform)
# test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

# model = Net()
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model = model.to(device)

# criterion = nn.BCELoss()
# optimizer = torch.nn.Adam(model.parameters(), lr=learning_rate)

# for epoch in range(epoches):
#     model.train()
#     train_loss = 0.0
#     for images, labels in train_loader:
#         images, labels = images.to(device), labels.to(device).float()
#         labels = labels.unsqueeze(1)

#         optimizer.zero_grad()
#         output = model(images)
#         loss = criterion(output, labels)
#         train_loss += loss.item()
#         loss.backward()
#         optimizer.step()
#     print(f"Epoch[{epoch+1}/{epoches}, Loss:{train_loss/len(train_loader):.4f}]")

# model.eval()
# correct = 0
# total = 0

# with torch.no_grad():
#     for images, labels in test.loader:
#         images, labels = images.to(device), labels.to(device).float()
#         labels.unsqueeze(1)
#         outputs = model(images)
#         predictd = (outputs > 0.5).float()
#         total += labels.size(0)
#         correct += (predicted).sum().item()

# print(f"Accuray:{correct/total:.4f}")

import torch 
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data import DataLoader, Dataset
from torchvision import transforms, datasets

eposhes = 100
learning_rate = 0.001
batch_size = 32

def Net(nn.Module):
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
        x = torch.faltten(x, 1)
        x = F.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor()
])

train_data = datasets.ImageFolder(root='./train_data', transform=transform)
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

test_data = datasets.ImageFolder(root='/test_data', transform=transform)
test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

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
    print(f"Epoch[{epoch+1/epoches}, Loss:{train_loss/len(train_loader):.4f}]")

model.eval()
total = 0
corret = 0

for images, labels in test_loader:
    images, labels = images.to(device), labels.to(device)
    labels = labels.unsqueeze(1)
    output = model(images)
    predicted = (output > 0.5).float()
    total += labels.size(0)
    corret += (predicted == labels).sum().item()
print(f"Accuracy:{correct/total:.4f}")