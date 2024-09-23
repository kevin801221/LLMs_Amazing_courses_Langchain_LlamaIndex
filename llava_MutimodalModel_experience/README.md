
# VQA-RAD DPO 資料集處理

此倉庫包含一個 Python 程式，用於處理 VQA 資料集以進行 DPO（直接偏好優化），並將其準備好進行模型訓練。該程式會下載所需的 CSV 檔案，將拒絕標籤添加到資料中，並格式化資料集。

## 環境設置

在執行程式前，請確保已安裝必要的套件：

```bash
pip install datasets pandas requests
```

## 使用方式

1. **下載 CSV 檔案**：
   此程式包含從指定 URL 下載 CSV 檔案的功能。請將 `csv_url` 替換為實際的檔案位置。

2. **運行程式**：

```bash
python vqa_dpo_processing.py
```

該程式將會下載 CSV 檔案（如果尚未下載）、處理 VQA 資料集，並將格式化後的資料集儲存為 DPO 訓練格式。

## 函數概覽

### 1. `download_file(url: str, dest_path: Path) -> None`

從指定 URL 下載檔案並將其儲存至指定本地路徑。

- `url`: 要下載檔案的 URL。
- `dest_path`: 儲存檔案的本地路徑。

### 2. `load_and_process_vqa_dpo(csv_path: Path, train_df: pd.DataFrame, test_df: pd.DataFrame) -> DatasetDict`

處理 VQA 資料集以進行 DPO，將拒絕標籤加入資料並將其格式化為 Hugging Face 的 DatasetDict 格式。

- `csv_path`: 包含拒絕標籤的 CSV 檔案路徑。
- `train_df`: 包含訓練資料的 DataFrame，預期欄位為 `['image', 'question', 'answer']`。
- `test_df`: 包含測試資料的 DataFrame，與 `train_df` 欄位相同。

### 3. `save_dataset(dataset_dict: DatasetDict, output_path: Path) -> None`

將處理後的資料集儲存至磁碟。

- `dataset_dict`: 要儲存的資料集（DatasetDict）。
- `output_path`: 儲存資料集的路徑。

#### TRL DPO Datasets Basi Tutorial
以下是根據你的需求將 **README.md** 轉換成中文的版本，並進一步詳細說明了如何將各種 LLMs 訓練數據集轉換成 DPO，以及使用 TRL 進行 DPO 訓練流程的步驟。還包括了 LLaVA 1.5、LLaVA 1.6 和 LLaVA-NeXT 的詳細使用方法、訓練做法和推理步驟。

---

# TRL: Transformer Reinforcement Learning - 中文使用說明

本文件詳盡介紹如何使用 TRL 庫對大型語言模型（LLMs）進行微調和對齊，方法包括直接偏好優化（DPO）、監督微調（SFT）、以及近端策略優化（PPO）。此外，還提供了 LLaVA 1.5、LLaVA 1.6 和 LLaVA-NeXT 等模型的具體使用方法與訓練步驟。

## 目錄
1. [概述](#概述)
2. [安裝指南](#安裝指南)
3. [DPO 訓練流程](#DPO-訓練流程)
4. [LLaVA 1.5、LLaVA 1.6 和 LLaVA-NeXT 的使用方法](#LLaVA-1.5-1.6-和-LLaVA-NeXT-的使用方法)
5. [資料集及其應用方法](#資料集及其應用方法)
6. [DPO 訓練的標準化流程，適用於不同情境](#DPO-訓練的標準化流程)

---

## 概述
TRL（Transformer Reinforcement Learning）是一個專門用於微調和對齊變壓器（Transformer）語言模型的庫，支援以下主要方法：

- **監督微調 (SFT)**
- **獎勵建模 (RM)**
- **近端策略優化 (PPO)**
- **直接偏好優化 (DPO)**

該庫構建於 Hugging Face 的 `transformers` 之上，您可以使用任何該庫中提供的模型架構。

### 亮點:
- **高效且可擴展**：基於 `accelerate`，允許從單 GPU 擴展到大規模多節點集群，使用 DDP 和 DeepSpeed 等技術。
- **完全集成 PEFT**：支援使用低資源硬件進行訓練，例如 LoRA 和 QLoRA。
- **CLI 支援**：無需編寫任何代碼，只需透過 CLI 和配置系統即可進行模型微調和對話測試。

---

## 安裝指南

### Python Package 安裝
通過 Python 包安裝 TRL：

```bash
pip install trl
```

### 從源碼安裝
如果您希望使用最新的功能，可以從源碼直接安裝：

```bash
pip install git+https://github.com/huggingface/trl.git
```

### 克隆 Repository
```bash
git clone https://github.com/huggingface/trl.git
```

---

## DPO 訓練流程

DPO（直接偏好優化）是一種根據偏好數據優化模型的技術。以下是如何使用 TRL 進行 DPO 訓練的詳細步驟：

### 將 LLM 訓練數據集轉換為 DPO 格式的步驟：

1. **準備數據集**：
    - 數據集應包含 `query`（查詢）、`chosen`（優選回應）、`rejected`（不優選回應）等欄位。
    - 範例：`RLHF-V Dataset` 包含 `question`、`chosen` 和 `rejected`，需要將這些欄位從一個字段中拆分出來。

2. **DPO 訓練範例**：

    ```python
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import DPOTrainer

    # 加載預訓練模型和 tokenizer
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    tokenizer = AutoTokenizer.from_pretrained("gpt2")

    # 加載您的數據集，格式應符合需求
    dataset = ...  # 數據集加載邏輯

    # 初始化 DPO 訓練器
    trainer = DPOTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
    )

    # 開始訓練
    trainer.train()
    ```

### 數據集轉換：
如果數據集中包含影像模式（例如 RGB），您可以將其轉換為處理所需的格式：

```python
from PIL import Image
from datasets import Dataset

def convert_image_mode(example):
    image = example['images'][0]
    image_converted = image.convert("L")  # 轉換為灰階圖像
    example['images'] = [image_converted]
    return example

converted_dataset = dataset.map(convert_image_mode)
```

---

## LLaVA 1.5、LLaVA 1.6 和 LLaVA-NeXT 的使用方法

### LLaVA 1.5
- **訓練**：
    - 支援較低解析度輸入。
    - 常用於減少模型毒性或視覺-文本對齊任務的訓練。

- **推理**：
    - 適用於基本的視覺語言任務。

- **範例指令**：
    ```bash
    trl sft --model_name_or_path llava-1.5-7b --dataset_name openbmb/RLHF-V-Dataset --output_dir output-llava-1.5
    ```

### LLaVA 1.6
- **訓練**：
    - 支援更高解析度（最高達到 672x672 像素）。
    - 增強的視覺推理和光學字符識別（OCR）能力。

- **推理**：
    - 適用於需要更複雜視覺推理的任務。

- **範例指令**：
    ```bash
    trl dpo --model_name_or_path llava-1.6-7b --dataset_name trl-internal-testing/hh-rlhf-helpful-base-trl-style --output_dir output-llava-1.6
    ```

### LLaVA-NeXT
- **訓練**：
    - 支援超高解析度輸入和動態縱橫比。
    - 適用於醫療影像或高細節視覺任務的最佳選擇。

- **推理**：
    - 在多模態任務（如 OCR 和世界知識推理）中具有頂尖表現。

- **範例指令**：
    ```bash
    trl chat --model_name_or_path llava-next-7b --dataset_name medical-vqa-dataset --output_dir output-llava-next
    ```

---

## 資料集及其應用方法

1. **RLHF-V Dataset**：
    - 包含偏好數據，用於 DPO（直接偏好優化）訓練。
    - 應用場景：對模型進行人類偏好對齊的微調。

2. **RLAIF-V Dataset**：
    - 使用於 DPO 技術進行偏好學習的資料集。
    - 範例：醫療數據集中，提供選擇和拒絕答案進行比較的場景。

3. **LAION-CC-SBU Dataset**：
    - 圖像數據集，用於微調 LLaVA-NeXT 等模型。
    - 應用場景：強化多模態模型對視覺和文本數據的對齊能力。

4. **TextVQA Dataset**：
    - 基於文本的視覺問答（VQA）資料集。
    - 應用場景：提高模型的 OCR 和視覺推理能力。

---

## DPO 訓練的標準化流程，適用於不同情境

### 如何將 DPO 流程映射到各種情境中

1. **情境 1：視覺-文本對齊任務**
    - **資料集**：使用多模態數據集，如 LAION-CC-SBU 或 RLHF-V。
    - **任務**：讓模型學會生成與給定圖像匹配的偏好文字描述。
    - **訓練器**：使用 `DPOTrainer` 根據生成的描述進行優選與否的微調。

2. **情境 2：基於 NLP 的人類反饋**
    - **資料集**：任何基於文本的偏好數據集（如 RLHF-V）。
    - **任務**：訓練模型，使其

在文本生成中更傾向於用戶偏好的回應。
    - **訓練器**：使用 `DPOTrainer`，針對優選和不優選的文本進行優化。

3. **情境 3：醫療影像理解**
    - **資料集**：醫療影像資料集，如 VQA-DPO。
    - **任務**：使用高解析度醫療影像來優化模型的推理，根據醫生的反饋進行偏好優化。
    - **訓練器**：使用 LLaVA-NeXT，專注於增強的 OCR 和視覺推理能力進行微調。

---

此 README.md 文件應提供對 DPO 訓練流程的完整理解，並涵蓋了如何使用 TRL 進行模型微調以及不同 LLaVA 模型在不同場景中的應用。