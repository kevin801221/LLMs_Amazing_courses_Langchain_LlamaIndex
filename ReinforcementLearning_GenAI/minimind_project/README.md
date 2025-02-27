# MiniMind-V 醫療 VQA 模型訓練指南 🎯🎨🖥️

## 1. 簡介 🎉📢💡

MiniMind-V 是一款超小型多模態視覺語言模型（VLM），旨在讓個人 GPU 也能快速推理甚至訓練。該模型的最小版本僅 26M 參數，約為 GPT-3 的 1/7000，並且能夠在 NVIDIA 3090 單卡上以 **1 小時** 完成 1 個 epoch 的訓練，成本約 **1.3 元人民幣**。

本指南詳細介紹如何使用 **MiniMind-V** 訓練醫療 VQA（Visual Question Answering）模型。我們將使用 **SLAKE-VQA-English** 數據集，並對模型進行監督微調（Supervised Fine-Tuning, SFT），以提高其在醫療影像問答任務中的表現。

本指南適用於配備 **NVIDIA GPU（建議 8GB 以上顯存）** 的機器。

---

## 2. 環境設置 🛠️⚙️🔧

### 2.1 克隆 MiniMind-V 倉庫
```bash
# 下載 MiniMind-V 原始碼
git clone https://github.com/jingyaogong/minimind-v.git
cd minimind-v
```

### 2.2 下載 CLIP 模型
```bash
# 下載 CLIP 模型到 ./model/vision_model 目錄下
git clone https://huggingface.co/openai/clip-vit-base-patch16
# 或
git clone https://www.modelscope.cn/models/openai-mirror/clip-vit-base-patch16
```

### 2.3 建立並啟動虛擬環境 🖥️🐍🔗
```bash
# 創建 Python 虛擬環境
python -m venv minimind_gpu

# 啟動虛擬環境
source minimind_gpu/bin/activate  # Linux/macOS
minimind_gpu\Scripts\activate      # Windows
```

### 2.4 安裝依賴 📦📌🔍
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install datasets tqdm
```

---

## 3. 下載並轉換 SLAKE-VQA 數據集 📊📥📂

我們需要將 **SLAKE-VQA-English** 數據集轉換為 MiniMind-V 需要的 JSONL 格式。

### 3.1 創建 `convert_slake_dataset.py` 腳本 📝💾🔄

```python
from datasets import load_dataset
import json
import os

# 下載 SLAKE-VQA 數據集
dataset = load_dataset("Slake-VQA-English")

# 創建輸出目錄
os.makedirs("dataset/medical_images", exist_ok=True)

# 轉換為 JSONL 格式
def convert_to_jsonl(split):
    output_path = f"dataset/medical_vqa_{split}.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for item in dataset[split]:
            json.dump(item, f)
            f.write("\n")

convert_to_jsonl("train")
convert_to_jsonl("validation")
convert_to_jsonl("test")
print("數據集轉換完成！")
```

### 3.2 執行數據轉換 🚀🔄📁
```bash
python convert_slake_dataset.py
```

---

## 4. 訓練 MiniMind-V 醫療 VQA 模型 🏋️‍♂️📊🔬

### 4.1 預訓練（學習圖像描述） 🎓📸💡
```bash
python train_pretrain_vlm.py --epochs 4
```

### 4.2 監督微調（學習看圖對話方式） 🗣️📜🖼️
```bash
python train_sft_vlm.py --epochs 4
```

---

## 5. 模型評估與推理 🎯🧐🔍

### 5.1 評估模型 📊📑🧠
```bash
python eval_vlm.py --model_mode 1 # 0 為測試預訓練模型，1 為測試 SFT 模型
```

### 5.2 啟動 Web 介面 🌐🖥️📡
```bash
python web_demo_vlm.py --model_path out/medical_vlm_768.pth
```

---

## 6. 完整指令列表 📝📌📂

```bash
# 1. 克隆倉庫
git clone https://github.com/jingyaogong/minimind-v.git
cd minimind-v

# 2. 設置環境
python -m venv minimind_gpu
source minimind_gpu/bin/activate  # Linux/macOS
minimind_gpu\Scripts\activate      # Windows
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 下載並轉換數據集
python convert_slake_dataset.py

# 4. 預訓練與監督微調
python train_pretrain_vlm.py --epochs 4
python train_sft_vlm.py --epochs 4

# 5. 評估與推理
python eval_vlm.py --model_mode 1
python web_demo_vlm.py --model_path out/medical_vlm_768.pth
```

---

## 7. 注意事項 ⚠️🔎📢
- **硬體需求**: 需要 **NVIDIA GPU（建議 8GB 以上顯存）**。
- **訓練時間**: 視硬體配置而定，可能需要 **數小時到數天**。
- **內存優化**: 如果遇到 GPU 記憶體不足，可以 **減少 batch_size** 或 **使用梯度累積**。
- **數據擴充**: 可以考慮加入 **其他醫療 VQA 數據集** 來提升模型表現。

---

## 8. 結論 🎊🎯💡
透過本指南，您可以成功使用 **MiniMind-V** 訓練一個適用於醫療影像問答（VQA）的模型，並在 Web 介面上進行測試。

這個微調後的模型可以應用於 **醫療影像診斷、輔助決策、醫學教育** 等領域，提升醫療 AI 的應用價值！ 🚀📈🌟

