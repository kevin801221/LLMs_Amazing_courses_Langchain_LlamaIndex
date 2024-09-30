# 使用 TRL 進行 DPO 優化與 LLaVA-NeXT 模型的訓練指南

本指南將涵蓋如何使用 Hugging Face、TRL（Transformer Reinforcement Learning）以及 PEFT（Parameter-Efficient Fine-Tuning）庫來進行 DPO（直接偏好優化）訓練，並應用於多模態模型如 LLaVA 1.5、LLaVA 1.6 和 LLaVA-NeXT。整個過程將涵蓋數據集的準備、模型的微調、LoRA 應用以及如何整合 WandB 進行實驗追蹤。

---

## 目錄

1. [專案概述](#專案概述)
2. [環境設置與依賴安裝](#環境設置與依賴安裝)
3. [數據集處理與格式化](#數據集處理與格式化)
4. [模型準備與微調](#模型準備與微調)
5. [DPO 訓練流程](#DPO-訓練流程)
6. [PEFT 與 LoRA 微調](#PEFT-與-LoRA-微調)
7. [LLaVA-NeXT 模型的下載與應用](#LLaVA-NeXT-模型的下載與應用)
8. [使用 WandB 進行實驗追蹤](#使用-WandB-進行實驗追蹤)
9. [DPO 訓練的標準化流程](#DPO-訓練的標準化流程)

---

## 專案概述

此專案的目標是使用 Hugging Face 和 TRL 進行大型語言模型（LLMs）的 DPO 訓練，特別針對 LLaVA-NeXT 等多模態模型在視覺-文本對話和圖像識別等任務中的優選回應能力進行微調。本文將詳細介紹如何下載、準備和微調 LLaVA-NeXT 模型，並在訓練過程中整合 WandB 進行實驗追蹤。

---

## 環境設置與依賴安裝

### 安裝依賴
首先，確保安裝了所有必要的依賴庫：

```bash
pip install transformers torch torchvision datasets pandas requests peft trl wandb
```

---

## 數據集處理與格式化

### 1. 加載數據集
我們將使用 `openbmb/RLAIF-V-Dataset` 和 `flaviagiammarino/vqa-rad` 數據集進行模型訓練。

```python
from datasets import load_dataset

# 加載數據集
dataset = load_dataset("openbmb/RLAIF-V-Dataset", split="train[:1%]")
sample = dataset[1]
print(sample["image"].show())
print(sample["question"])
print(sample["rejected"])
print(sample["chosen"])
```

### 2. 數據格式化
為了準備數據進行訓練，我們需要將數據轉換成 DPO 模型可接受的格式。

```python
from PIL import Image

def format(example):
    # 準備輸入模板
    prompt = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": example["question"]}]}]
    chosen = [{"role": "assistant", "content": [{"type": "text", "text": example["chosen"]}]}]
    rejected = [{"role": "assistant", "content": [{"type": "text", "text": example["rejected"]}]}]
    
    prompt = processor.apply_chat_template(prompt, tokenize=False)
    chosen = processor.apply_chat_template(chosen, tokenize=False)
    rejected = processor.apply_chat_template(rejected, tokenize=False)

    # 圖像縮放
    max_size = processor.image_processor.size["longest_edge"]
    example["image"].thumbnail((max_size, max_size))
    
    return {"images": [example["image"]], "prompt": prompt, "chosen": chosen, "rejected": rejected}

# 將格式化應用到整個數據集
dataset = dataset.map(format, remove_columns=dataset.column_names)
```

---

## 模型準備與微調

### 1. 克隆 LLaVA 1.6 模型代碼
使用以下命令克隆 Hugging Face 的 LLaVA 1.6 代碼：

```bash
git clone https://huggingface.co/liuhaotian/llava-v1.6-mistral-7b
cd llava-v1.6-mistral-7b
```

### 2. 加載模型與處理器
確認路徑正確並加載模型和處理器：

```python
from transformers import AutoProcessor, AutoModelForCausalLM

# 加載模型和處理器
processor = AutoProcessor.from_pretrained("/content/llava-v1.6-mistral-7b")
model = AutoModelForCausalLM.from_pretrained("/content/llava-v1.6-mistral-7b")
```

---

## DPO 訓練流程

DPO 是一種根據偏好數據優化模型的技術，適合用於視覺和文本對齊任務中。以下是基本的 DPO 訓練步驟：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import DPOTrainer

# 加載模型和 tokenizer
model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# 初始化 DPO 訓練器
trainer = DPOTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
)

# 開始訓練
trainer.train()
```

---

## PEFT 與 LoRA 微調

PEFT 是一種高效的微調方法，能夠在低資源的情況下進行大模型的微調。

### 1. 使用 PEFT 進行 LoRA 微調

```python
from peft import get_peft_model, LoraConfig
from transformers import AutoModelForVision2Seq

# 加載 Idefics 2.8B 模型
model = AutoModelForVision2Seq.from_pretrained("HuggingFaceM4/idefics2-8b")

# 設置 LoRA 配置
peft_config = LoraConfig(target_modules="all-linear")
model = get_peft_model(model, peft_config)
```

---

## LLaVA-NeXT 模型的下載與應用

LLaVA-NeXT 模型在視覺與語言任務上的表現尤為優秀，特別是在高解析度圖像處理方面。以下是下載與使用 LLaVA-NeXT 模型的步驟：

### Step 1: 安裝所需的庫

確保您已安裝必要的庫：

```bash
pip install transformers torch torchvision
```

### Step 2: 加載模型與 Tokenizer

使用 `LlavaNextForConditionalGeneration` 和 `LlavaNextProcessor` 類來加載模型和處理器：

```python
from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
import torch

# 加載模型與處理器
model_name = "llava-hf/llava-v1.6-mistral-7b-hf"
processor = LlavaNextProcessor.from_pretrained(model_name)
model = LlavaNextForConditionalGeneration.from_pretrained(model_name, torch_dtype=torch.float16)
```

### Step 3: 準備輸入數據

```python
from PIL import Image

# 準備輸入數據
prompt = "What are the things I should be cautious about when I visit here?"
image_path = "path/to/your/image.jpg"  # 替換為您的圖像路徑
image = Image.open(image_path)

# 預處理輸入
inputs = processor(text=prompt, images=image, return_tensors="pt")
```

### Step 4: 執行推理

```python
# 將模型移動到 GPU（如果可用）
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# 生成結果
with torch.no_grad():
    outputs = model.generate(**inputs.to(device))

# 解碼並打印輸出
result = processor.decode(outputs[0], skip_special_tokens=True)
print(result)
```

### Step 5: DPO 訓練（可選）

若您想對模型進行進一步的微調或訓練，您可以設置 DPOTrainer 進行訓練：

```python
from trl import DPOTrainer

trainer = DPOTrainer(
    model=model,
    tokenizer=processor.tokenizer,
    train_dataset=dataset,
)

# 開

始訓練
trainer.train()
```

---

## 使用 WandB 進行實驗追蹤

### 1. 初始化 WandB

在訓練過程中整合 WandB 進行實驗監控：

```python
import wandb

wandb.init(project="idefics2-8b-training", config={
    "model_name": "HuggingFaceM4/idefics2-8b",
    "dataset_name": "openbmb/RLAIF-V-Dataset",
    "train_split": 0.3,
    "num_epochs": 1,
    "batch_size": 4,
    "gradient_accumulation_steps": 4,
    "learning_rate": 5e-5
})
```

---

## DPO 訓練的標準化流程

根據不同應用場景，DPO 流程可以進行相應調整：

1. **視覺-文本對齊任務**：使用 `LAION-CC-SBU` 或 `RLHF-V` 數據集進行多模態數據處理。
   
2. **基於 NLP 的人類反饋優化**：使用 DPO 來調整模型生成的文本，使其更符合用戶偏好。

3. **醫療影像處理**：使用 LLaVA-NeXT 進行醫療影像優化，增強模型的視覺推理與文本生成能力。

