from ultralytics import YOLO
from pathlib import Path
import csv

project_root = Path(__file__).parent.parent
data_yaml = project_root/'data'/'data.yaml'

print("数据配置文件：", data_yaml)
print("是否存在：", data_yaml.exists())

if __name__ == "__main__":
    # 加载一个预训练模型
    model = YOLO("yolo11n.pt")
    # 开始训练
    model.train(
        data=str(data_yaml),
        epochs=1,
        imgsz=640,
        batch=4,
        device="cpu",
    )

    # ===== 训练结束，拿每类缺陷的指标 =====
    metrics = model.val(data=str(data_yaml), device="cpu", verbose=False,
                        project=str(project_root / 'runs' / 'detect'))
    rows = metrics.summary()

    headers = ["类别", "Images", "Instances", "Precision", "Recall", "F1", "mAP50", "mAP75", "mAP50-95"]
    data = [
        [r["Class"], r["Images"], r["Instances"],
         r["Box-P"], r["Box-R"], r["Box-F1"],
         r["mAP50"], r["mAP75"], r["mAP50-95"]] for r in rows
    ]

    # 拼 Markdown 表
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in data:
        lines.append("| " + " | ".join(str(v) for v in r) + " |")
    table = "\n".join(lines)

    print("\n===== 各类缺陷指标 =====")
    print(table)

    # 存盘
    save_dir = Path(model.trainer.save_dir)
    (save_dir / "各类缺陷指标.md").write_text(table + "\n", encoding="utf-8")
    with open(save_dir / "各类缺陷指标.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(data)

    print("\n已保存:", save_dir / "各类缺陷指标.md")
    print("已保存:", save_dir / "各类缺陷指标.csv")
