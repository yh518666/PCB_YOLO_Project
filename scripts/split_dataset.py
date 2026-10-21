import random
from pathlib import Path

data_root = Path(__file__).parent.parent/"data"
images_dir = data_root/"images"
labels_dir = data_root/"labels"
#创建图片相关文件夹
images_train = images_dir/"train"
images_train.mkdir(parents=True,exist_ok=True)
images_val = images_dir/"val"
images_val.mkdir(parents=True,exist_ok=True)
#创建标注相关文件夹
labels_train = labels_dir/"train"
labels_train.mkdir(parents=True,exist_ok=True)
labels_val = labels_dir/"val"
labels_val.mkdir(parents=True,exist_ok=True)
#将图片文件与标注文件一一对应
images = list(images_dir.glob("*.jpg"))
pairs = []
for image_path in images:
    label_path = labels_dir/(image_path.stem+".txt")
    if label_path.exists():
        pairs.append((image_path, label_path))
#固定种子生成随机数
random.seed(42)
random.shuffle(pairs)
#按照80%train，20%val随机划分
split = int(len(pairs)*0.8)
trains, vals = pairs[:split], pairs[split:]
#将划分后的数据集写入文件夹
for img,lab in trains:
    img.replace(images_train/img.name)
    lab.replace(labels_train/lab.name)
for img,lab in vals:
    img.replace(images_val/img.name)
    lab.replace(labels_val/lab.name)
