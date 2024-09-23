# 使用 TRL 進行 DPO 優化與多模態模型（LLaVA）訓練的完整指南

本指南將帶您逐步了解如何使用 Hugging Face、TRL（Transformer Reinforcement Learning）以及 PEFT（Parameter-Efficient Fine-Tuning）庫來進行 DPO（直接偏好優化）訓練，並應用於多模態模型如 LLaVA 1.5、LLaVA 1.6 和 LLaVA-NeXT。整個過程將涵蓋數據集的準備、模型的微調、LoRA 應用以及整合 WandB 進行實驗追蹤。

---

## 目錄

1. [專案概述](#專案概述)
2. [環境設置與依賴安裝](#環境設置與依賴安裝)
3. [數據集處理與格式化](#數據集處理與格式化)
4. [模型準備與微調](#模型準備與微調)
5. [DPO 訓練流程](#DPO-訓練流程)
6. [PEFT 與 LoRA 微調](#PEFT-與-LoRA-微調)
7. [LLaVA 系列模型的應用與推理](#LLaVA-系列模型的應用與推理)
8. [使用 WandB 進行實驗追蹤](#使用-WandB-進行實驗追蹤)
9. [DPO 訓練的標準化流程](#DPO-訓練的標準化流程)

---

## 專案概述

此專案的目標是使用 TRL 和 Hugging Face 庫，針對多模態模型（如 LLaVA 系列模型）進行 DPO 訓練，從而在視覺-文本對話和圖像識別等任務中提升模型的優選回應能力。本指南將涵蓋模型的準備、數據集處理、LoRA 微調以及如何使用 WandB 進行實驗跟踪和分析。

---

## 環境設置與依賴安裝

### 安裝依賴
請確保您安裝了所有必要的 Python 庫：

```bash
pip install datasets pandas requests transformers peft trl wandb
```

---

## 數據集處理與格式化

### 1. 加載數據集
本指南將使用 `openbmb/RLAIF-V-Dataset` 和 `flaviagiammarino/vqa-rad` 數據集來訓練模型。這些數據集包含問題、優選回應（chosen）和拒絕回應（rejected）。

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
為了準備數據進行訓練，我們需要將數據轉換成 DPO 模型可接受的格式，並進行圖像縮放以避免超出內存限制。

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

### 1. 訓練數據集準備
確保數據集包含 `query`（查詢）、`chosen`（優選回應）和 `rejected`（不優選回應）欄位。

### 2. 使用 DPO 進行訓練

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

### 2. 訓練

```python
trainer = DPOTrainer(
    model=model,
    ref_model=None,
    args=training_args,
    train_dataset=dataset,
    tokenizer=processor,
    peft_config=LoraConfig(target_modules="all-linear"),
)

trainer.train()
```

---

## LLaVA 系列模型的應用與推理

### LLaVA 1.5 使用方法

- **訓練**：適用於中等解析度圖像處理，支援文本生成與減少毒性等任務。

```bash
trl sft --model_name_or_path llava-1.5-7b --dataset_name openbmb/RLHF-V-Dataset --output_dir output-llava-1.5
```

### LLaVA 1.6 使用方法

- **訓練**：支援高解析度圖像（最高達 672x672 像素），強化視覺推理和 OCR 能力。

```bash
trl dpo --model_name_or_path llava-1.6-7b --dataset_name trl-internal-testing/hh-rlhf-helpful-base-trl-style --output_dir output-llava-1.6
```

### LLaVA-NeXT 使用方法

- **訓練**：支援超高解析度輸入，適用於醫療影像等高細節場景的推理與對話。

```bash
trl chat --model_name_or_path llava-next-7b --dataset_name medical-vqa-dataset --output_dir output-llava-next
```

---

## 使用 WandB 進行實驗追蹤

WandB 可用於跟踪和監控模型訓練過程，提供實驗數據的視覺化工具。

### 1. 初始化 WandB

```python
import wandb

wandb.init(project="idefics2-8b-training", config={
    "model_name": "HuggingFaceM4/idefics2-8b",
    "dataset_name": "openbmb/RLAIF-V-Dataset",
    "train_split

": 0.3,
    "num_epochs": 1,
    "batch_size": 4,
    "gradient_accumulation_steps": 4,
    "learning_rate": 5e-5
})
```

### 2. 訓練參數設置

```python
from trl import DPOConfig

training_args = DPOConfig(
    output_dir="idefics2-8b-dpo",
    bf16=True,
    gradient_checkpointing=True,
    per_device_train_batch_size=wandb.config.batch_size,
    gradient_accumulation_steps=wandb.config.gradient_accumulation_steps,
    num_train_epochs=wandb.config.num_epochs,
    logging_steps=10,
    report_to="wandb"
)
```

---

## DPO 訓練的標準化流程

1. **視覺-文本對齊任務**：
   使用 `LAION-CC-SBU` 或 `RLHF-V` 數據集進行多模態數據處理。

2. **基於 NLP 的人類反饋優化**：
   使用 DPO 來調整模型生成的文本，使其更符合用戶的偏好。

3. **醫療影像處理**：
   使用 LLaVA-NeXT 進行醫療影像優化，強調視覺推理和文本生成能力。

---

此 README 文件詳細說明了如何進行多模態模型的 DPO 訓練，應用 LoRA 進行微調，並通過 WandB 跟踪實驗過程。如果需要進一步擴展，請參考 Hugging Face 和 TRL 的官方文檔。