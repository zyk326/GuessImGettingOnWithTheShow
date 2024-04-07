from torch import nn
import torch
import timm
import torch.nn.functional as F

class ConvNormAct(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, norm=None, act=None) -> None:
        super().__init__()
        self.conv = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride, padding=padding, dilation=dilation)
        self.norm = nn.Identity() if norm is None else norm(out_channels)
        self.act = nn.Identity() if act is None else act()

    def forward(self, x):
        x = self.conv(x)
        x = self.norm(x)
        x = self.act(x) 
        return x

class BasicBlock(nn.Module):
    def __init__(self, in_channels, out_channels, norm=None, act=None):
        super().__init__()
        self.conv1 = ConvNormAct(in_channels=in_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1, norm=norm, act=act)
        self.conv2 = ConvNormAct(in_channels=out_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1, norm=norm, act=act)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        return x
    
class UpBlock(nn.Module):
    def __init__(self, in_channels, out_channels, mid_channels=None, norm=None, act=None):
        super().__init__()
        mid_channels = in_channels if mid_channels is None else mid_channels
        self.up = nn.ConvTranspose2d(in_channels=in_channels, out_channels=out_channels, kernel_size=2, stride=2)
        self.conv = BasicBlock(in_channels=mid_channels, out_channels=out_channels, norm=norm, act=act)

    def forward(self, x, cat):
        x = self.up(x)
        x = torch.cat([x, cat], dim=1)
        x = self.conv(x)
        return x
    


class UNet(nn.Module):
    def __init__(self, in_channels, num_classes, channels=[64, 128, 256, 512, 1024], norm=nn.InstanceNorm2d, act=nn.ReLU) -> None:
        super().__init__()
        self.enc1 = BasicBlock(in_channels, channels[0], norm=norm, act=act)
        self.enc2 = BasicBlock(channels[0], channels[1], norm=norm, act=act)
        self.enc3 = BasicBlock(channels[1], channels[2], norm=norm, act=act)
        self.enc4 = BasicBlock(channels[2], channels[3], norm=norm, act=act)
        self.enc5 = BasicBlock(channels[3], channels[4], norm=norm, act=act)
        self.down = nn.MaxPool2d(2)
        self.dec4 = UpBlock(channels[4], channels[3], norm=norm, act=act)
        self.dec3 = UpBlock(channels[3], channels[2], norm=norm, act=act)
        self.dec2 = UpBlock(channels[2], channels[1], norm=norm, act=act)
        self.dec1 = UpBlock(channels[1], channels[0], norm=norm, act=act)
        self.out_conv = nn.Conv2d(channels[0], num_classes, 1, 1)

    def forward(self, x):
        x1 = self.enc1(x)
        x = self.down(x1)
        x2 = self.enc2(x)
        x = self.down(x2)
        x3 = self.enc3(x)
        x = self.down(x3)
        x4 = self.enc4(x)
        x = self.down(x4)
        x = self.enc5(x)
        x = self.dec4(x, x4)
        x = self.dec3(x, x3)
        x = self.dec2(x, x2)
        x = self.dec1(x, x1)
        x = self.out_conv(x)
        return x
    

class SEResUNet(nn.Module):
    def __init__(self, in_channels, num_classes, norm=nn.InstanceNorm2d, act=nn.ReLU) -> None:
        super().__init__()

        backbone = timm.create_model('seresnet50', pretrained=False)
        self.layer0 = nn.Sequential(
            nn.Conv2d(in_channels, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False),
            backbone.bn1,
            backbone.act1,
            
        )
        self.down = backbone.maxpool
        self.layer1 = backbone.layer1
        self.layer2 = backbone.layer2
        self.layer3 = backbone.layer3
        self.layer4 = backbone.layer4
        self.dec4 = UpBlock(2048, 1024, norm=norm, act=act)
        self.dec3 = UpBlock(1024, 512, norm=norm, act=act)
        self.dec2 = UpBlock(512, 256, norm=norm, act=act)
        self.dec1 = UpBlock(256, 64, 128, norm=norm, act=act)
        self.dec0 = UpBlock(64, 32, 32+in_channels)
        self.out_conv = nn.Conv2d(32, num_classes, 1, 1)
    

    def forward(self, inputs):
        x1 = self.layer0(inputs)
        x = self.down(x1)
        x2= self.layer1(x)
        x3 = self.layer2(x2)
        x4 = self.layer3(x3)
        x = self.layer4(x4)
        x = self.dec4(x, x4)
        x = self.dec3(x, x3)
        x = self.dec2(x, x2)
        x = self.dec1(x, x1)
        x = self.dec0(x, inputs)
        x = self.out_conv(x)
        return x


class Bottleneck(nn.Module):
    def __init__(self, in_channels, out_channels, stride, dilation, downsample, norm=None, act=None, BOTTLENECK_EXPANSION=4):
        super(Bottleneck, self).__init__()
        mid_channels = out_channels // BOTTLENECK_EXPANSION
        self.reduce = ConvNormAct(in_channels, mid_channels, 1, stride, 0, 1, norm=norm, act=act)
        self.conv3x3 = ConvNormAct(mid_channels, mid_channels, 3, 1, dilation, dilation, norm=norm, act=act)
        self.increase = ConvNormAct(mid_channels, out_channels, 1, 1, 0, 1, norm=norm, act=act)

        self.shortcut = (
            ConvNormAct(in_channels, out_channels, 1, stride, 0, 1, norm=norm, act=nn.Identity)
            if downsample
            else nn.Identity()
        )

    def forward(self, x):
        h = self.reduce(x)
        h = self.conv3x3(h)
        h = self.increase(h)
        h += self.shortcut(x)
        return F.relu(h)

class ResBlock(nn.Sequential):
    def __init__(self, num_layers, in_channels, out_channels, stride, dilation, multi_grids=None):
        super(ResBlock, self).__init__()

        if multi_grids is None:
            multi_grids = [1 for _ in range(num_layers)]
        else:
            assert num_layers == len(multi_grids)

        for i in range(num_layers):
            self.add_module(
                "block{}".format(i + 1),
                Bottleneck(
                    in_channels=(in_channels if i == 0 else out_channels),
                    out_channels=out_channels,
                    stride=(stride if i == 0 else 1),
                    dilation=dilation * multi_grids[i],
                    downsample=(True if i == 0 else False),
                ),
            )


class Pool(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.conv = ConvNormAct(in_channels, out_channels, 1, 1, 0, 1)

    def forward(self, x):
        _, _, H, W = x.shape
        h = self.pool(x)
        h = self.conv(h)
        h = F.interpolate(h, size=(H, W), mode="bilinear", align_corners=False)
        return h


class ASPP(nn.Module):
    def __init__(self, in_channels, out_channels, rates):
        super(ASPP, self).__init__()
        self.stages = nn.Module()
        self.stages.add_module("c0", ConvNormAct(in_channels, out_channels, 1, 1, 0, 1))
        for i, rate in enumerate(rates):
            self.stages.add_module(
                "c{}".format(i + 1),
                ConvNormAct(in_channels, out_channels, 3, 1, padding=rate, dilation=rate),
            )
        self.stages.add_module("imagepool", Pool(in_channels, out_channels))

    def forward(self, x):
        return torch.cat([stage(x) for stage in self.stages.children()], dim=1)


class DeepLabV3(nn.Sequential):
    def __init__(self, in_channels, num_classes, n_blocks, atrous_rates, multi_grids, output_stride, input_size):
        super(DeepLabV3, self).__init__()

        if output_stride == 8:
            s = [1, 2, 1, 1]
            d = [1, 1, 2, 4]
        elif output_stride == 16:
            s = [1, 2, 2, 1]
            d = [1, 1, 1, 2]

        ch = [64 * 2 ** p for p in range(6)]
        self.add_module("layer1", nn.Sequential(
            ConvNormAct(in_channels, ch[0], 7, 2, 3, 1),
            nn.MaxPool2d(3, 2, 1, ceil_mode=True)))

        self.add_module("layer2", ResBlock(n_blocks[0], ch[0], ch[2], s[0], d[0]))
        self.add_module("layer3", ResBlock(n_blocks[1], ch[2], ch[3], s[1], d[1]))
        self.add_module("layer4", ResBlock(n_blocks[2], ch[3], ch[4], s[2], d[2]))
        self.add_module(
            "layer5", ResBlock(n_blocks[3], ch[4], ch[5], s[3], d[3], multi_grids)
        )
        self.add_module("aspp", ASPP(ch[5], 256, atrous_rates))
        concat_ch = 256 * (len(atrous_rates) + 2)
        self.add_module("fc1", ConvNormAct(concat_ch, 256, 1, 1, 0, 1))
        self.add_module("fc2", nn.Conv2d(256, num_classes, kernel_size=1))
        self.add_module("upsample", nn.UpsamplingBilinear2d(size=input_size))




if __name__ == '__main__':
    # model = UNet(7, 3).cuda()
    model = SEResUNet(7, 3).cuda()
    # model = DeepLabV3(
    #     in_channels=7, 
    #     num_classes=3, 
    #     n_blocks=[3, 4, 23, 3],
    #     atrous_rates=[6, 12, 18],
    #     multi_grids=[1, 2, 4],
    #     output_stride=8,
    #     input_size=(256, 256)).cuda()
    from torchsummary import summary
    summary(model, (7, 256, 256), 1, 'cuda')