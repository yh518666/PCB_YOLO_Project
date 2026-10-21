def convert_annotation_to_yolo(content,width_image,height_image):
    lines = content.split("\n")
    yolo_lines = []
    for line in lines:
        part = line.split()
        # 空行跳过
        if not part:
            continue
        # 取出数值
        x_1,y_1,x_2,y_2,ty = map(int,part)
        # 计算相关量
        width = x_2 - x_1
        height = y_2 - y_1
        x_c = (x_2 + x_1) / 2
        y_c = (y_2 + y_1) / 2
        # 归一化处理
        x_c_relative = x_c / width_image
        y_c_relative = y_c / height_image
        width_relative = width / width_image
        height_relative = height / height_image
        ty_yolo = ty - 1
        # 保存YOLO行
        yolo_line = (f"{ty_yolo} {x_c_relative} {y_c_relative} {width_relative} {height_relative}")
        yolo_lines.append(yolo_line)
    return yolo_lines