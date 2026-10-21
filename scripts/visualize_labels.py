from pathlib import Path
import cv2
from PIL import Image
import random

data_root = Path(__file__).parent.parent/"data"
NUM_SAMPLES = 10

for split in ["train","val"]:
    images_dir = data_root/"images"/split
    labels_dir = data_root/"labels"/split
    out_dir = data_root/"check"/split
    out_dir.mkdir(parents=True,exist_ok=True)
    images = list(images_dir.glob("*.jpg"))

    pairs = []
    for image_path in images:
        label_path = labels_dir/(image_path.stem+".txt")
        if label_path.exists():
            pairs.append((image_path, label_path))

    samples = random.sample(pairs, min(NUM_SAMPLES, len(pairs)))

    for image_path,label_path in samples:
        with Image.open(image_path) as img:
            width_image, height_image = img.size

        img = cv2.imread(str(image_path))
        label = label_path.read_text(encoding="utf-8")
        for line in label.split("\n"):
            if not line.strip():
                continue
            ty_yolo, x, y, w, h = map(float,line.split())
            x_c = x*width_image
            y_c = y*height_image
            width = w*width_image
            height = h*height_image
            x1 = int(x_c - width/2)
            y1 = int(y_c - height/2)
            x2 = int(x_c + width/2)
            y2 = int(y_c + height/2)
            ty = int(ty_yolo) + 1
            cv2.rectangle(
                img,
                (x1,y1),
                (x2,y2),
                (0,0,255),
                2
            )
        cv2.imwrite(
            str(out_dir/image_path.name),
            img
        )
        print(f"[{split}]已保存{image_path.name}")
print("可视化完成")
