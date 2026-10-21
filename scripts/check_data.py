from pathlib import Path

data_root = Path(__file__).parent.parent/"data"

images_train_dir = data_root/"images"/"train"
labels_train_dir = data_root/"labels"/"train"

images_val_dir = data_root/"images"/"val"
labels_val_dir = data_root/"labels"/"val"

images_train = list(images_train_dir.glob("*.jpg"))
labels_train = list(labels_train_dir.glob("*.txt"))
images_val = list(images_val_dir.glob("*.jpg"))
labels_val = list(labels_val_dir.glob("*.txt"))
#检查图片数量与标签数量是否一致
print("===========train===========")
print("图片数量：",len(images_train))
print("标注数量：",len(labels_train))
print("============val============")
print("图片数量：",len(images_val))
print("标注数量：",len(labels_val))
#检查图片与标注是否一一对应
for image in images_train[:3]:
    label = labels_train_dir/(image.stem+".txt")
    if not label.exists():
        print("train图片对应标注缺失：",image.name)
        continue
    print(image.name,label.name)

print("=================================")

for image in images_val[:3]:
    label = labels_val_dir/(image.stem+".txt")
    if not label.exists():
        print("val图片对应标注缺失：",image.name)
        continue
    print(image.name,label.name)
#检查标注文件的数据格式是否符合yolo标准
def check_labels(labels):
    error_count = 0
    for label in labels:
        lines = label.read_text(encoding="utf-8").splitlines()
        if not lines:
            print("该标签为空：",label.name)
        for line_number, line in enumerate(lines,start=1):
            if not line.strip():
                continue
            pairs = line.split()
            #检查每行数据是否完整
            if len(pairs) != 5:
                error_count +=1
                print("格式错误：",label.name,f"第{line_number}行")
                continue
            class_id = int(pairs[0])
            x,y,w,h = map(float,pairs[1:])
            #检查类型数据是否正确
            if class_id not in range(0,6):
                error_count += 1
                print("类别错误：",label.name,f"第{line_number}行")
            #检查x数据是否正确
            if not (0<=x<=1):
                error_count += 1
                print("x错误：",label.name,f"第{line_number}行")
            #检查y数据是否正确
            if not (0<=y<=1):
                error_count += 1
                print("y错误：",label.name,f"第{line_number}行")
            # 检查w数据是否正确
            if not (0<=w<=1):
                error_count += 1
                print("w错误：",label.name,f"第{line_number}行")
            #检查h数据是否正确
            if not (0<=h<=1):
                error_count += 1
                print("h错误：",label.name,f"第{line_number}行")
    print("标注检查完毕，错误数量：",error_count)

print("\n==========检查train标注==========")
check_labels(labels_train)
print("\n===========检查val标注===========")
check_labels(labels_val)