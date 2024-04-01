import argparse
import datetime
import os
import time
from logging import DEBUG, INFO, basicConfig, getLogger

import torch
import torch.optim as optim
import cv2
from albumentations import Compose, HorizontalFlip, Normalize, RandomResizedCrop, Resize
from albumentations.pytorch import ToTensorV2

import wandb
from libs.checkpoint import resume_BEDSRNet, save_checkpoint_BEDSRNet
from libs.config import get_config
from libs.dataset import get_dataloader
from libs.device import get_device
from libs.helper_bedsrnet import evaluate, train
from libs.logger import TrainLoggerBEDSRNet
from libs.loss_fn import get_criterion
from libs.models import get_model
from libs.seed import set_seed

logger = getLogger(__name__)


# 定义从命令行获取数据
def get_arguments() -> argparse.Namespace:  
    """parse all the arguments from command line inteface return a list of
    parsed arguments."""

    parser = argparse.ArgumentParser(
        description="""
        train a network for image classification with Flowers Recognition Dataset.
        """
    )
    parser.add_argument("config", type=str, help="path of a config file")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Add --resume option if you start training from checkpoint.",
    )
    parser.add_argument(
        "--use_wandb",
        action="store_true",
        help="Add --use_wandb option if you want to use wandb.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Add --debug option if you want to see debug-level logs.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="random seed",
    )

    return parser.parse_args()


def main() -> None: # ->表示返回值为None
    args = get_arguments()

    # save log files in the directory which contains config file.
    result_path = os.path.dirname(args.config)
    experiment_name = os.path.basename(result_path)

    # setting logger configuration
    logname = os.path.join(result_path, f"{datetime.datetime.now():%Y-%m-%d}_train.log")
    
    basicConfig(
        level=DEBUG if args.debug else INFO,
        format="[%(asctime)s] %(name)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=logname,
    )

    # fix seed
    set_seed()

    # configuration
    config = get_config(args.config)

    # cpu or cuda
    device = get_device(allow_only_gpu=False)

    # Dataloader 数据增强
    train_transform = Compose(
        [
            RandomResizedCrop(config.height, config.width), # 随机裁剪并重新调整大小。
            HorizontalFlip(),                               # 水平翻转。
            Normalize(mean=(0.5,), std=(0.5,)),             # 归一化操作，设置均值为0.5，标准差为0.5。
            ToTensorV2(),                                   # 将数据转换为张量格式。
        ]
    )

    # 测试集
    val_transform = Compose(
        [
            Resize(config.height, config.width),
            Normalize(mean=(0.5,), std=(0.5,)),
            ToTensorV2(),
        ]
    )

    train_loader = get_dataloader(
        config.dataset_name,
        config.model,
        "train",
        batch_size=config.batch_size,
        shuffle=True,       # 打乱数据集
        num_workers=config.num_workers, # num越大,加快从RAM中找batch的速度,缺点是会加重cpu负担
        pin_memory=True,  # 把tensor放入锁页区,加快训练速度
        drop_last=True,     # 控制保存不完整的批次
        transform=train_transform,
    )

    val_loader = get_dataloader(
        config.dataset_name,
        config.model,
        "val",
        batch_size=1,
        shuffle=False,
        num_workers=config.num_workers,
        pin_memory=True,
        transform=val_transform,
    )

    # define a model
    benet = get_model("cam_benet", in_channels=3, pretrained=True)  # 只是用来可视化benet的
    srnet = get_model("srnet", pretrained=config.pretrained)  # [generator, discriminator] 生成器、鉴别器
    generator, discriminator = srnet[0], srnet[1]

    # send the model to cuda/cpu
    benet.model.to(device)
    generator.to(device)
    discriminator.to(device)

    optimizerG = optim.Adam(                    # adam优化器
        generator.parameters(),                 # 用生成器的参数
        lr=config.learning_rate,                # learning rate
        betas=(config.beta1, config.beta2),     # 衰减因子
    )
    optimizerD = optim.Adam(
        discriminator.parameters(),
        lr=config.learning_rate,
        betas=(config.beta1, config.beta2),
    )

    lambda_dict = {"lambda1": config.lambda1, "lambda2": config.lambda2}

    # keep training and validation log
    begin_epoch = 0
    best_g_loss = float("inf")   # 设置无穷大
    best_d_loss = float("inf")

    # resume if you want # 从断点处继续训练模型
    if args.resume:
        resume_path = os.path.join(result_path, "checkpoint.pth")
        (
            begin_epoch,
            generator,
            discriminator,
            optimizerG,
            optimizerD,
            best_g_loss,
            best_d_loss,
        ) = resume_BEDSRNet(
            resume_path, generator, discriminator, optimizerG, optimizerD
        )

    log_path = os.path.join(result_path, "log.csv")
    train_logger = TrainLoggerBEDSRNet(log_path, resume=args.resume)

    # criterion for loss
    criterion = get_criterion(config.loss_function_name, device)    # 根据损失名和设备获取损失函数

    # Weights and biases
    if args.use_wandb:
        wandb.init(
            name=experiment_name,
            config=config,
            project="BEDSR-Net",
            job_type="training",
        )
        # Magic
        wandb.watch(generator, log="all")
        wandb.watch(discriminator, log="all")

    # train and validate model
    logger.info("Start training.")


    # 获取当前时间
    current_time = datetime.datetime.now()

    # 格式化时间信息
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    minute = current_time.minute

    # 创建文件夹名称
    folder_name = f"{year}_{month}_{day}_{hour}_{minute}"

    # 创建文件夹
    # os.makedirs(folder_name)

    # 如果需要指定在某个路径下创建文件夹，可以使用os.path.join
    folder_path = os.path.join(result_path, folder_name)
    train_folder = os.path.join(folder_path, f'train')
    train_inputs = os.path.join(train_folder, f'inputs')
    train_preds = os.path.join(train_folder, f'preds')
    train_gts = os.path.join(train_folder, f'gt')
    val_folder = os.path.join(folder_path, f'val')
    val_inputs = os.path.join(val_folder, f'inputs')
    val_preds = os.path.join(val_folder, f'preds')
    val_gts = os.path.join(val_folder, f'gt')
    val_ats = os.path.join(val_folder, f'ats')
    train_ats = os.path.join(train_folder, f'ats')
    os.makedirs(folder_path)
    os.makedirs(train_folder)
    os.makedirs(train_inputs)
    os.makedirs(train_preds)
    os.makedirs(train_gts)
    os.makedirs(val_folder)
    os.makedirs(val_inputs)
    os.makedirs(val_preds)
    os.makedirs(val_gts)
    os.makedirs(val_ats)
    os.makedirs(train_ats)

    # 训练
    for epoch in range(begin_epoch, config.max_epoch):
        # training
        start = time.time()
        img_train_out_path = os.path.join(result_path, f"eps_jung_2_27/train/{epoch}.jpg")
        img_val_out_path = os.path.join(result_path, f"eps_jung_2_27/val/{epoch}.jpg")

#——————————————————————————————————————————————————————————————————————————————————————————————————————————————#
    # 调用了一个train函数
        train_g_loss, train_d_loss, train_psnr, train_ssim, train_result_images,train_inputs_imgs,train_preds_imgs,train_gts_imgs,train_attention_maps   = train(
            train_loader,
            generator,
            discriminator,
            benet,
            criterion,
            lambda_dict,
            optimizerG,
            optimizerD,
            epoch,
            device,
        )
#——————————————————————————————————————————————————————————————————————————————————————————————————————————————#

        train_time = int(time.time() - start)

#——————————————————————————————————————————————————————————————————————————————————————————————————————————————#
        # 调用了evaluate函数
        # validation
        start = time.time()
        val_g_loss, val_d_loss, val_psnr, val_ssim, val_result_images,val_inputs_imgs,val_preds_imgs,val_gts_imgs,val_attention_maps = evaluate(
            val_loader, generator, discriminator, benet, criterion, lambda_dict, device
        )
#——————————————————————————————————————————————————————————————————————————————————————————————————————————————#
        val_time = int(time.time() - start)
        for i in range(0, len(val_inputs_imgs)):
            vi = val_inputs_imgs[i].transpose([1, 2, 0]) * 0.5 + 0.5
            vp = val_preds_imgs[i].transpose([1, 2, 0]) * 0.5 + 0.5
            vg = val_gts_imgs[i].transpose([1, 2, 0]) * 0.5 + 0.5
            vat = val_attention_maps[i].transpose([1, 2, 0]) * 0.5 + 0.5
            ti = train_inputs_imgs[i].transpose([1, 2, 0]) * 0.5 + 0.5
            tp = train_preds_imgs[i].transpose([1, 2, 0]) * 0.5 + 0.5
            tg = train_gts_imgs[i].transpose([1, 2, 0]) * 0.5 + 0.5
            tat = train_attention_maps[i].transpose([1, 2, 0]) * 0.5 + 0.5

            cv2.imwrite(os.path.join(val_inputs, f'{epoch}_{i}.jpg'),cv2.cvtColor(vi*255, cv2.COLOR_RGB2BGR))
            cv2.imwrite(os.path.join(val_preds, f'{epoch}_{i}.jpg'),cv2.cvtColor(vp*255, cv2.COLOR_RGB2BGR))
            cv2.imwrite(os.path.join(val_gts, f'{epoch}_{i}.jpg'),cv2.cvtColor(vg*255, cv2.COLOR_RGB2BGR))
            cv2.imwrite(os.path.join(train_inputs, f'{epoch}_{i}.jpg'),cv2.cvtColor(ti*255, cv2.COLOR_RGB2BGR))
            cv2.imwrite(os.path.join(train_preds, f'{epoch}_{i}.jpg'),cv2.cvtColor(tp*255, cv2.COLOR_RGB2BGR))
            cv2.imwrite(os.path.join(train_gts, f'{epoch}_{i}.jpg'),cv2.cvtColor(tg*255, cv2.COLOR_RGB2BGR))
            cv2.imwrite(os.path.join(val_ats, f'{epoch}_{i}.jpg'),cv2.cvtColor(vat*255, cv2.COLOR_RGB2BGR))
            cv2.imwrite(os.path.join(train_ats, f'{epoch}_{i}.jpg'),cv2.cvtColor(tat*255, cv2.COLOR_RGB2BGR))
            # cv2.imwrite(os.path.join(val_inputs, f'{i}.jpg'),cv2.cvtColor(vi*255, cv2.COLOR_RGB2BGR))
            # cv2.imwrite(os.path.join(val_preds, f'{i}.jpg'),cv2.cvtColor(vp*255, cv2.COLOR_RGB2BGR))
            # cv2.imwrite(os.path.join(val_gts, f'{i}.jpg'),cv2.cvtColor(vg*255, cv2.COLOR_RGB2BGR))
            # cv2.imwrite(os.path.join(train_inputs, f'{i}.jpg'),cv2.cvtColor(ti*255, cv2.COLOR_RGB2BGR))
            # cv2.imwrite(os.path.join(train_preds, f'{i}.jpg'),cv2.cvtColor(tp*255, cv2.COLOR_RGB2BGR))
            # cv2.imwrite(os.path.join(train_gts, f'{i}.jpg'),cv2.cvtColor(tg*255, cv2.COLOR_RGB2BGR))

        

        cv2.imwrite(img_train_out_path, cv2.cvtColor(train_result_images*255, cv2.COLOR_RGB2BGR))
        cv2.imwrite(img_val_out_path, cv2.cvtColor(val_result_images*255, cv2.COLOR_RGB2BGR))
        print(f'第{epoch}轮结束================================>')

        cv2.imwrite(img_train_out_path, cv2.cvtColor(train_result_images*255, cv2.COLOR_RGB2BGR))
        cv2.imwrite(img_val_out_path, cv2.cvtColor(val_result_images*255, cv2.COLOR_RGB2BGR))

        # save a model if top1 acc is higher than ever
        if best_g_loss > val_g_loss:
            best_g_loss = val_g_loss
            best_d_loss = val_d_loss
            torch.save(
                generator.state_dict(),
                os.path.join(result_path, "pretrained_g_srnet.prm"),
            )
            torch.save(
                discriminator.state_dict(),
                os.path.join(result_path, "pretrained_d_srnet.prm"),
            )

        # save checkpoint every epoch
        save_checkpoint_BEDSRNet(
            result_path,
            epoch,
            generator,
            discriminator,
            optimizerG,
            optimizerD,
            best_g_loss,
            best_d_loss,
        )

        # write logs to dataframe and csv file
        train_logger.update(
            epoch,
            optimizerG.param_groups[0]["lr"],
            optimizerD.param_groups[0]["lr"],
            train_time,
            train_g_loss,
            train_d_loss,
            val_time,
            val_g_loss,
            val_d_loss,
            train_psnr,
            train_ssim,
            val_psnr,
            val_ssim,
        )

        # save logs to wandb
        if args.use_wandb:
            wandb.log(
                {
                    "lrG": optimizerG.param_groups[0]["lr"],
                    "lrD": optimizerD.param_groups[0]["lr"],
                    "train_time[sec]": train_time,
                    "train_g_loss": train_g_loss,
                    "train_d_loss": train_d_loss,
                    "val_time[sec]": val_time,
                    "val_g_loss": val_g_loss,
                    "val_d_loss": val_d_loss,
                    "train_psnr": train_psnr,
                    "val_psnr": val_psnr,
                    "train_ssim": train_ssim,
                    "val_ssim": val_ssim,
                    "train_image": wandb.Image(train_result_images, caption="train"),
                    "val_image": wandb.Image(val_result_images, caption="val"),
                },
                step=epoch,
            )

    # save models
    torch.save(generator.state_dict(), os.path.join(result_path, "g_final_0331_new.prm"))
    torch.save(discriminator.state_dict(), os.path.join(result_path, "d_final_0331_new.prm"))

    # delete checkpoint
    os.remove(os.path.join(result_path, "g_checkpoint.pth"))
    os.remove(os.path.join(result_path, "d_checkpoint.pth"))

    logger.info("Done")


if __name__ == "__main__":
    main()
