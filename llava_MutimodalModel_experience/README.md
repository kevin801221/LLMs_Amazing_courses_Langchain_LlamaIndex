
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
