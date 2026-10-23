from pathlib import Path
from PIL import Image
from shutil import copy2
from data_utils import convert_annotation_to_yolo
def convert_image(images):
    success_count = 0
    for image_path in images:
        #根据图片编号获取标注编号
        image_name = image_path.stem

        #print(image_name)
        not_name = image_name.replace("_test", "")

        #获取标注路径
        img_dir = image_path.parent
        img_dir_name = img_dir.name
        group_path = image_path.parent.parent
        group_name = group_path.name
        #print(group_name)
        label_name = img_dir_name + "_not"
        label_path = group_path/f"{label_name}"/f"{not_name}.txt"
        if not label_path.exists():
            print("路径缺失:", label_path)
            continue
        #读取文件内容
        content = label_path.read_text(encoding="utf-8")
        with Image.open(image_path) as img:
            width_image, height_image = img.size
        print(width_image, height_image)
        #调用函数，处理数据
        yolo_lines = convert_annotation_to_yolo(content,width_image,height_image)
        #整理数据，输出文本
        output_data = Path(__file__).parent.parent/"data"/"labels"
        output_data.mkdir(parents=True,exist_ok=True)
        output_file = output_data/f"{group_name}_{not_name}_test.txt"
        output_file.write_text("\n".join(yolo_lines))
        #复制图片数据
        new_image_name = f"{group_name}_{image_name}.jpg"
        image_output = Path(__file__).parent.parent/"data"/"images"
        image_output.mkdir(parents=True,exist_ok=True)
        image_output_file = image_output/new_image_name
        copy2(
            image_path,
            image_output_file
        )
        success_count += 1
    print("成功转换：",success_count)
root = Path(__file__).parent.parent/"DeepPCB"/"DeepPCB-master"/"PCBData"
print(root)
images = list(root.glob("*/*/*_test.jpg"))
convert_image(images)

