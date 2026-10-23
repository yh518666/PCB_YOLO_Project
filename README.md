# YOLO11 PCB 缺陷检测

基于 YOLO11 迁移学习的 PCB 表面缺陷检测项目，使用 DeepPCB 数据集，
覆盖 6 类缺陷，实现从数据预处理、训练到逐类别评估的完整流程。

## 环境依赖
- Python 3.x
- PyTorch（CPU 或 CUDA 版）
- ultralytics

## 快速开始
CPU训练：
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 准备数据（下载 DeepPCB → 转 YOLO → 划分）
python scripts/convert_deeppcb.py
python scripts/split_dataset.py

# 3. 检查数据（图片与标注数据是否一一对应，YOLO格式标注是否正确对应缺陷位置）
python scripts/check_data.py
python scripts/visualize_labels.py

# 4. 训练评估（逐类别指标）
python scripts/train.py

```
GPU训练：
注：训练前修改train.py文件，" epoch=50,batch=32,device=0 "
```bash
# 1. 下载GPU版torch + 安装依赖
pip install torch==2.14.0 torchvision==0.29.0 --index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt 

# 2. 准备数据（下载 DeepPCB → 转 YOLO → 划分）
python scripts/convert_deeppcb.py
python scripts/split_dataset.py

# 3. 检查数据（图片与标注数据是否一一对应，YOLO格式标注是否正确对应缺陷位置）
python scripts/check_data.py
python scripts/visualize_labels.py

# 4. 训练评估（逐类别指标）
python scripts/train.py

```

## 目录结构

```
PCB_YOLO_Project/
├── data/                          # 数据目录
│   ├── data.yaml                  # 数据集配置（6 类缺陷）
│   ├── images/                    # 图片（划分后生成）
│   ├── labels/                    # YOLO 标注（划分后生成）
│   └── check/                     # 标注可视化输出（可视化检查生成）
├── scripts/                       # 核心脚本
│   ├── convert_deeppcb.py         # 原始标注 → YOLO 格式转换
│   ├── data_utils.py              # 坐标转换工具函数
│   ├── split_dataset.py           # 划分训练集 / 验证集
│   ├── check_data.py              # 数据完整性检查
│   ├── visualize_labels.py        # 标注可视化（画框抽查）
│   └── train.py                   # 训练 + 逐类别评估
├── README.md                      # 项目说明
├── requirements.txt                # 依赖清单
└── .gitignore                     # Git 忽略规则
```


## 实验结果
仅 1 个 epoch 的基线训练后，模型在验证集上的整体指标如下。

**整体检测指标（验证集）**

| Precision | Recall | F1 | mAP50 | mAP50-95 |
|:---:|:---:|:---:|:---:|:---:|
| 0.569 | 0.571 | 0.552 | **0.597** | 0.358 |

进一步将验证集按六类缺陷拆解，逐类别指标如下。

**逐类别检测指标（验证集）**

| 类别 | Images | Instances | Precision | Recall | F1 | mAP50 | mAP75 | mAP50-95 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| open（开路） | 276 | 403 | 0.479 | 0.712 | 0.573 | 0.613 | 0.302 | 0.316 |
| short（短路） | 210 | 287 | 0.508 | 0.392 | 0.443 | 0.404 | 0.181 | 0.209 |
| mousebite（鼠咬） | 255 | 397 | 0.521 | 0.573 | 0.546 | 0.565 | 0.372 | 0.334 |
| spur（毛刺） | 241 | 337 | 0.519 | **0.199** | 0.288 | **0.370** | 0.204 | 0.199 |
| copper（余铜） | 246 | 299 | **0.726** | **0.856** | **0.786** | **0.888** | **0.764** | **0.617** |
| pin-hole（针孔） | 267 | 306 | 0.658 | 0.696 | 0.677 | 0.744 | 0.547 | 0.474 |

改用 GPU 训练（batch 从 4 提升到 32，训练 50 个 epoch）后，模型在验证集的整体指标如下：

**整体检测指标（验证集）**

| Precision | Recall | F1 | mAP50 | mAP50-95 |
|:---:|:---:|:---:|:---:|:---:|
| 0.976 | 0.969 | 0.971 | 0.988 | 0.758 |

进一步将验证集按六类缺陷拆解，逐类别指标如下。

**逐类别检测指标（验证集）**

| 类别 | Images | Instances | Precision | Recall | F1 | mAP50 | mAP75 | mAP50-95 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| open | 276 | 403 | 0.98653 | 0.97767 | 0.98208 | 0.9891 | 0.85987 | 0.7135 |
| short | 210 | 287 | 0.97905 | 0.94077 | 0.95952 | 0.98058 | 0.8259 | 0.68646 |
| mousebite | 255 | 397 | 0.97159 | 0.95214 | 0.96177 | 0.98029 | 0.92108 | 0.76291 |
| spur | 241 | 337 | 0.97023 | 0.96692 | 0.96857 | 0.98672 | 0.90248 | 0.73309 |
| copper | 246 | 299 | 0.97323 | 0.97659 | 0.97491 | 0.9887 | 0.9887 | 0.88998 |
| pin-hole | 267 | 306 | 0.97426 | 0.98937 | 0.98176 | 0.99173 | 0.99173 | 0.86784 |

## 数据集
DeepPCB 数据集（https://github.com/tangsanli5201/DeepPCB），6 类缺陷。

## 许可证
本项目代码遵循 MIT 协议；YOLO11 遵循 AGPL-3.0。
