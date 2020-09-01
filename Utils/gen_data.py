import tifffile as tiff
import os
import numpy as np


def create_dataset_1(saved_path="dataset",crop_size=256, step=30, need_c=3):
    print('creating dataset...')
    # file_names = ["no_cotton06.png"," no_cotton_town.png", train08_1.tif  train08_2.tif]
    # 未切割的原始图片和标签图路径
    train_dir = r"data/train/image"
    label_dir = r"data/train/label"
    file_names = os.listdir(label_dir)
    count = 0
    for file_name in file_names:
        label_file = os.path.join(label_dir, file_name)
        # print("label file name", file_name)
        if "png" in file_name:
            file_name = file_name.split(".")[0] + '.tif'
        # print("train")
        train_file = os.path.join(train_dir, file_name)
        src_img = tiff.imread(train_file)[:, :, :need_c]  # 4 channels
        label_img = tiff.imread(label_file)  # single channel
        # assert src_img.shape[0]==label_img.shape[0] and src_img.shape[1]==label_img.shape[1], "训练图和标签图大小不一致"
        print(src_img.max(axis=(0, 1)))
        # src_img = np.where(src_img>255, 0, src_img)
        label_img = np.where(label_img > 0, 1, 0)
        print(src_img.max(axis=(0, 1)))
        print(label_img.max())
        # g_count = 0
        train_height, train_width, _ = src_img.shape
        # 每次步进10,往前剪裁样本。
        label_h, label_w = label_img.shape
        assert train_height == label_h and train_width == label_w, "图片大小不一致"
        # step = 10
        steps_h = np.ceil((train_height - crop_size) / step)
        steps_w = np.ceil((train_width - crop_size) / step)
        padded_h = int(steps_h * step + crop_size)
        padded_w = int(steps_w * step + crop_size)
        train_padded = np.zeros(shape=(padded_h, padded_w, need_c))
        label_padded = np.zeros(shape=(padded_h, padded_w))
        print(src_img.shape)
        print(train_padded.shape)
        train_padded[:train_height, :train_width, :] = src_img
        label_padded[:label_h, :label_w] = label_img
        print("crop file ", file_name)
        for i in range(int(steps_h)):
            for j in range(int(steps_w)):
                train_crop = train_padded[i * step:crop_size + step * i, j * step:crop_size + step * j, :]
                label_crop = label_padded[i * step:crop_size + step * i, j * step:crop_size + step * j]
                train_save = f"{saved_path}/img/{count}.tif"
                label_save = f"{saved_path}/label/{count}.tif"

                tiff.imsave(train_save, train_crop)
                tiff.imsave(label_save, label_crop)
                count += 1
        print("have croped ", count)
    print("total croped", count)


def main():
    create_dataset_1(saved_path="dataset",crop_size=256, step=20, need_c=4) # print(max(maxs))


if __name__ == '__main__':
    main()
